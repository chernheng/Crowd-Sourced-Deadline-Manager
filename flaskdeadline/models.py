
from flaskdeadline import db
from datetime import datetime


take = db.Table('take', 
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'), primary_key=True)
) # set to lower case

responsible = db.Table('responsible', 
    db.Column('lecturer_id', db.Integer, db.ForeignKey('lecturer.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'), primary_key=True)
) # set to lower case

class Deadline(db.Model):
    coursework_id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=True, primary_key=True)
    lecturer_id = db.Column(db.Integer, db.ForeignKey("lecturer.id"), nullable=True, primary_key=True)
    module_id = db.Column(db.String(9), db.ForeignKey("module.id"), nullable=False, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,primary_key=True, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint(coursework_id, student_id, lecturer_id, module_id, date),)

    student = db.relationship("Student", backref="student_vote")
    module = db.relationship("Module", backref="module_vote")
    vote = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Deadline('{self.student_id}', '{self.lecturer_id}', '{self.module}', '{self.module_id}','{self.coursework_id}', '{self.date}')"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    stream = db.Column(db.String(3), nullable=False)
    module_taken = db.relationship('Module',secondary = take, backref='student_taking')

    def __repr__(self):
        return f"Student('{self.id}', '{self.name}', '{self.stream}')"


class Module(db.Model):
    id = db.Column(db.String(9), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ects = db.Column(db.Float, nullable=False,default=5.0)
    content = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Modules('{self.title}', '{self.id}')"


# To calculate number of hours
class Hours(db.Model):
    coursework_title = db.Column(db.String(100), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False, primary_key=True)
    module_id = db.Column(db.String(9), db.ForeignKey("module.id"), nullable=False, primary_key=True)
    hours = db.Column(db.Integer, nullable=False)
    expected = db.Column(db.Integer, nullable=False) # 1 is expected, 0 is less than expected, 2 is more than expected
    __table_args__ = (db.UniqueConstraint(coursework_title, student_id, module_id),)

    def __repr__(self):
        return f"Hours('{self.module_id}', '{self.coursework_title}', '{self.student_id}', '{self.hours}')"

class Coursework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    module_id = db.Column(db.String(9), db.ForeignKey("module.id"), nullable=False)
    breakdown = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint(title, module_id),)
    module = db.relationship("Module", backref="module_cw")

    def __repr__(self):
        return f"Coursework('{self.module_id}', '{self.id}', '{self.title}', '{self.breakdown}')"


class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    module_responsible = db.relationship('Module',secondary = responsible, backref='lecturer_responsible')

    def __repr__(self):
        return f"Lecturer('{self.id}', '{self.name}')"
