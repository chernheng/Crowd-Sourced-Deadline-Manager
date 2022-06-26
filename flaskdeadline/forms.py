
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, SelectField, IntegerField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from wtforms_components import DateRange
from datetime import datetime
from flaskdeadline.models import Student, Coursework
from flaskdeadline import db

academic_yr = 2022

class ModuleForm(FlaskForm):
    id = StringField('Module Code', validators=[DataRequired(), Length(min=9,max=9)])
    title = StringField('Name of Module', validators=[DataRequired()])
    coursework_title = StringField('Name of Coursework', description = 'Coursework 1', validators=[DataRequired()])
    ects = DecimalField('ECTS Credit',default=5, validators=[DataRequired(),NumberRange(min=0,max=35)])
    breakdown = IntegerField('% of Module (Out of 100%)',default=20, validators=[DataRequired(),NumberRange(min=0,max=100)])
    start_date = DateTimeField('Start Date of Coursework',format='%Y-%m-%dT%H:%M',default=datetime.utcnow())
    date = DateTimeField('Deadline of Coursework',format='%Y-%m-%dT%H:%M', validators=[DataRequired(), DateRange(min=datetime.utcnow(), max=datetime(academic_yr, 7, 1))])
    submit = SubmitField('Add Module')

class ResponsibilityForm(FlaskForm):
    id = StringField('Module Code', validators=[DataRequired(), Length(min=9,max=9)])
    title = StringField('Name of Module', validators=[DataRequired()])
    coursework_title = StringField('Name of Coursework', description = 'Coursework 1', validators=[DataRequired()])
    ects = DecimalField('ECTS Credit',default=5, validators=[DataRequired(),NumberRange(min=0,max=35)])
    breakdown = IntegerField('% of Module (Out of 100%)',default=20, validators=[DataRequired(),NumberRange(min=0,max=100)])
    start_date = DateTimeField('Start Date of Coursework',format='%Y-%m-%dT%H:%M',default=datetime.utcnow())
    date = DateTimeField('Deadline of Coursework',format='%Y-%m-%dT%H:%M', validators=[DataRequired(), DateRange(min=datetime.utcnow(), max=datetime(academic_yr, 7, 1))])
    submit = SubmitField('Add Module Responsibility')

class DeadlineForm(FlaskForm):
    id = StringField('Module Code', render_kw={'readonly': True})
    title = StringField('Name of Module', render_kw={'readonly': True})
    coursework_title = StringField('Name of Coursework', description = 'Coursework 1', validators=[DataRequired()])
    breakdown = IntegerField(' % of Module (Out of 100%) (Only if adding deadline for new coursework, else ignore)',default=20, validators=[DataRequired(),NumberRange(min=0,max=100)])
    date = DateTimeField('Deadline of Coursework',format='%Y-%m-%dT%H:%M', validators=[DataRequired(), DateRange(min=datetime.utcnow(), max=datetime(academic_yr, 7, 1))])
    start_date = DateTimeField('Start date of coursework (Only if adding deadline for new coursework, else ignore)',format='%Y-%m-%dT%H:%M',default=datetime.utcnow())
    submit = SubmitField('Add Module')

class BreakdownForm(FlaskForm):
    title = StringField('Name of Module', render_kw={'readonly': True})
    coursework_title = StringField('Name of Coursework', validators=[DataRequired()])
    breakdown = IntegerField('% of Module (Out of 100%)',default=20, validators=[DataRequired(),NumberRange(min=1,max=100)])
    start_date = DateTimeField('Start Date of Coursework',format='%Y-%m-%dT%H:%M',default=datetime.utcnow())
    submit = SubmitField('Edit Coursework Details')

def avail_students():      
    student = db.session.query(Student).all()
    return sorted([m.id + " - " + m.name for m in student])

def avail_cw():      
    cw = db.session.query(Coursework).all()
    choices = ['p']
    choices.append("---")
    return sorted(choices)

class GTAForm(FlaskForm):
    title = StringField('Name of Module', render_kw={'readonly': True})
    gta = SelectField('Select your GTA', choices=avail_students(), validators = [DataRequired()])
    submit = SubmitField('Add GTA')

class OptimisationForm(FlaskForm):
    c1 = SelectField('Module 1', choices=avail_cw(), validators = [DataRequired()])
    c2 = SelectField('Module 2', choices=avail_cw(), validators = [DataRequired()])
    c3 = SelectField('Module 3', choices=avail_cw())
    c4 = SelectField('Module 4', choices=avail_cw())
    c5 = SelectField('Module 5', choices=avail_cw())
    submit = SubmitField('Compare Modules')

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

