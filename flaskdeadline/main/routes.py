from turtle import st
from flask import render_template, url_for,flash, redirect, request, session, make_response, Blueprint
from flaskdeadline import db, app
from flaskdeadline.models import Student, Lecturer, ACCESS
from flaskdeadline.onelogin.saml2.utils import OneLogin_Saml2_Utils
from flaskdeadline.utils import init_saml_auth, prepare_flask_request

main = Blueprint('main',__name__)


@main.route('/login')
def login():
    global user
    if session['samlNameId']:
        login_info = session['samlUserdata']
        id = login_info['urn:oid:0.9.2342.19200300.100.1.1'][0]
        email = login_info['urn:oid:0.9.2342.19200300.100.1.3'][0]
        name = login_info['urn:oid:2.5.4.4'][0] + ", " + login_info['urn:oid:2.5.4.42'][0]
        membership = login_info['urn:oid:1.3.6.1.4.1.5923.1.1.1.1']
        session['id'] = id
        session['name'] = name
        session['email'] = email
        if id == 'cht119' and email == 'chern.tan19@imperial.ac.uk':
            session['access'] = ACCESS['admin']
            return redirect(url_for('students.home'))
        if 'staff' in membership:
            check_staff= Lecturer.query.filter_by(id =id, name = name, email = email).first()
            session['access'] = ACCESS['staff']
            if not check_staff:
                staff = Lecturer(id=id, name = name, email = email)
                db.session.add(staff)
                db.session.commit()
            return redirect(url_for('teach.staff'))
        elif 'student' in membership:
            check_student= Student.query.filter_by(id =id, name = name, email = email).first()
            session['access'] = ACCESS['student']
            if not check_student:
                student = Student(id=id, name = name, email = email)
                db.session.add(student)
                db.session.commit()
            
    else:
        flash('User Not Logged In!', 'danger')
        return redirect(url_for('main.landing'))

    return redirect(url_for('students.home'))



@main.route('/', methods=['GET', 'POST'])
def landing():
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
        global login_info
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()
            return redirect(url_for('main.login'))

    return render_template(
        'index.html',
        errors=errors,
        error_reason=error_reason,
        not_auth_warn=not_auth_warn,
        success_slo=success_slo,
        attributes=attributes,
        paint_logout=paint_logout
    )




@main.route('/metadata/')
def metadata():
    if session['access'] != ACCESS['admin']:
        return redirect(url_for('students.home'))
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