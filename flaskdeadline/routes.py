
from gettext import npgettext
from sqlite3 import Date
from xml.sax.xmlreader import AttributesImpl
from flask import render_template, url_for, flash, redirect, request, session, make_response
from flaskdeadline import app, db
from flaskdeadline.models import Student, Module, Lecturer, Deadline, Coursework, Hours
from flaskdeadline.forms import RegistrationForm, LoginForm, ModuleForm, EditForm, DeadlineForm, FeedbackForm
from sqlalchemy import update, func
from datetime import datetime
from flaskdeadline.onelogin.saml2.auth import OneLogin_Saml2_Auth
from flaskdeadline.onelogin.saml2.utils import OneLogin_Saml2_Utils


@app.route("/test")
def test():
    avail = Module.query.all()
    user = Student.query.filter_by(stream='EIE').first()
    check = [row.id for row in user.module_taken]
    # for x in user.module_taken:
    #     check.append(x.id)
    print(user.id)
    # deadline = Deadline.query.filter(Deadline.module_id.in_(check)).all()
    # unique = db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date).\
    # group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date).all()


    all_deadlines_subscribed = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date, func.count(Deadline.lecturer_id).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.in_(check)).all()
    t = {}
    for element in all_deadlines_subscribed:
        mod = Module.query.filter_by(id=element[1]).first()
        modname = mod.title + "/" + element[0]
        print(modname)
        if modname in t:
            temp = t[modname]
            temp.append((element[2],element[3]))
            t[modname] = temp
        else:
            t[modname] = [(element[2],element[3])]    
    
    print(t)
    # print(unique)
    # print(deadline)
    # print(user)
    # print(user.module_taken)

    # # deadline = Deadline.query.filter_by()
    # # student.module_taken.append(modules)
    # # student.module_taken.remove(modules)
    # # db.session.commit()
    # print(modules.student_taking)

    return render_template("home.html", user_modules=t, avail_modules = avail, taking = user.module_taken)

@app.route('/index1')
def index1():
    cw = Coursework.query.all()
    print(cw)
    cww = Coursework.query.filter_by(module_id='ELEC60006').first()
    print(cww)
    print(cww.module)
    mod = Module.query.filter_by(id='ELEC60006').first()
    print(mod.module_cw)
    print(cww.module.ects*cww.breakdown)
    # user.module_responsible.append(mod)
    # db.session.commit()
    all_cw = Coursework.query.all()
    print(all_cw[0].module.title)
    total_hours = db.session.query(func.avg(Hours.hours).label('average')).filter_by(coursework_title="Coursework 1",module_id="ELEC60006").all()
    # print(user.module_responsible)
    print(total_hours[0][0])
    # if mod:
    #     print("yes")
    # else:
    #     print("no")
    return render_template("index1.html")

@app.route('/<string:module>/<string:cw>/<string:date>/up')
def upvote_deadline(module,cw,date):
    user = Student.query.filter_by(stream='EIE').first()
    mod = Module.query.filter_by(title=module).first()
    to_change = Deadline.query.filter_by(student=user,module=mod,coursework_id=cw,date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).first()
    if to_change:
        if to_change.vote == "Up":
            to_change.vote = "Neutral"
        else:
            to_change.vote="Up"
    else:
        insert = Deadline(student_id = user.id, module_id=mod.id,coursework_id=cw,date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),vote="Up")
        db.session.add(insert)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/<string:module>/<string:cw>/<string:date>/down')
def downvote_deadline(module,cw,date):
    user = Student.query.filter_by(stream='EIE').first()
    mod = Module.query.filter_by(title=module).first()
    to_change = Deadline.query.filter_by(student=user,module=mod,coursework_id=cw,date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).first()
    if to_change:
        if to_change.vote == "Down":
            to_change.vote = "Neutral"
        else:
            to_change.vote = "Down"
    else:
        insert = Deadline(student_id = user.id, lecturer_id='',module_id=mod.id,coursework_id=cw,date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),vote="Down")
        db.session.add(insert)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/feedback/<string:module>/<string:cw>", methods=['GET', 'POST'])
def feedback(module,cw):
    form = FeedbackForm()
    mod = Module.query.filter_by(title=module).first()
    user = Student.query.filter_by(stream='EIE').first()
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
            check_hours.expectation = expectation
        else:
            new_hour = Hours(module_id=mod.id, student_id=user.id,coursework_title=cw, hours=form.hours.data, expected = expectation)
            db.session.add(new_hour)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('feedback.html', form=form, cw =cw_data)

@app.route('/subscribed/<string:module_id>')
def subscribed(module_id):
    user = Student.query.filter_by(stream='EIE').first()
    adding = Module.query.filter_by(id=module_id).first()
    if adding in user.module_taken:
        user.module_taken.remove(adding)
    else:
        user.module_taken.append(adding)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash('Login Successful', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html', form=form)

@app.route("/module/new", methods=['GET', 'POST'])
def new_mod():
    form = ModuleForm()
    user = Student.query.filter_by(stream='EIE').first()
    if form.validate_on_submit():
        check_id = Module.query.filter_by(id = form.id.data).first()
        check_title = Module.query.filter_by(title = form.title.data).first()
        if check_id or check_title:
            flash('Module already exists', 'danger')
        else:
            module = Module(id = form.id.data, title = form.title.data,ects=form.ects.data)
            cw = Coursework(title = form.coursework_title.data, module_id = form.id.data, breakdown = 10)
            deadline = Deadline(coursework_id = form.coursework_title.data, student_id = user.id, module_id =form.id.data,lecturer_id = '', date = form.date.data, vote = "Up")
            db.session.add_all([module,cw,deadline])
            db.session.commit()
            user.module_taken.append(module)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('create_mod.html', form=form)

@app.route("/deadline/new/<string:module_title>", methods=['GET', 'POST'])
def new_deadline(module_title):
    form = DeadlineForm()
    mod = Module.query.filter_by(title=module_title).first()
    user = Student.query.filter_by(stream='EIE').first()
    if form.validate_on_submit():
        # 2 checks: 1. User votes up on another deadline / 2. Deadline already exist and user voted already
        deadline_check1 = Deadline.query.filter_by(module_id=form.id.data,coursework_id=form.coursework_title.data,student_id=user.id,vote="Up").all()
        deadline_check2 = Deadline.query.filter_by(module_id=form.id.data,coursework_id=form.coursework_title.data,student_id=user.id, date = form.date.data).first()
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
        return redirect(url_for('home'))
    return render_template('new_deadline.html', form=form, mod=mod)

@app.route("/edit/<string:module_title>", methods=['GET', 'POST'])
def edit_mod(module_title):
    form = EditForm()
    mod = Module.query.filter_by(title=module_title).first()
    original_id = mod.id
    original_title = mod.title
    check_id = check_title = False
    if form.validate_on_submit():
        if original_title == form.title.data and original_id == form.id.data:
            return redirect(url_for('home'))
        if original_id != form.id.data:
            check_id = Module.query.filter_by(id = form.id.data).first()
        if original_title != form.title.data:
            check_title = Module.query.filter_by(title = form.title.data).first()
        if check_id or check_title:
            flash('Module ID or title already exists', 'danger')
        else:
            mod.title = form.title.data
            mod.id = form.id.data
            db.session.commit()
            stmt = update(Deadline).where(Deadline.module_id==original_id).values(module_id=form.id.data).execution_options(synchronize_session="fetch")
            db.session.execute(stmt)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('update_mod.html', form=form, mod =mod)

@app.route("/staff/module/new", methods=['GET', 'POST'])
def new_staff_mod():
    form = ModuleForm()
    user = Student.query.filter_by(stream='EIE').first()
    if form.validate_on_submit():
        check_id = Module.query.filter_by(id = form.id.data).first()
        check_title = Module.query.filter_by(title = form.title.data).first()
        if check_id or check_title:
            flash('Module already exists', 'danger')
        else:
            module = Module(id = form.id.data, title = form.title.data)
            deadline = Deadline(coursework_id = form.coursework_title.data, student_id = user.id, module_id =form.id.data,lecturer_id = '', date = form.date.data)
            db.session.add(module)
            db.session.add(deadline)
            user.module_taken.append(module)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('staff_mod.html', form=form, staff=True)

@app.route('/staff')
def staff():
    avail = Module.query.all()
    teacher = Lecturer.query.filter_by(id='0425569').first()

    # All modules responsible by the teacher
    staff_responsible = teacher.module_responsible


    Dead = Deadline.query.first()
    # Check which modules are taken by the teacher
    check = [row.id for row in teacher.module_responsible]

    # Deadlines that Lecturer voted for
    deadlines_voted = Deadline.query.filter_by(lecturer_id=teacher.id).all()
    print(deadlines_voted)
    
    # All deadlines subscribed by teacher
    all_deadlines_subscribed = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date, func.count(Deadline.lecturer_id).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.in_(check)).all()

    # All other deadlines not subscribed by teacher
    all_deadlines_else = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date, func.count(Deadline.lecturer_id).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.not_in(check)).all()

    teacher_mod = {}
    for element in all_deadlines_subscribed:
        mod = Module.query.filter_by(id=element[1]).first()
        modname = mod.title
        voted = False
        for vote in deadlines_voted:
            if vote.module_id == element[1] and vote.date == element[2] and vote.coursework_id == element[0]:
                voted = True
        if modname in teacher_mod:
            temp = teacher_mod[modname]
            if element[0] in teacher_mod[modname]:
                temp = teacher_mod[modname][element[0]]
                temp.append([element[2],element[3],voted])
                teacher_mod[modname][element[0]] = sorted(temp, key = lambda x: x[1], reverse=True)
            else:
                teacher_mod[modname][element[0]] = [[element[2],element[3],voted]]
        else:
            teacher_mod[modname] = {element[0]:[[element[2],element[3],voted]]}
    all_else_mod = {}
    for element in all_deadlines_else:
        mod = Module.query.filter_by(id=element[1]).first()
        modname = mod.title
        if modname in all_else_mod:
            temp = all_else_mod[modname]
            if element[0] in all_else_mod[modname]:
                temp = all_else_mod[modname][element[0]]
                temp.append([element[2],element[3]])
                all_else_mod[modname][element[0]] = sorted(temp, key = lambda x: x[1], reverse=True)
            else:
                all_else_mod[modname][element[0]] = [[element[2],element[3]]]
        else:
            all_else_mod[modname] = {element[0]:[[element[2],element[3]]]}
    
    print(all_else_mod)
    # print(unique)
    # print(deadline)
    # print(user)
    # print(user.module_taken)

    # # deadline = Deadline.query.filter_by()
    # # student.module_taken.append(modules)
    # # student.module_taken.remove(modules)
    # # db.session.commit()
    # print(modules.student_taking)

    return render_template("staff.html", teacher_deadlines=teacher_mod, avail_modules = avail, taking = teacher.module_responsible, user=teacher, all_else=all_else_mod, staff=True)



@app.route('/home')
def home():
    avail = Module.query.all()
    user = Student.query.filter_by(stream='EIE').first()
    Dead = Deadline.query.first()
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
    # deadline = Deadline.query.filter(Deadline.module_id.in_(check)).all()
    # unique = db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date).\
    # group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date).all()

    # Deadlines that student voted for
    deadlines_voted = Deadline.query.filter_by(student=user).all()
    print(deadlines_voted)

    # All deadlines subscribed by student
    all_deadlines_subscribed = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date,func.count(Deadline.vote).filter(Deadline.vote=="Up"),func.count(Deadline.vote).filter(Deadline.vote=="Down"),func.count(Deadline.vote).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.in_(check)).all()
    print(all_deadlines_subscribed)
    no_hours = {}
    all_cw = Coursework.query.all()
    print(all_cw[0].module.title)
    for cw in all_cw:
        avg_hrs = db.session.query(func.avg(Hours.hours).label('average')).filter_by(coursework_title=cw.title,module_id=cw.module_id).all()
        if cw.module.title in no_hours:
            no_hours[cw.module.title][cw.title] = avg_hrs[0][0]
        else:
            no_hours[cw.module.title] = {cw.title:avg_hrs[0][0]}
    print(no_hours)
    t = {}
    for element in all_deadlines_subscribed:
        mod = Module.query.filter_by(id=element[1]).first()
        modname = mod.title
        lect = mod.lecturer_responsible
        if lect:
            lect_deadline = Deadline.query.filter_by(lecturer_id=lect.id).all()
        else:
            lect_deadline = None
        data = [0] #[Did user vote, Did Lect vote, Is majority?]
        for vote in deadlines_voted:
            if vote.module_id == element[1] and vote.date == element[2] and vote.coursework_id == element[0]:
                if vote.vote == "Up":
                    data[0] = 1
                elif vote.vote == "Down":
                    data[0] = 2
        if lect_deadline:
            if lect_deadline.vote =="Up" and lect_deadline.date==element[2]:
                data.append(True)
            else:
                data.append(False)
        else:
            data.append(False)
        if element[3] > element[5]/2:
            data.append(True)
        else:
            data.append(False)
        if modname in t:
            temp = t[modname]
            if element[0] in t[modname]:
                temp = t[modname][element[0]]
                temp.append([element[2],element[3],element[4],data])
                t[modname][element[0]] = temp
            else:
                t[modname][element[0]] = [[element[2],element[3],element[4],data]]
        else:
            t[modname] = {element[0]:[[element[2],element[3],element[4],data]]}
    
    print(t)
    # print(unique)
    # print(deadline)
    # print(user)
    # print(user.module_taken)

    # # deadline = Deadline.query.filter_by()
    # # student.module_taken.append(modules)
    # # student.module_taken.remove(modules)
    # # db.session.commit()
    # print(modules.student_taking)

    return render_template("new_home.html", user_modules=t, avail_modules = avail, taking = user.module_taken, user=user, no_deadline=no_deadline_mod, hours = no_hours)



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


@app.route('/', methods=['GET', 'POST'])
def login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    error_reason = None
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False


    if 'sso' in request.args:
        return redirect(auth.login())
        # If AuthNRequest ID need to be stored in order to later validate it, do instead
        # sso_built_url = auth.login()
        # request.session['AuthNRequestID'] = auth.get_last_request_id()
        # return redirect(sso_built_url)
    elif 'sso2' in request.args:
        return_to = '%sattrs/' % request.host_url
        return redirect(auth.login(return_to))
    elif 'slo' in request.args:
        name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
        if 'samlNameId' in session:
            name_id = session['samlNameId']
        if 'samlSessionIndex' in session:
            session_index = session['samlSessionIndex']
        if 'samlNameIdFormat' in session:
            name_id_format = session['samlNameIdFormat']
        if 'samlNameIdNameQualifier' in session:
            name_id_nq = session['samlNameIdNameQualifier']
        if 'samlNameIdSPNameQualifier' in session:
            name_id_spnq = session['samlNameIdSPNameQualifier']

        return redirect(auth.logout(name_id=name_id, session_index=session_index, nq=name_id_nq, name_id_format=name_id_format, spnq=name_id_spnq))
    elif 'acs' in request.args:
        request_id = None
        if 'AuthNRequestID' in session:
            request_id = session['AuthNRequestID']

        auth.process_response(request_id=request_id)
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()
        if len(errors) == 0:
            if 'AuthNRequestID' in session:
                del session['AuthNRequestID']
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            session['samlNameIdFormat'] = auth.get_nameid_format()
            session['samlNameIdNameQualifier'] = auth.get_nameid_nq()
            session['samlNameIdSPNameQualifier'] = auth.get_nameid_spnq()
            session['samlSessionIndex'] = auth.get_session_index()
            self_url = OneLogin_Saml2_Utils.get_self_url(req)
            if 'RelayState' in request.form and self_url != request.form['RelayState']:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the request.form['RelayState'] is a trusted URL.
                return redirect(auth.redirect_to(request.form['RelayState']))
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()
    elif 'sls' in request.args:
        request_id = None
        if 'LogoutRequestID' in session:
            request_id = session['LogoutRequestID']
        dscb = lambda: session.clear()
        url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the url is a trusted URL.
                return redirect(url)
            else:
                success_slo = True
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()
            print(attributes)
            # return redirect(url_for('home'))

    return render_template(
        'index.html',
        errors=errors,
        error_reason=error_reason,
        not_auth_warn=not_auth_warn,
        success_slo=success_slo,
        attributes=attributes,
        paint_logout=paint_logout
    )





@app.route('/attrs/')
def attrs():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()

    return render_template('attrs.html', paint_logout=paint_logout,
                           attributes=attributes)


@app.route('/metadata/')
def metadata():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp

