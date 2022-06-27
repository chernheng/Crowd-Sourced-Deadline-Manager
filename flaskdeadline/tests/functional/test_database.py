
from flaskdeadline import app, db
from flaskdeadline.models import Student, Module, Lecturer, Deadline, Coursework, ACCESS, Hours, Reliable
import datetime
from dateutil.tz import gettz

timezone_variable = gettz("Europe/London") 
def test_student():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        new_user = Student(id = 'test', name ='TEST', email = 'test@imperial.ac.uk')
        current_user = Student.query.filter_by(id='cht119').first()
        current_user.name = "TESTING_NAME"
        db.session.add(new_user)
        db.session.commit()
        student = Student.query.filter_by(id='test').first()
        
        assert student.name == 'TEST'
        assert student.email == 'test@imperial.ac.uk'
        assert current_user.name == "TESTING_NAME"
        current_user.name = "Tan, Chern"
        db.session.delete(student)
        db.session.commit()


def test_lecturer():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        new_lect = Lecturer(id = 'test', name ='TEST', email = 'test@imperial.ac.uk')
        current_user = Lecturer.query.filter_by(id='jbarria').first()
        current_user.name = "TESTING_NAME"
        db.session.add(new_lect)
        db.session.commit()
        lect = Lecturer.query.filter_by(id='test').first()
        
        assert lect.name == 'TEST'
        assert lect.email == 'test@imperial.ac.uk'
        assert current_user.name == "TESTING_NAME"
        current_user.name = "Javier Barria"
        db.session.delete(lect)
        db.session.commit()

def test_module():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        new_module = Module(id='ELEC61111', title ='TESTING',ects=34)
        current_module = Module.query.filter_by(id='ELEC60008').first()
        current_module.title = "TESTING_NAME"
        db.session.add(new_module)
        db.session.commit()
        module = Module.query.filter_by(id='ELEC61111').first()
        
        assert module.title == 'TESTING'
        assert module.ects == 34
        assert current_module.title == "TESTING_NAME"
        current_module.title = "Control Engineering"
        db.session.delete(module)
        db.session.commit()

def test_coursework():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        new_cw = Coursework(title = "test", module_id = "ELEC60005", breakdown = 28, start_date = datetime.datetime(2022, 5,5,12,0,0,0,timezone_variable))
        current_cw = Coursework.query.filter_by(title = "Coursework 1", module_id = "ELEC60005").first()
        current_cw.breakdown = 100
        current_cw.start_date = datetime.datetime(2022, 1,1,12,0,0,0,timezone_variable)
        db.session.add(new_cw)
        db.session.commit()
        cw = Coursework.query.filter_by(title = "test").first()
        
        assert cw.breakdown == 28
        assert cw.start_date.date() == datetime.datetime(2022, 5,5,12,0,0,0,timezone_variable).date()
        assert current_cw.breakdown== 100
        assert current_cw.start_date.date()== datetime.datetime(2022, 1,1,12,0,0,0,timezone_variable).date()
        current_cw.breakdown = 10
        current_cw.start_date = datetime.datetime(2022, 5, 18,12,0,0,0,timezone_variable)
        db.session.delete(cw)
        db.session.commit()

def test_take():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        current_user = Student.query.filter_by(id='cht119').first()
        current_module = Module.query.filter_by(id='ELEC60008').first()
        current_user.module_taken.append(current_module)
        db.session.commit()
        
        assert current_module in current_user.module_taken
        assert current_user in current_module.student_taking
        current_user.module_taken.remove(current_module)
        db.session.commit()

def test_responsible():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        current_user = Lecturer.query.filter_by(id='jbarria').first()
        current_module = Module.query.filter_by(id='ELEC60008').first()
        current_user.module_responsible.append(current_module)
        db.session.commit()
        
        assert current_module in current_user.module_responsible
        assert current_user in current_module.lecturer_responsible
        current_user.module_responsible.remove(current_module)
        db.session.commit()

def test_hours():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        new_hour = Hours(module_id="ELEC60005", student_id="ep2917",coursework_title="Coursework 1", hours=41, expected = 2)
        current_hour = Hours.query.filter_by(student_id="cht119",module_id="ELEC60006").first()
        current_hour.hours = 80
        current_hour.expected = 0
        db.session.add(new_hour)
        db.session.commit()
        hour = Hours.query.filter_by(module_id='ELEC60005', student_id="ep2917",coursework_title="Coursework 1").first()
        
        assert hour.hours == 41
        assert hour.expected == 2
        assert current_hour.hours == 80
        assert current_hour.expected == 0
        current_hour.hours = 4
        current_hour.expected = 1
        db.session.delete(hour)
        db.session.commit()

def test_reliable():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        new_reliable = Reliable(coursework_title = "Coursework 2", module_id = "ELEC60005", date = datetime.datetime(2022, 1, 1,12,0,0,0,timezone_variable),lect = True, majority = True, gta = True, vote = 41)
        current_reliable = Reliable.query.filter_by(coursework_title = "Coursework 1", module_id = "ELEC60005").first()
        current_reliable.vote = 300
        current_reliable.lect = False
        db.session.add(new_reliable)
        db.session.commit()
        reliable = Reliable.query.filter_by(coursework_title = "Coursework 2", module_id = "ELEC60005").first()
        
        assert reliable.vote== 41
        assert reliable.date.date() == datetime.datetime(2022, 1, 1,12,0,0,0,timezone_variable).date()
        assert current_reliable.vote == 300
        assert current_reliable.lect == False
        current_reliable.vote = 1
        current_reliable.lect = True
        db.session.delete(reliable)
        db.session.commit()

def test_gta():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        current_user = Student.query.filter_by(id='cht119').first()
        current_module = Module.query.filter_by(id='ELEC60008').first()
        current_user.module_gta.append(current_module)
        db.session.commit()
        
        assert current_module in current_user.module_gta
        assert current_user in current_module.gta_responsible
        current_user.module_gta.remove(current_module)
        db.session.commit()

def test_deadline():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        new_date = Deadline(coursework_id = 'TEST', student_id = 'cht119', module_id ='ELEC60006',lecturer_id = '', date = datetime.datetime(2022, 1, 1,12,0,0,0,timezone_variable),vote="Down")
        current_date = Deadline.query.filter_by(coursework_id = 'Coursework 1', student_id = 'cht119', module_id ='ELEC60006',vote= "Down").first()
        current_date.vote = "Up"
        db.session.add(new_date)
        db.session.commit()
        date = Deadline.query.filter_by(coursework_id = 'TEST').first()
        
        assert date.date.date() == datetime.datetime(2022, 1, 1,12,0,0,0,timezone_variable).date()
        assert date.vote == "Down"
        assert current_date.vote == "Up"
        current_date.vote = "Down"
        db.session.delete(date)
        db.session.commit()