from flask import Flask, render_template, url_for, redirect
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

take = db.Table('take', 
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'), primary_key=True)
) # set to lower case

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    stream = db.Column(db.String(3), unique=True, nullable=False)
    module_taken = db.relationship('Module',secondary = take, backref='student_taking')

    def __repr__(self):
        return f"Student('{self.id}', '{self.name}', '{self.stream}')"


class Module(db.Model):
    id = db.Column(db.String(9), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Modules('{self.title}', '{self.id}')"

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

# import flask

# app = flask.Flask(__name__)


# @app.route("/")
# def index():
#     return """
#     <a href="/login">Login with SimpleLogin</a>
#     """


if __name__ == "__main__":
    app.run(debug=True)