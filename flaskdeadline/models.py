
from flaskdeadline import db


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