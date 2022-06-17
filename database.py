from flaskdeadline.models import db, Student, Module, Lecturer,Deadline, Coursework, Hours
import datetime
from dateutil.tz import gettz

db.drop_all()
db.create_all()
student_1 = Student(id = 'cht119', name ='Tan, Chern', email = 'chern.tan19@imperial.ac.uk')
student_2 = Student(id = 'wcc19', name = 'Chang, winnie', email = 'winnie.chang19@imperial.ac.uk')
student_3 = Student(id = 'ep2917', name = 'Pek Zhen Wen, Edwyn', email = 'edwyn.pek-zhen-wen18@imperial.ac.uk')
module_1 = Module(id='ELEC60004', title ='Artificial Intelligence', content = 'Jeremy Pitt')
module_2 = Module(id='ELEC60005', title ='Biomedical Electronics', content = 'Pantelis Georgiou')
module_3 = Module(id = 'ELEC60013', title = 'Embedded Systems', content='Edward Stott')
module_4 = Module(id='ELEC60006', title ='Communication Networks', content = 'Javier Barria')
module_5 = Module(id='ELEC60007', title ='Communication Systems', content = 'Athanassios Manikas')
module_6 = Module(id = 'ELEC60008', title = 'Control Engineering', content='Alessandro Astolfi')
module_7 = Module(id = 'ELEC60010', title = 'Digital Signal Processing', content='Tania Stathaki')
module_8 = Module(id='ELEC60019', title ='Machine Learning', content = 'Deniz Gunduz')
module_9 = Module(id='ELEC60021', title ='Mathematics for Signals and Systems', content = 'Pier-Luigi Dragotti')
lecturer_1 = Lecturer(id = 'jpitt', name ='Jeremy Pitt', email = 'j.pitt@imperial.ac.uk')
lecturer_2 = Lecturer(id = 'estott', name ='Edward Stott', email = 'ed.stott@imperial.ac.uk')
lecturer_3 = Lecturer(id = 'jbarria', name ='Javier Barria', email = 'j.barria@imperial.ac.uk')
lecturer_3.module_responsible.append(module_4)
module_2.gta_responsible.append(student_1)
timezone_variable = gettz("Europe/London") 
cw_1 = Coursework(title = "Coursework 1", module_id = "ELEC60005", breakdown = 10)
cw_2 = Coursework(title = "Coursework 1", module_id = "ELEC60006", breakdown = 20)
cw_3 = Coursework(title = "Coursework 2", module_id = "ELEC60006", breakdown = 20)
deadline_1 = Deadline(coursework_id = 'Coursework 1', student_id = 'cht119', module_id ='ELEC60005',lecturer_id = '', date = datetime.datetime(2022, 6, 17,12,0,0,0,timezone_variable), vote="Up")
deadline_2 = Deadline(coursework_id = 'Coursework 1', student_id = 'ep2917', module_id ='ELEC60006',lecturer_id = '', date = datetime.datetime(2022, 6, 19,12,0,0,0,timezone_variable),vote="Up")
deadline_3 = Deadline(coursework_id = 'Coursework 1', student_id = 'cht119', module_id ='ELEC60006',lecturer_id = '', date = datetime.datetime(2022, 6, 18,12,0,0,0,timezone_variable),vote="Up")
deadline_4 = Deadline(coursework_id = 'Coursework 1', student_id = '', module_id ='ELEC60006',lecturer_id = 'jbarria', date = datetime.datetime(2022, 6, 18,12,0,0,0,timezone_variable),vote="Up")
deadline_5 = Deadline(coursework_id = 'Coursework 1', student_id = 'cht119', module_id ='ELEC60006',lecturer_id = '', date = datetime.datetime(2022, 6, 19,12,0,0,0,timezone_variable),vote="Down")
deadline_5 = Deadline(coursework_id = 'Coursework 2', student_id = 'ep2917', module_id ='ELEC60006',lecturer_id = '', date = datetime.datetime(2022, 6, 20,12,0,0,0,timezone_variable),vote="Down")
hour1 = Hours(module_id="ELEC60006", student_id="cht119",coursework_title="Coursework 1", hours="4", expected = 1)
hour2 = Hours(module_id="ELEC60006", student_id="ep2917",coursework_title="Coursework 1", hours="3", expected = 0)
hour3 = Hours(module_id="ELEC60006", student_id="ep2917",coursework_title="Coursework 2", hours="10", expected =2)
db.session.add_all([student_1,student_2,student_3,module_1,module_2, module_3,module_4,module_5, module_6,module_7,module_8, module_9,lecturer_1, lecturer_2,lecturer_3,deadline_1,deadline_2,deadline_3,deadline_4, deadline_5,cw_1, cw_2,cw_3,hour1,hour2,hour3]) 
db.session.commit()
