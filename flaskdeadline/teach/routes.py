from flask import render_template, url_for, flash, redirect, session, Blueprint
from flaskdeadline import db
from flaskdeadline.models import Student, Module, Lecturer, Deadline, Coursework, Hours, ACCESS, Reliable
from flaskdeadline.forms import DeadlineForm, ResponsibilityForm, StaffEditForm, BreakdownForm, GTAForm, OptimisationForm
from sqlalchemy import update, func, and_
from datetime import datetime
from dateutil.tz import gettz
import time
from flaskdeadline.utils import deadline_data, linear_opt, startdate_data

teach = Blueprint('teach',__name__)


@teach.route("/teststaff")
def test():
    session['id'] = 'jbarria'
    session['name'] = 'Javier Barria'
    session['email'] = 'j.barria@imperial.ac.uk'
    session['access'] = ACCESS['staff']
    return redirect(url_for('teach.staff'))



@teach.route('/staff/<string:module>/<string:cw>/<string:date>/up')
def staff_upvote_deadline(module,cw,date):
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    else:
        user = Lecturer.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    mod = Module.query.filter_by(title=module).first()
    # Change Vote of deadline
    to_change = Deadline.query.filter_by(lecturer=user,module=mod,coursework_id=cw,date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).first()
    if to_change:
        if to_change.vote == "Up":
            to_change.vote = "Neutral"
        else:
            to_change.vote="Up"
    else:
        insert = Deadline(student_id = '',lecturer_id=user.id, module_id=mod.id,coursework_id=cw,date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),vote="Up")
        db.session.add(insert)
    db.session.commit()
    return redirect(url_for('teach.staff'))

@teach.route('/staff/<string:module>/<string:cw>/<string:date>/down')
def staff_downvote_deadline(module,cw,date):
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    else:
        user = Lecturer.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    mod = Module.query.filter_by(title=module).first()
    # Change Vote of deadline
    to_change = Deadline.query.filter_by(lecturer=user,module=mod,coursework_id=cw,date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).first()
    if to_change:
        if to_change.vote == "Down":
            to_change.vote = "Neutral"
        else:
            to_change.vote = "Down"
    else:
        insert = Deadline(student_id = '', lecturer_id=user.id,module_id=mod.id,coursework_id=cw,date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),vote="Down")
        db.session.add(insert)
    db.session.commit()
    return redirect(url_for('teach.staff'))

@teach.route("/staff/gta/<string:module_title>", methods=['GET', 'POST'])
def staff_gta_assignment(module_title):
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    form = GTAForm()
    mod = Module.query.filter_by(title=module_title).first()
    # Assigning GTA to the module     
    student = db.session.query(Student).all()
    form.gta.choices = sorted([m.id + " - " + m.name for m in student])
    if form.validate_on_submit():
        data = form.gta.data.split(" - ")
        gta = Student.query.filter_by(id=data[0]).first()
        mod.gta_responsible.append(gta)
        db.session.commit()
        return redirect(url_for('teach.staff'))
    return render_template('gta.html', form=form, mod=mod ,staff=True)

@teach.route("/staff/cw/edit/<string:module_title>/<string:cw>", methods=['GET', 'POST'])
def staff_edit_breakdown(module_title,cw):
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    form = BreakdownForm()
    mod = Module.query.filter_by(title=module_title).first()
    cwk = Coursework.query.filter_by(title=cw,module_id = mod.id).first()
    original_title = cwk.title
    if form.validate_on_submit():
        #  Only edit title when the coursework title is different
        if original_title != form.coursework_title.data:
            cwk.title = form.coursework_title.data
            db.session.commit()
            # edit the coursework title with other Tables
            stmt = update(Deadline).where(and_(Deadline.coursework_id==original_title, Deadline.module_id==mod.id)).values(coursework_id=form.coursework_title.data).execution_options(synchronize_session="fetch")
            stmt2 = update(Hours).where(and_(Hours.coursework_title==original_title, Hours.module_id==mod.id)).values(coursework_title=form.coursework_title.data).execution_options(synchronize_session="fetch")
            stmt3 = update(Reliable).where(and_(Reliable.coursework_title==original_title, Reliable.module_id==mod.id)).values(coursework_title=form.coursework_title.data).execution_options(synchronize_session="fetch")
            db.session.execute(stmt)
            db.session.execute(stmt2)
            db.session.execute(stmt3)
        cwk.start_date = form.start_date.data
        cwk.breakdown = form.breakdown.data
        db.session.commit()
        return redirect(url_for('teach.staff'))
    return render_template('edit_breakdown.html', form=form, cwk=cwk,staff=True)

@teach.route("/staff/module/new", methods=['GET', 'POST'])
def new_staff_mod():
    form = ResponsibilityForm()
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    else:
        user = Lecturer.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    # Adding modules they are responsible for
    if form.validate_on_submit():
        check_id = Module.query.filter_by(id = form.id.data).first()
        check_title = Module.query.filter_by(title = form.title.data).first()
        # prevent any spelling errors,if either id or title is available, assign it to that first.
        if check_id:
            user.module_responsible.append(check_id)
        elif check_title:
            user.module_responsible.append(check_title)
        else:
            module = Module(id = form.id.data, title = form.title.data, ects = form.ects.data, content = form.content.data)
            db.session.add(module)
            user.module_responsible.append(module)
        check_cw = Coursework.query.filter_by(title = form.coursework_title.data, module_id = form.id.data).first()
        check_deadline = Deadline.query.filter_by(coursework_id = form.coursework_title.data, lecturer_id = user.id, module_id =form.id.data).first()
        # Checking if deadline or coursework already exist
        if check_cw:
            check_cw.title = form.coursework_title.data
            check_cw.breakdown  = form.breakdown.data
            check_cw.start_date = form.start_date.data
        else:
            cw = Coursework(title = form.coursework_title.data, module_id = form.id.data, breakdown = form.breakdown.data, start_date = form.start_date.data)
            db.session.add(cw)
        if check_deadline:
            check_deadline.date = form.date.data
            check_deadline.vote = "Up"
        else:
            deadline = Deadline(coursework_id = form.coursework_title.data, lecturer_id = user.id, module_id =form.id.data,student_id = '', date = form.date.data, vote = "Up")
            db.session.add(deadline)
        db.session.commit()
        return redirect(url_for('teach.staff'))
    return render_template('staff_mod.html', form=form, staff=True)

@teach.route('/staff/subscribe/<string:module>')
def remove_res(module):
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    else:
        user = Lecturer.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    # Remove it if they accidentally said they were responsible for it
    adding = Module.query.filter_by(id=module).first()
    if adding in user.module_responsible:
        user.module_responsible.remove(adding)
    else:
        user.module_responsible.append(adding)
    db.session.commit()
    return redirect(url_for('teach.staff'))

@teach.route("/staff/deadline/new/<string:module_title>", methods=['GET', 'POST'])
def staff_new_deadline(module_title):
    form = DeadlineForm()
    mod = Module.query.filter_by(title=module_title).first()
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    else:
        user = Lecturer.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    if form.validate_on_submit():
        # 2 checks: 1. User votes up on another deadline / 2. Deadline already exist and user voted already
        deadline_check1 = Deadline.query.filter_by(module_id=form.id.data,coursework_id=form.coursework_title.data,lecturer_id=user.id,vote="Up").all()
        deadline_check2 = Deadline.query.filter_by(module_id=form.id.data,coursework_id=form.coursework_title.data,lecturer_id=user.id, date = form.date.data).first()
        cw_check = Coursework.query.filter_by(module_id=form.id.data,title =form.coursework_title.data).first()
        if not cw_check:
            cw = Coursework(title = form.coursework_title.data, module_id =form.id.data, breakdown = form.breakdown.data, start_date = form.start_date.data)
            db.session.add(cw)
        # If user already subscribe to a deadline
        if deadline_check1:
            for element in deadline_check1:
                element.vote = "Neutral"
        if deadline_check2:
            deadline_check2.vote = "Up"
        else:
            deadline = Deadline(coursework_id = form.coursework_title.data, student_id = '', module_id =form.id.data,lecturer_id = user.id, date = form.date.data, vote = "Up")
            db.session.add(deadline)
        db.session.commit()
        return redirect(url_for('teach.staff'))
    return render_template('new_deadline.html', form=form, mod=mod,staff=True)

@teach.route("/staff/edit/<string:module_title>", methods=['GET', 'POST'])
def staff_edit_mod(module_title):
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    form = StaffEditForm()
    mod = Module.query.filter_by(title=module_title).first()
    original_id = mod.id
    original_title = mod.title
    check_id = check_title = False
    # Check if the title or module id already exist
    if form.validate_on_submit():
        if original_id != form.id.data:
            check_id = Module.query.filter_by(id = form.id.data).first()
        if original_title != form.title.data:
            check_title = Module.query.filter_by(title = form.title.data).first()
        if check_id or check_title:
            flash('Module ID or title already exists', 'danger')
        else:
            mod.title = form.title.data
            mod.id = form.id.data
            mod.ects = form.ects.data
            mod.content = form.content.data
            db.session.commit()
            # Change everywhere module id is used
            stmt = update(Deadline).where(Deadline.module_id==original_id).values(module_id=form.id.data).execution_options(synchronize_session="fetch")
            stmt2 = update(Hours).where(Hours.module_id==original_id).values(module_id=form.id.data).execution_options(synchronize_session="fetch")
            stmt3 = update(Coursework).where(Coursework.module_id==original_id).values(module_id=form.id.data).execution_options(synchronize_session="fetch")
            stmt4 = update(Reliable).where(Reliable.module_id==original_id).values(module_id=form.id.data).execution_options(synchronize_session="fetch")
            db.session.execute(stmt)
            db.session.execute(stmt2)
            db.session.execute(stmt3)
            db.session.execute(stmt4)
            db.session.commit()
            return redirect(url_for('teach.staff'))
    return render_template('staff_update_mod.html', form=form, mod =mod,staff=True)


@teach.route("/staff/feedback/<string:module>/<string:cw>")
def staff_feedback(module,cw):
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    mod = Module.query.filter_by(title=module).first()
    '''
    Get feedback data in this format:
    [('student_id',number of hours, expectation),...]
    0 -> Less than expected, 1 -> Similar to expectation, 2 -> More than expected
    '''
    feedback_data = (db.session.query(Hours.student_id,Hours.hours,Hours.expected)
    .group_by(Hours.student_id,Hours.hours,Hours.expected)
     ).filter_by(module_id = mod.id,coursework_title=cw).all()
    for i in range(len(feedback_data)):
        if feedback_data[i][2] == 0:
            feedback_data[i] = (feedback_data[i][0],feedback_data[i][1], "Less Than Expected")
        elif feedback_data[i][2] == 1:
            feedback_data[i] = (feedback_data[i][0],feedback_data[i][1], "Similar to my Expectations")
        elif feedback_data[i][2] == 2:
            feedback_data[i] = (feedback_data[i][0],feedback_data[i][1], "More Than Expected")
    return render_template('staff_hours_data.html', attributes= feedback_data, staff= True)


@teach.route('/staff/scheduling', methods=['GET', 'POST'])
def staff_intensity():
    form = OptimisationForm()
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    else:
        user = Lecturer.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    avail = Module.query.all()
    teacher = user
    data = None
    label = None
    names = None
    cw = Coursework.query.all()
    choices = [m.module.title + " - " + m.title for m in cw]
    choices.append("---")
    form.c1.choices = sorted(choices)
    form.c2.choices = sorted(choices)
    form.c3.choices = sorted(choices)
    form.c4.choices = sorted(choices)
    form.c5.choices = sorted(choices)
    start_dates_dict = {}
    start_end_dates =[]
    if form.validate_on_submit():
        cwk_list = []
        names = []
        if form.c1.data != "---":
            data = form.c1.data.split(" - ")
            cwk_list.append((data[0],data[1]))
            names.append(form.c1.data)
        if form.c2.data != "---":
            data = form.c2.data.split(" - ")
            cwk_list.append((data[0],data[1]))
            names.append(form.c2.data)
        if form.c3.data != "---":
            data = form.c3.data.split(" - ")
            cwk_list.append((data[0],data[1]))
            names.append(form.c3.data)
        if form.c4.data != "---":
            data = form.c4.data.split(" - ")
            cwk_list.append((data[0],data[1]))
            names.append(form.c4.data)
        if form.c5.data != "---":
            data = form.c5.data.split(" - ")
            cwk_list.append((data[0],data[1]))
            names.append(form.c5.data)
        ects_breakdown = []
        for i in cwk_list:
            mod = Module.query.filter_by(title=i[0]).first()
            cw = Coursework.query.filter_by(title=i[1],module_id = mod.id).first()
            deadline = Reliable.query.filter_by(coursework_title=i[1], module_id = mod.id).first()
            ects_breakdown.append(cw.breakdown*mod.ects)
            start_end_dates.append(cw.start_date.date())
            start_end_dates.append(deadline.date.date())
            start_dates_dict[i] = (cw.start_date.date(),deadline.date.date())
        if len(ects_breakdown)!=5:
            ects_breakdown = ects_breakdown + [0]*(5-len(ects_breakdown))
        print("STart end: ",start_end_dates)
        data,label = linear_opt(start_end_dates,ects_breakdown)
        print(ects_breakdown)
        print(start_end_dates)
        if len(data)!=6:
            data= data + [[0]]*(6-len(data))
        if len(names)!=5:
            names= names + ["---"]*(5-len(names))

    return render_template("lin_opt.html", display= start_dates_dict,  avail_modules = avail,form = form, staff= True,taking = teacher.module_responsible, user=teacher, label=label,date=data, cwk= names)



@teach.route('/staff')
def staff():
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['student']:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('students.home'))
    else:
        user = Lecturer.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    avail = Module.query.all()
    teacher = user

    # All modules responsible by the teacher
    # Check which modules are taken by the teacher
    check = [row.id for row in teacher.module_responsible]

    # Deadlines that Lecturer voted for
    deadlines_voted = Deadline.query.filter_by(lecturer_id=teacher.id).all()
    # All deadlines subscribed by teacher
    all_deadlines_subscribed = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date,func.count(Deadline.vote).filter(Deadline.vote=="Up").label('# Upvote'),func.count(Deadline.vote).filter(Deadline.vote=="Down").label('# Downvote'),func.count(Deadline.vote).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.in_(check)).all()

    # Get the coursework start dates of all coursework 
    cw_startdate = (db.session.query(Coursework.title,Coursework.module_id,Coursework.start_date)
     ).all()


    # All other deadlines not subscribed by teacher
    all_deadlines_else = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date,func.count(Deadline.vote).filter(Deadline.vote=="Up"),func.count(Deadline.vote).filter(Deadline.vote=="Down"),func.count(Deadline.vote).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.not_in(check)).all()


    # Checking the average number of hours for each coursework
    no_hours = {}
    all_cw = Coursework.query.all()
    for cw in all_cw:
        avg_hrs = db.session.query(func.avg(Hours.hours).label('average')).filter_by(coursework_title=cw.title,module_id=cw.module_id).all()
        count = db.session.query(func.count(Hours.hours).label('number')).filter_by(coursework_title=cw.title,module_id=cw.module_id).all()
        if cw.module.title in no_hours:
            no_hours[cw.module.title][cw.title] = (avg_hrs[0][0],count[0][0])
        else:
            no_hours[cw.module.title] = {cw.title:(avg_hrs[0][0],count[0][0])}

    teacher_mod = deadline_data(all_deadlines_subscribed,deadlines_voted)
    
    all_else_mod = deadline_data(all_deadlines_else,deadlines_voted)
    

    return render_template("new_staff.html", teacher_deadlines=teacher_mod, avail_modules = avail, taking = teacher.module_responsible, user=teacher, all_else=all_else_mod, staff=True, hours= no_hours, start = startdate_data(cw_startdate))

