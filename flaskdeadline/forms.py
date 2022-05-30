
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ModuleForm(FlaskForm):
    id = StringField('Module Code', validators=[DataRequired(), Length(9)])
    title = StringField('Name of Module', validators=[DataRequired()])
    coursework_title = StringField('Name of Coursework', description = 'Coursework 1', validators=[DataRequired()])
    date = DateTimeField('Deadline of Coursework',format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Add Module')

class DeadlineForm(FlaskForm):
    id = StringField('Module Code', render_kw={'readonly': True})
    title = StringField('Name of Module', render_kw={'readonly': True})
    coursework_title = StringField('Name of Coursework', description = 'Coursework 1', validators=[DataRequired()])
    date = DateTimeField('Deadline of Coursework',format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Add Module')

class EditForm(FlaskForm):
    id = StringField('Module ID', validators=[DataRequired(), Length(9)])
    title = StringField('Name of Module', validators=[DataRequired()])
    submit = SubmitField('Edit Module')