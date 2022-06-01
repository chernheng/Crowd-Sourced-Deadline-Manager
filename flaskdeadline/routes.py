
from gettext import npgettext
from sqlite3 import Date
from flask import render_template, url_for, flash, redirect, request, session, make_response
from flaskdeadline import app, db
from markupsafe import escape
from flaskdeadline.models import Student, Module, Lecturer, Deadline
from flaskdeadline.forms import RegistrationForm, LoginForm, ModuleForm, EditForm, DeadlineForm
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
    user = Lecturer.query.filter_by(id='0425569').first()
    mod = Module.query.filter_by(id='ELEC60006').first()
    user.module_responsible.append(mod)
    db.session.commit()
    mods = Deadline.query.all()
    print(user.module_responsible)
    print(mod.module_vote)
    if mod:
        print("yes")
    else:
        print("no")
    return render_template("index1.html")

@app.route('/<string:module>/<string:date>')
def change_deadline(module,date):
    user = Student.query.filter_by(stream='EIE').first()
    mod = Module.query.filter_by(title=module).first()
    to_change = Deadline.query.filter_by(student=user,module=mod).first()
    to_change.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    db.session.commit()
    return redirect(url_for('home'))

# @app.route('/subscribe/<string:module_id>')
# def subscribe(module_id):
#     user = Student.query.filter_by(stream='EIE').first()
#     adding = Module.query.filter_by(id=module_id).first()
#     print(user.module_taken)
#     if adding in user.module_taken:
#         user.module_taken.remove(adding)
#     else:
#         user.module_taken.append(adding)
#     db.session.commit()
#     return redirect(url_for('test'))

@app.route('/subscribed/<string:module_id>')
def subscribed(module_id):
    user = Student.query.filter_by(stream='EIE').first()
    adding = Module.query.filter_by(id=module_id).first()
    print(user.module_taken)
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

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

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
            module = Module(id = form.id.data, title = form.title.data)
            deadline = Deadline(coursework_id = form.coursework_title.data, student_id = user.id, module_id =form.id.data,lecturer_id = '', date = form.date.data)
            db.session.add(module)
            db.session.add(deadline)
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
        check_deadline = Deadline.query.filter_by(module_id=form.id.data,coursework_id=form.coursework_title.data,student_id=user.id).first()
        # If user already subscribe to a deadline
        if check_deadline:
            check_deadline.date = form.date.data
        else:
            deadline = Deadline(coursework_id = form.coursework_title.data, student_id = user.id, module_id =form.id.data,lecturer_id = '', date = form.date.data)
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
    all_deadlines_subscribed = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date, func.count(Deadline.lecturer_id).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.in_(check)).all()
    print(all_deadlines_subscribed)
    t = {}
    for element in all_deadlines_subscribed:
        mod = Module.query.filter_by(id=element[1]).first()
        modname = mod.title
        voted = False
        for vote in deadlines_voted:
            if vote.module_id == element[1] and vote.date == element[2] and vote.coursework_id == element[0]:
                voted = True
        if modname in t:
            temp = t[modname]
            if element[0] in t[modname]:
                temp = t[modname][element[0]]
                temp.append([element[2],element[3],voted])
                t[modname][element[0]] = sorted(temp, key = lambda x: x[1], reverse=True)
            else:
                t[modname][element[0]] = [[element[2],element[3],voted]]
        else:
            t[modname] = {element[0]:[[element[2],element[3],voted]]}
    
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

    return render_template("new_home.html", user_modules=t, avail_modules = avail, taking = user.module_taken, user=user, no_deadline=no_deadline_mod)




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
def index():
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

