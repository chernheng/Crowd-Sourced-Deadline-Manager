from flask import render_template, url_for, flash, redirect, session, Blueprint
from flaskdeadline import db
from flaskdeadline.models import Student, Module, Deadline, Coursework, Hours, ACCESS, Reliable
from flaskdeadline.forms import ModuleForm, EditForm, DeadlineForm, FeedbackForm, BreakdownForm, OptimisationForm
from sqlalchemy import update, func, and_
from datetime import datetime
from dateutil.tz import gettz
from flaskdeadline.utils import deadline_data, linear_opt, startdate_data

students = Blueprint('students',__name__)

timezone_variable = gettz("Europe/London") 
@students.route('/index1')
def index11():
    current_date = Deadline.query.filter_by(coursework_id = 'Coursework 1', student_id = 'cht119', module_id ='ELEC60006',vote= "Down").first()
    current_date.vote = "Up"
    print(current_date)
    db.session.commit()
    check = Deadline.query.filter_by(coursework_id = 'Coursework 1', student_id = 'cht119', module_id ='ELEC60006',vote= "Up").all()
    print(check)
    check_date =  Deadline.query.filter_by(coursework_id = 'Coursework 1', student_id = 'cht119', module_id ='ELEC60006',date = datetime(2022, 6,19,12,0,0,0,timezone_variable)).first()
    print(check_date)
    return render_template('index1.html')

@students.route('/<string:module>/<string:cw>/<string:date>/up')
def upvote_deadline(module,cw,date):
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    else:
        user = Student.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    mod = Module.query.filter_by(title=module).first()
    to_change = Deadline.query.filter_by(student=user,module=mod,lecturer_id = '',coursework_id=cw,date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).first()
    if to_change:
        if to_change.vote == "Up":
            to_change.vote = "Neutral"
        else:
            to_change.vote="Up"
    else:
        insert = Deadline(student_id = user.id, module_id=mod.id,lecturer_id = '',coursework_id=cw,date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),vote="Up")
        db.session.add(insert)
    db.session.commit()
    return redirect(url_for('students.home'))

@students.route('/<string:module>/<string:cw>/<string:date>/down')
def downvote_deadline(module,cw,date):
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    else:
        user = Student.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    mod = Module.query.filter_by(title=module).first()
    to_change = Deadline.query.filter_by(student=user,lecturer_id='',module=mod,coursework_id=cw,date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).first()
    if to_change:
        if to_change.vote == "Down":
            to_change.vote = "Neutral"
        else:
            to_change.vote = "Down"
    else:
        insert = Deadline(student_id = user.id, lecturer_id='',module_id=mod.id,coursework_id=cw,date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),vote="Down")
        db.session.add(insert)
    db.session.commit()
    return redirect(url_for('students.home'))

@students.route("/feedback/<string:module>/<string:cw>", methods=['GET', 'POST'])
def feedback(module,cw):
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    else:
        user = Student.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    form = FeedbackForm()
    mod = Module.query.filter_by(title=module).first()
    cw_data = Coursework.query.filter_by(title=cw, module_id = mod.id).first()
    print(cw)
    if form.validate_on_submit():
        expectation = 1 # Similar to expectation
        if form.expectation.data == "More than expected":
            expectation = 2
        elif form.expectation.data == "Less than expected":
            expectation = 0
        check_hours = Hours.query.filter_by(student_id = user.id, coursework_title = cw, module_id = mod.id).first()
        if check_hours:
            check_hours.hours = form.hours.data
            check_hours.expected = expectation
        else:
            new_hour = Hours(module_id=mod.id, student_id=user.id,coursework_title=cw, hours=form.hours.data, expected = expectation)
            db.session.add(new_hour)
        db.session.commit()
        return redirect(url_for('students.home'))
    return render_template('feedback.html', form=form, cw =cw_data)

@students.route('/subscribed/<string:module_id>')
def subscribed(module_id):
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    else:
        user = Student.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    adding = Module.query.filter_by(id=module_id).first()
    if adding in user.module_taken:
        user.module_taken.remove(adding)
    else:
        user.module_taken.append(adding)
    db.session.commit()
    return redirect(url_for('students.home'))


@students.route("/module/new", methods=['GET', 'POST'])
def new_mod():
    form = ModuleForm()
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    else:
        user = Student.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    if form.validate_on_submit():
        check_id = Module.query.filter_by(id = form.id.data).first()
        check_title = Module.query.filter_by(title = form.title.data).first()
        if check_id or check_title:
            flash('Module already exists', 'danger')
        else:
            module = Module(id = form.id.data, title = form.title.data,ects=form.ects.data)
            cw = Coursework(title = form.coursework_title.data, module_id = form.id.data, breakdown = form.breakdown.data, start_date = form.start_date.data)
            deadline = Deadline(coursework_id = form.coursework_title.data, student_id = user.id, module_id =form.id.data,lecturer_id = '', date = form.date.data, vote = "Up")
            db.session.add_all([module,cw,deadline])
            db.session.commit()
            user.module_taken.append(module)
            db.session.commit()
            return redirect(url_for('students.home'))
    return render_template('create_mod.html', form=form)

@students.route("/deadline/new/<string:module_title>", methods=['GET', 'POST'])
def new_deadline(module_title):
    form = DeadlineForm()
    mod = Module.query.filter_by(title=module_title).first()
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    else:
        user = Student.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    if form.validate_on_submit():
        # 2 checks: 1. User votes up on another deadline / 2. Deadline already exist and user voted already
        deadline_check1 = Deadline.query.filter_by(module_id=form.id.data,coursework_id=form.coursework_title.data,student_id=user.id,vote="Up").all()
        deadline_check2 = Deadline.query.filter_by(module_id=form.id.data,coursework_id=form.coursework_title.data,student_id=user.id, date = form.date.data).first()
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
            deadline = Deadline(coursework_id = form.coursework_title.data, student_id = user.id, module_id =form.id.data,lecturer_id = '', date = form.date.data, vote = "Up")
            db.session.add(deadline)
        db.session.commit()
        return redirect(url_for('students.home'))
    return render_template('new_deadline.html', form=form, mod=mod)

@students.route("/edit/<string:module_title>", methods=['GET', 'POST'])
def edit_mod(module_title):
    form = EditForm()
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    mod = Module.query.filter_by(title=module_title).first()
    original_id = mod.id
    original_title = mod.title
    check_id = check_title = False
    if form.validate_on_submit():
        if original_title == form.title.data and original_id == form.id.data:
            return redirect(url_for('students.home'))
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
            db.session.commit()
            stmt = update(Deadline).where(Deadline.module_id==original_id).values(module_id=form.id.data).execution_options(synchronize_session="fetch")
            stmt2 = update(Hours).where(Hours.module_id==original_id).values(module_id=form.id.data).execution_options(synchronize_session="fetch")
            stmt3 = update(Coursework).where(Coursework.module_id==original_id).values(module_id=form.id.data).execution_options(synchronize_session="fetch")
            db.session.execute(stmt)
            db.session.execute(stmt2)
            db.session.execute(stmt3)
            db.session.commit()
            return redirect(url_for('students.home'))
    return render_template('update_mod.html', form=form, mod =mod)

@students.route("/cw/edit/<string:module_title>/<string:cw>", methods=['GET', 'POST'])
def edit_breakdown(module_title,cw):
    form = BreakdownForm()
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    mod = Module.query.filter_by(title=module_title).first()
    cwk = Coursework.query.filter_by(title=cw,module_id = mod.id).first()
    print(cwk.start_date)
    original_title = cwk.title
    if form.validate_on_submit():
        if original_title != form.coursework_title.data:
            cwk.title = form.coursework_title.data
            db.session.commit()
            stmt = update(Deadline).where(and_(Deadline.coursework_id==original_title, Deadline.module_id==mod.id)).values(coursework_id=form.coursework_title.data).execution_options(synchronize_session="fetch")
            stmt2 = update(Hours).where(and_(Hours.coursework_title==original_title, Hours.module_id==mod.id)).values(coursework_title=form.coursework_title.data).execution_options(synchronize_session="fetch")
            db.session.execute(stmt)
            db.session.execute(stmt2)
        cwk.breakdown = form.breakdown.data
        cwk.start_date = form.start_date.data
        db.session.commit()
        return redirect(url_for('students.home'))
    return render_template('edit_breakdown.html', form=form, cwk=cwk)


@students.route('/scheduling', methods=['GET', 'POST'])
def intensity():
    form = OptimisationForm()
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    else:
        user = Student.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    avail = Module.query.all()
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
    timezone_variable = gettz("Europe/London") 
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
        print(cwk_list)
        print("Waht the hell")
        ects_breakdown = []
        start_end_dates =[]
        for i in cwk_list:
            mod = Module.query.filter_by(title=i[0]).first()
            cw = Coursework.query.filter_by(title=i[1],module_id = mod.id).first()
            deadline = Reliable.query.filter_by(coursework_title=i[1], module_id = mod.id).first()
            print(i)
            print(deadline)
            ects_breakdown.append(cw.breakdown*mod.ects)
            start_end_dates.append(cw.start_date.date())
            start_end_dates.append(deadline.date.date())
        if len(ects_breakdown)!=5:
            ects_breakdown = ects_breakdown + [0]*(5-len(ects_breakdown))
        print("STart end: ",start_end_dates)
        data,label = linear_opt(start_end_dates,ects_breakdown)
        print(ects_breakdown)
        print(start_end_dates)
        if len(data)!=5:
            data= data + [[0]]*(5-len(data))
        if len(names)!=5:
            names= names + ["---"]*(5-len(names))

    return render_template("lin_opt.html",  form = form, avail_modules = avail, taking = user.module_taken, user=user, label=label,date=data, cwk= names)


@students.route('/home')
def home():
    user = None
    if not session['samlUserdata']:
        return redirect(url_for('main.landing'))
    elif session['access'] == ACCESS['staff']:
        flash('Please use the staff page!', 'danger')
        return redirect(url_for('teach.staff'))
    else:
        user = Student.query.filter_by(id=session['id'],name=session['name'],email=session['email']).first()
        if not user:
            flash('User does not exist!', 'danger')
            return redirect(url_for('main.landing'))
    avail = Module.query.all()
    # Check which modules are taken by the user
    check = [row.id for row in user.module_taken]
    # for x in user.module_taken:
    #     check.append(x.id)
    print(user.module_taken)
    no_deadline_mod = []
    for row in user.module_taken:
        if row.module_vote == []:
            no_deadline_mod.append(row)
    print(no_deadline_mod)

    # Deadlines that student voted for
    deadlines_voted = Deadline.query.filter_by(student=user).all()
    print(deadlines_voted)

    # All deadlines subscribed by student
    all_deadlines_subscribed = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date,func.count(Deadline.vote).filter(Deadline.vote=="Up"),func.count(Deadline.vote).filter(Deadline.vote=="Down"),func.count(Deadline.vote).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.in_(check)).all()
    '''
    all_deadlines_subscribed had this form:
    ('Coursework 1', 'ELEC40005', datetime.datetime(2022, 6, 17, 3, 25), 1, 0, 1)
    (Cw_title, Module_id, date, # of upvotes, # of downvotes, total # of votes)
    '''
    cw_startdate = (db.session.query(Coursework.title,Coursework.module_id,Coursework.start_date)
     ).filter(Coursework.module_id.in_(check)).all()

    no_hours = {}
    all_cw = Coursework.query.all()
    for cw in all_cw:
        avg_hrs = db.session.query(func.avg(Hours.hours).label('average')).filter_by(coursework_title=cw.title,module_id=cw.module_id).all()
        count = db.session.query(func.count(Hours.hours).label('number')).filter_by(coursework_title=cw.title,module_id=cw.module_id).all()
        if cw.module.title in no_hours:
            no_hours[cw.module.title][cw.title] = (avg_hrs[0][0],count[0][0])
        else:
            no_hours[cw.module.title] = {cw.title:(avg_hrs[0][0],count[0][0])}
    print(no_hours)
    student_deadline = deadline_data(all_deadlines_subscribed,deadlines_voted)

    return render_template("new_home.html", user_modules=student_deadline, avail_modules = avail, taking = user.module_taken, user=user, no_deadline=no_deadline_mod, hours = no_hours, access = session['access'], start = startdate_data(cw_startdate))

