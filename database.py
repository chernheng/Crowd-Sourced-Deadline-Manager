from deadline import db, Student, Module

db.drop_all()
db.create_all()
student_1 = Student(id = '01566453', name ='Andy', stream = 'EIE')
student_2 = Student(id = '01566454', name = 'John', stream = 'EEE')
module_1 = Module(id='ELEC60004', title ='Artificial Intelligence', content = 'Jeremy Pitt')
module_2 = Module(id='ELEC60005', title ='Biomedical Electronics', content = 'Pantelis Georgiou')
embedded_system = Module(id = 'ELEC60013', title = 'Embedded Systems', content='Edward Stott')
db.session.add_all([student_1,student_2,module_1,module_2, embedded_system])
db.session.commit()