
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, SelectField, IntegerField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from wtforms_components import DateRange
from datetime import datetime

academic_yr = 2022

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
    id = StringField('Module Code', validators=[DataRequired(), Length(min=9,max=9)])
    title = StringField('Name of Module', validators=[DataRequired()])
    coursework_title = StringField('Name of Coursework', description = 'Coursework 1', validators=[DataRequired()])
    ects = DecimalField('ECTS Credit',default=5, validators=[DataRequired(),NumberRange(min=0,max=35)])
    breakdown = IntegerField('% of Module (Out of 100%)',default=20, validators=[DataRequired(),NumberRange(min=0,max=100)])
    date = DateTimeField('Deadline of Coursework',format='%Y-%m-%dT%H:%M', validators=[DataRequired(), DateRange(min=datetime.utcnow(), max=datetime(academic_yr, 7, 1))])
    submit = SubmitField('Add Module')

class ResponsibilityForm(FlaskForm):
    id = StringField('Module Code', validators=[DataRequired(), Length(min=9,max=9)])
    title = StringField('Name of Module', validators=[DataRequired()])
    ects = DecimalField('ECTS Credit',default=5, validators=[DataRequired(),NumberRange(min=0,max=35)])
    submit = SubmitField('Add Module Responsibility')

class DeadlineForm(FlaskForm):
    id = StringField('Module Code', render_kw={'readonly': True})
    title = StringField('Name of Module', render_kw={'readonly': True})
    coursework_title = StringField('Name of Coursework', description = 'Coursework 1', validators=[DataRequired()])
    breakdown = IntegerField('If adding deadline for new coursework, please give the % of Module (Out of 100%)',default=20, validators=[DataRequired(),NumberRange(min=0,max=100)])
    date = DateTimeField('Deadline of Coursework',format='%Y-%m-%dT%H:%M', validators=[DataRequired(), DateRange(min=datetime.utcnow(), max=datetime(academic_yr, 7, 1))])
    submit = SubmitField('Add Module')

class BreakdownForm(FlaskForm):
    title = StringField('Name of Module', render_kw={'readonly': True})
    coursework_title = StringField('Name of Coursework', validators=[DataRequired()])
    breakdown = IntegerField('% of Module (Out of 100%)',default=20, validators=[DataRequired(),NumberRange(min=0,max=100)])
    submit = SubmitField('Edit Breakdown')

class GTAForm(FlaskForm):
    title = StringField('Name of Module', render_kw={'readonly': True})
    coursework_title = StringField('Name of Coursework', validators=[DataRequired()])
    breakdown = IntegerField('% of Module (Out of 100%)',default=20, validators=[DataRequired(),NumberRange(min=0,max=100)])
    submit = SubmitField('Edit Breakdown')

class EditForm(FlaskForm):
    id = StringField('Module ID', validators=[DataRequired(), Length(min=9,max=9)])
    title = StringField('Name of Module', validators=[DataRequired()])
    ects = DecimalField('ECTS Credit',default=5, validators=[DataRequired(),NumberRange(min=0,max=35)])
    submit = SubmitField('Edit Module')

class StaffEditForm(FlaskForm):
    id = StringField('Module ID', validators=[DataRequired(), Length(min=9,max=9)])
    title = StringField('Name of Module', validators=[DataRequired()])
    ects = DecimalField('ECTS Credit',default=5, validators=[DataRequired(),NumberRange(min=0,max=35)])
    content = TextAreaField('Details of Module', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Edit Module')

class FeedbackForm(FlaskForm):
    module = StringField('Name of Module', render_kw={'readonly': True})
    title = StringField('Name of Coursework', render_kw={'readonly': True})
    hours = IntegerField('Estimated number of hours spent on this Coursework', description = 'Round to the nearest integer', validators=[DataRequired(),NumberRange(min=0,max=120)])
    expectation = SelectField('Was the time taken more or less than expected?', choices = ["More than expected", "Less than expected", "Similar to my expectations"], validators = [DataRequired()])
    submit = SubmitField('Submit Feedback')
