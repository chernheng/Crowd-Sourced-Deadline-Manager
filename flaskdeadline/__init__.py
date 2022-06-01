
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '1e84d9bd36571efbeb07f9ec09c60022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flaskdeadline import routes, models