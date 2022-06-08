from flaskdeadline.models import db, Student, Module, Lecturer,Deadline, Coursework
import datetime
from dateutil.tz import gettz

db.drop_all()
db.create_all()
student_1 = Student(id = '01566453', name ='Andy', stream = 'EIE')
student_2 = Student(id = '01566454', name = 'John', stream = 'EEE')
student_3 = Student(id = '01566455', name = 'Carol', stream = 'EIE')
module_1 = Module(id='ELEC60004', title ='Artificial Intelligence', content = 'Jeremy Pitt')
module_2 = Module(id='ELEC60005', title ='Biomedical Electronics', content = 'Pantelis Georgiou')
module_3 = Module(id = 'ELEC60013', title = 'Embedded Systems', content='Edward Stott')
module_4 = Module(id='ELEC60006', title ='Communication Networks', content = 'Javier Barria')
module_5 = Module(id='ELEC60007', title ='Communication Systems', content = 'Athanassios Manikas')
module_6 = Module(id = 'ELEC60008', title = 'Control Engineering', content='Alessandro Astolfi')
module_7 = Module(id = 'ELEC60010', title = 'Digital Signal Processing', content='Tania Stathaki')
module_8 = Module(id='ELEC60019', title ='Machine Learning', content = 'Deniz Gunduz')
module_9 = Module(id='ELEC60021', title ='Mathematics for Signals and Systems', content = 'Pier-Luigi Dragotti')
lecturer_1 = Lecturer(id = '0425567', name ='Jeremy Pitt')
lecturer_2 = Lecturer(id = '0425568', name ='Edward Stott')
lecturer_3 = Lecturer(id = '0425569', name ='Javier Barria')
timezone_variable = gettz("Europe/London") 
deadline_1 = Deadline(coursework_id = 'Coursework 1', student_id = '01566453', module_id ='ELEC60005',lecturer_id = '', date = datetime.datetime(2022, 6, 17,12,0,0,0,timezone_variable), vote="Up")
deadline_2 = Deadline(coursework_id = 'Coursework 1', student_id = '01566454', module_id ='ELEC60006',lecturer_id = '', date = datetime.datetime(2022, 6, 19,12,0,0,0,timezone_variable),vote="Up")
deadline_3 = Deadline(coursework_id = 'Coursework 1', student_id = '01566453', module_id ='ELEC60006',lecturer_id = '', date = datetime.datetime(2022, 6, 18,12,0,0,0,timezone_variable),vote="Up")
deadline_4 = Deadline(coursework_id = 'Coursework 1', student_id = '', module_id ='ELEC60006',lecturer_id = '0425569', date = datetime.datetime(2022, 6, 18,12,0,0,0,timezone_variable),vote="Up")
deadline_5 = Deadline(coursework_id = 'Coursework 1', student_id = '01566453', module_id ='ELEC60006',lecturer_id = '', date = datetime.datetime(2022, 6, 19,12,0,0,0,timezone_variable),vote="Down")
hour1 = Coursework(module_id="ELEC60006", student_id="01566453",id="Coursework 1", hours="4")
hour2 = Coursework(module_id="ELEC60006", student_id="01566454",id="Coursework 1", hours="3")
hour3 = Coursework(module_id="ELEC60006", student_id="01566454",id="Coursework 2", hours="10")
db.session.add_all([student_1,student_2,student_3,module_1,module_2, module_3,module_4,module_5, module_6,module_7,module_8, module_9,lecturer_1, lecturer_2,lecturer_3,deadline_1,deadline_2,deadline_3,deadline_4, deadline_5,hour1,hour2,hour3])
db.session.commit()