
from flask import render_template, url_for, flash, redirect
from flaskdeadline import app, db
from markupsafe import escape
from flaskdeadline.models import Student, Module

@app.route("/")
@app.route("/home")
def home():
    modules =  Module.query.filter_by(id="ELEC60013").first()
    avail = Module.query.all()
    user = Student.query.filter_by(stream='EIE').first()
    print(user)
    print(avail)
    # student.module_taken.append(modules)
    # student.module_taken.remove(modules)
    # db.session.commit()
    print(modules.student_taking)

    return render_template("home.html", user_modules=user.module_taken, avail_modules = avail)


@app.route('/embedded')
def embedded():
    user = Student.query.filter_by(stream='EIE').first()
    adding = Module.query.filter_by(id="ELEC60013").first()
    print(user.module_taken)
    if adding in user.module_taken:
        user.module_taken.remove(adding)
    else:
        user.module_taken.append(adding)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'