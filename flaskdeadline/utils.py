
from flaskdeadline.models import Student, Module, Lecturer, Reliable, Deadline, Coursework, Hours, ACCESS, VOTE
from flaskdeadline import app, db
from datetime import datetime
from dateutil.tz import gettz
from gekko import GEKKO
import pandas as pd
from numpy import cumsum
from flaskdeadline.onelogin.saml2.auth import OneLogin_Saml2_Auth



def linear_opt(start_end,ects_breakdown):
    timezone_variable = gettz("Europe/London") 
    m = GEKKO(remote=False)

    # Number of modules
    n = int(len(start_end)/2)
    no_intervals = len(start_end)-1
    sorted_dates = start_end.copy()

    # Sorted the dates from earliest to latest, hence getting the itnervals
    sorted_dates.sort()
    interval_days = [0] * (no_intervals)
    exist = []
    for i in range(n):
        exist.append([0]*no_intervals)
    for s in range(no_intervals):
        interval_days[s] = (sorted_dates[s+1] - sorted_dates[s]).days
    for t in range(n):
        for s in range(no_intervals):
            if start_end[t*2]<= sorted_dates[s] and sorted_dates[s+1] <= start_end[t*2+1] :
                exist[t][s] = 1
    # Creating variables for linear optimisation
    Z = m.Var()
    intensity_val = m.Array(m.Var,(n,no_intervals)) # Dynamic creation of variables to schedule arbitrary number of modules
    for i in range(n):
        for j in range(no_intervals):
                    intensity_val[i,j].lower = 0 # set all variables to be positive


    m.Minimize(Z)

    equality_equations = []
    for i in range(n):
        result = 0
        for j in range(no_intervals):
            if exist[i][j] == 1:
                result = result + interval_days[j]*intensity_val[i][j]
        equality_equations.append(result == ects_breakdown[i])

    m.Equations([equality_equations])

    inequality_equations = []
    for i in range(no_intervals):
        result = 0
        for j in range(n):
            if exist[j][i]:
                result = result + intensity_val[j][i]
        inequality_equations.append(Z >=result)


    m.Equations([inequality_equations])
    m.solve(disp=False)
    print('Solver Time: ', m.options.SOLVETIME)

    # Creating data for graph
    date_range = pd.date_range(start=sorted_dates[0], end = sorted_dates[-1]).to_pydatetime().tolist()
    date_range = [i.strftime("%d/%m/%Y") for i in date_range]

    # putting intensity values into an array
    date_intensity = []
    # if coursework does not exist in that interval, set it to 0
    for i in range(n):
        for j in range(no_intervals):
                    intensity_val[i][j].value[0]=intensity_val[i][j].value[0] * exist[i][j]
        
    for i in intensity_val: # for each coursework
        temp = [i[0].value[0]]
        for j in range(no_intervals):
            for k in range(interval_days[j]):
                temp.append(i[j].value[0])
        date_intensity.append(temp)

    # Sum up intensity values across all module for each interval
    sum_interval = []
    for i in date_intensity:
        sum_interval = [sum(x) for x in zip(*date_intensity)]
    date_intensity.insert(0,sum_interval)

    return (date_intensity,date_range)

def deadline_data(deadline_array, deadlines_voted):
    '''
    Aimed to extract the the deadlines and their votes in this form:
    {'Communication Networks': 
        {'Coursework 1': [[datetime.datetime(2022, 6, 18, 12, 0), 2, 0, [1, False, True,False]], [datetime.datetime(2022, 6, 19, 12, 0), 1, 0, [0, False, True,False]]], 
         'Coursework 2': [[datetime.datetime(2022, 6, 20, 12, 0), 0, 1, [0, False, False,False]]]}}
    Title of module as the key for a dict, and the output is another dict with the coursework title as the key
    The output of the nest dict is an array of array, with each element of the outer array being data corresponding to 1 deadline.
    Each element of the inner array is as follow:
        [date, upvotes, downvotes, [What user voted for: 1 -> up, 2-> down, 0 -> neutral], Did Lect responsible vote?, Is this the majority?, Did GTA vote?]]
    '''
    return_array = {}
    
    for element in deadline_array:
        '''
        deadline_array had this form:
        ('Coursework 1', 'ELEC40005', datetime.datetime(2022, 6, 17, 3, 25), 1, 0, 1)
        (Cw_title, Module_id, date, # of upvotes, # of downvotes, total # of votes)
        '''
        mod = Module.query.filter_by(id=element[1]).first()
        modname = mod.title
        gta_array = mod.gta_responsible
        lect_responsible = mod.lecturer_responsible
        lect_deadline = []
        gta_deadline = []
        reliability_count = 0
        if gta_array:
            for gta in gta_array:
                gta_deadline.append(Deadline.query.filter_by(student_id=gta.id).all())
        else:
            gta_deadline = None

        if lect_responsible:
            for lect in lect_responsible:
                lect_deadline.append(Deadline.query.filter_by(lecturer_id=lect.id).all())
        else:
            lect_deadline = None
        data = [0] #[Did user vote, Did Lect vote, Is majority?]    
        for vote in deadlines_voted:
            if vote.module_id == element[1] and vote.date == element[2] and vote.coursework_id == element[0]:
                if vote.vote == "Up":
                    data[0] = VOTE['Up']
                elif vote.vote == "Down":
                    data[0] = VOTE['Down']
        # Majority of staff must agree on same deadline
        lect_vote = False
        lect_count = 0
        if lect_deadline:
            for outer in lect_deadline:
                for inner in outer:
                    if inner.vote =="Up" and inner.date==element[2]:
                        lect_count = lect_count + 1
            if lect_count > len(lect_deadline)/2:
                lect_vote = True
                reliability_count = reliability_count + 1
        data.append(lect_vote)
        # Majority Vote
        if element[3] > element[5]/2:
            data.append(True)
            reliability_count = reliability_count + 1
        else:
            data.append(False)
        # >50% of gta that voted must vote on same deadline
        gta_vote = False
        gta_count = 0
        if gta_deadline:
            for outer in gta_deadline:
                for inner in outer:
                    if inner.vote =="Up" and inner.date==element[2]:
                        gta_count = gta_count +1
            if gta_count > len(gta_deadline)/2:
                gta_vote = True
                reliability_count = reliability_count + 1
        data.append(gta_vote)
        # Adding/Updating the Reliable Table
        current_rel = Reliable.query.filter_by(module_id = mod.id, coursework_title = element[0]).first()
        if current_rel:
            # If the date is currently the most reliable one
            if current_rel.date.date() == element[2].date():
                current_rel.lect = data[1]
                current_rel.majority = data[2]
                current_rel.gta = data[3]
                current_rel.vote = element[3]
                db.session.commit()
            else:
                indicator = current_rel.gta + current_rel.lect+ current_rel.majority
                if (reliability_count == indicator and element[3] > current_rel.vote) or reliability_count > indicator:
                    current_rel.date = element[2]
                    current_rel.lect = data[1]
                    current_rel.majority = data[2]
                    current_rel.gta = data[3]
                    current_rel.vote = element[3]
                    db.session.commit()
        else:
            add_reliable = Reliable(coursework_title = element[0], module_id = mod.id, date = element[2],lect = data[1], majority = data[2], gta = data[3], vote = element[3])
            db.session.add(add_reliable)
            db.session.commit() 
    
        # putting all the data into a dict of dicts as the return array
        if modname in return_array:
            temp = return_array[modname]
            if element[0] in return_array[modname]:
                temp = return_array[modname][element[0]]
                temp.append([element[2],element[3],element[4],data])
                return_array[modname][element[0]] = temp
            else:
                return_array[modname][element[0]] = [[element[2],element[3],element[4],data]]
        else:
            return_array[modname] = {element[0]:[[element[2],element[3],element[4],data]]}
    return return_array


def startdate_data(deadline_array):
    '''
    Aimed to extract the start dates of coursework in this form:
    {'Communication Networks': 
        {'Coursework 1': datetime.datetime(2022, 6, 18, 12, 0), 
         'Coursework 2': datetime.datetime(2022, 6, 20, 12, 0)}}
    Title of module as the key for a dict, and the output is another dict with the coursework title as the key
    The output of the nest dict is the start date of the coursework
    '''
    return_array = {}
    
    for element in deadline_array:
        mod = Module.query.filter_by(id=element[1]).first()
        modname = mod.title
        if modname in return_array:
            return_array[modname][element[0]] = element[2]
        else:
            return_array[modname] = {element[0]:element[2]}
    return return_array

# Functions for SAML login

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=app.config['SAML_PATH'])
    return auth


def prepare_flask_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'script_name': request.path,
        'get_data': request.args.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.form.copy(),
    }