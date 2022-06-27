
from flaskdeadline import db
from datetime import datetime

ACCESS = {
    'student': 0,
    'staff': 1,
    'admin': 2
}
VOTE = {
    'Neutral': 0,
    'Up': 1,
    'Down': 2
}

take = db.Table('take', 
    db.Column('student_id', db.String(32), db.ForeignKey('student.id'), primary_key=True),
    db.Column('module_id', db.String(9), db.ForeignKey('module.id'), primary_key=True)
) # set to lower case

gta = db.Table('gta', 
    db.Column('module_id', db.String(9), db.ForeignKey('module.id'), primary_key=True),  
    db.Column('student_id',db.String(32), db.ForeignKey('student.id'), primary_key=True)
) # set to lower case

responsible = db.Table('responsible', 
    db.Column('lecturer_id', db.String(32), db.ForeignKey('lecturer.id'), primary_key=True),
    db.Column('module_id', db.String(9), db.ForeignKey('module.id'), primary_key=True)
) # set to lower case

class Deadline(db.Model):
    coursework_id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(32), db.ForeignKey("student.id"), nullable=True, primary_key=True)
    lecturer_id = db.Column(db.String(32), db.ForeignKey("lecturer.id"), nullable=True, primary_key=True)
    module_id = db.Column(db.String(9), db.ForeignKey("module.id"), nullable=False, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,primary_key=True, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint(coursework_id, student_id, lecturer_id, module_id, date),)

    student = db.relationship("Student", backref="student_vote")
    module = db.relationship("Module", backref="module_vote")
    lecturer = db.relationship("Lecturer", backref="lecturer_vote")
    vote = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Deadline('{self.student_id}', '{self.lecturer_id}', '{self.module}', '{self.module_id}','{self.coursework_id}', '{self.date}','{self.vote}')"


class Student(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    module_taken = db.relationship('Module',secondary = take, backref='student_taking',lazy='subquery')


    def __repr__(self):
        return f"Student('{self.id}', '{self.name}', '{self.email}')"


class Module(db.Model):
    id = db.Column(db.String(9), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ects = db.Column(db.Float, nullable=False,default=5.0)
    content = db.Column(db.Text, nullable=True)
    gta_responsible = db.relationship('Student', secondary = gta, backref='module_gta',lazy='subquery')

    def __repr__(self):
        return f"Modules('{self.title}', '{self.id}')"


# To calculate number of hours
class Hours(db.Model):
    coursework_title = db.Column(db.String(100), primary_key=True)
    student_id = db.Column(db.String(32), db.ForeignKey("student.id"), nullable=False, primary_key=True)
    module_id = db.Column(db.String(9), db.ForeignKey("module.id"), nullable=False, primary_key=True)
    hours = db.Column(db.Integer, nullable=False)
    expected = db.Column(db.Integer, nullable=False) # 1 is expected, 0 is less than expected, 2 is more than expected
    __table_args__ = (db.UniqueConstraint(coursework_title, student_id, module_id),)

    def __repr__(self):
        return f"Hours('{self.module_id}', '{self.coursework_title}', '{self.student_id}', '{self.hours}')"

class Coursework(db.Model):
    title = db.Column(db.String(100), nullable=False, primary_key=True)
    module_id = db.Column(db.String(9), db.ForeignKey("module.id"), nullable=False, primary_key=True)
    breakdown = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint(title, module_id),)
    module = db.relationship("Module", backref="module_cw",lazy='subquery')

    def __repr__(self):
        return f"Coursework('{self.module_id}', '{self.id}', '{self.title}', '{self.breakdown}')"


class Lecturer(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    module_responsible = db.relationship('Module',secondary = responsible, backref='lecturer_responsible',lazy='subquery')

    def __repr__(self):
        return f"Lecturer('{self.id}', '{self.name}')"

class Reliable(db.Model):
    coursework_title = db.Column(db.String(100), nullable=False, primary_key=True)
    module_id = db.Column(db.String(9), db.ForeignKey("module.id"), nullable=False, primary_key=True)
    lect = db.Column(db.Integer, nullable=False)
    majority = db.Column(db.Integer, nullable=False)
    vote = db.Column(db.Integer, nullable=False)
    gta = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint(coursework_title, module_id),)

    def __repr__(self):
        return f"Reliable('{self.module_id}', '{self.coursework_title}', '{self.date}', '{self.vote}')"