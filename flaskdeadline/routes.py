
from gettext import npgettext
from sqlite3 import Date
from flask import render_template, url_for, flash, redirect
from flaskdeadline import app, db
from markupsafe import escape
from flaskdeadline.models import Student, Module, Lecturer, Deadline
from flaskdeadline.forms import RegistrationForm, LoginForm, ModuleForm, EditForm, DeadlineForm
from sqlalchemy import update, func
from datetime import datetime


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

@app.route('/index')
def index():
    user = Student.query.filter_by(stream='EIE').first()
    mod = Module.query.filter_by(id='ELEC60010').first()

    mods = Deadline.query.all()
    print(mod)
    print(mod.module_vote)
    print(mods)
    if mod:
        print("yes")
    else:
        print("no")
    return render_template("index.html")

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


@app.route("/")
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



@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

