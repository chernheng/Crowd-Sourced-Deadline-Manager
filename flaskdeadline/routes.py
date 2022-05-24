
from flask import render_template, url_for, flash, redirect
from flaskdeadline import app, db
from markupsafe import escape
from flaskdeadline.models import Student, Module, Lecturer, Deadline
from flaskdeadline.forms import RegistrationForm, LoginForm
from sqlalchemy import tuple_, func

@app.route("/")
@app.route("/home")
def home():
    avail = Module.query.all()
    user = Student.query.filter_by(stream='EIE').first()
    check = [row.id for row in user.module_taken]
    # for x in user.module_taken:
    #     check.append(x.id)
    print(check)
    # deadline = Deadline.query.filter(Deadline.module_id.in_(check)).all()
    # unique = db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date).\
    # group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date).all()


    q = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date, func.count(Deadline.lecturer_id).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.in_(check)).all()
    t = {}
    for element in q:
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


@app.route('/subscribe/<string:module_id>')
def subscribe(module_id):
    user = Student.query.filter_by(stream='EIE').first()
    adding = Module.query.filter_by(id=module_id).first()
    print(user.module_taken)
    if adding in user.module_taken:
        user.module_taken.remove(adding)
    else:
        user.module_taken.append(adding)
    db.session.commit()
    return redirect(url_for('home'))

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
    return redirect(url_for('test'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            return redirect(url_for('test'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/test')
def test():
    avail = Module.query.all()
    user = Student.query.filter_by(stream='EIE').first()
    check = [row.id for row in user.module_taken]
    # for x in user.module_taken:
    #     check.append(x.id)
    print(check)
    # deadline = Deadline.query.filter(Deadline.module_id.in_(check)).all()
    # unique = db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date).\
    # group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date).all()


    q = (db.session.query(Deadline.coursework_id,Deadline.module_id,Deadline.date, func.count(Deadline.lecturer_id).label("# people"))
    .group_by(Deadline.coursework_id,Deadline.module_id,Deadline.date)
     ).filter(Deadline.module_id.in_(check)).all()
    t = {}
    for element in q:
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

    return render_template("new_home.html", user_modules=t, avail_modules = avail, taking = user.module_taken)