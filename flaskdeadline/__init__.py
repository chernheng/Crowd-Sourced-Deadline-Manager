
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from werkzeug.datastructures import ImmutableDict

app = Flask(__name__)
jinja_options = ImmutableDict(
 extensions=[
  'jinja2.ext.autoescape', 'jinja2.ext.with_' #Turn auto escaping on
 ])

# Autoescaping depends on you
app.jinja_env.autoescape = True 

app.config['SECRET_KEY'] = '1e84d9bd36571efbeb07f9ec09c60022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml')
# app.config['WTF_CSRF_ENABLED'] = False
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flaskdeadline import models
from flaskdeadline.students.routes import students
from flaskdeadline.teach.routes import teach

app.register_blueprint(students)
app.register_blueprint(teach)
