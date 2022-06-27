
from flaskdeadline import app, db
from flaskdeadline.models import Student, Module, Lecturer, Deadline, Coursework, ACCESS, Hours
from datetime import datetime
from dateutil.tz import gettz

timezone_variable = gettz("Europe/London") 
def test_edit_module():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        user = Student.query.filter_by(id='cht119').first()
        response = test_client.post("/edit/Biomedical Electronics",data={
            'id' : "ELEC60005",
            "title": "test",
            "ects": "20"
        })
        # Checking the database
        mod = Module.query.filter_by(id="ELEC60005").first()
        assert mod.ects == 20
        assert mod.title == 'test'
        assert response.status_code == 302
        # reset the database
        mod.title = "Biomedical Electronics"
        mod.ects = 5
        db.session.commit()
   
def test_feedback():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response = test_client.post("/feedback/Communication Networks/Coursework 1",data={
            'module':'Communication Networks',
            'title':'Coursework 1',
            'hours' : "43",
            "expectation": "More than expected"
        })
        assert response.status_code == 302
        hours = Hours.query.filter_by(module_id = "ELEC60006",coursework_title = "Coursework 1", student_id = "cht119").first()
        assert hours.hours == 43
        assert hours.expected == 2     # hours.hours = 4
        hours.hours = 4
        hours.expected = 1
        db.session.commit()

def test_new_module():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response = test_client.post("/module/new",data={
            'id':'ELEC61234',
            'title':'TESTING',
            'coursework_title' : "TESTCW",
            "ects": "14.00",
            "breakdown" : "100",
            "start_date" : "2022-06-29T12:00",
            "date" : "2022-06-30T12:00",
        })
        assert response.status_code == 302
        mod = Module.query.filter_by(id="ELEC61234").first()
        cw = Coursework.query.filter_by(module_id = "ELEC61234", title = "TESTCW").first()
        deadline = Deadline.query.filter_by(module_id = "ELEC61234", coursework_id = "TESTCW").first()
        assert cw.breakdown == 100
        assert cw.start_date.date() == datetime(2022, 6, 29).date()
        assert mod.title == "TESTING"
        assert mod.ects == 14
        assert deadline.date.date() == datetime(2022, 6, 30).date()
        assert deadline.vote == "Up"
        db.session.delete(mod)
        db.session.delete(cw)
        db.session.delete(deadline)
        db.session.commit()

def test_edit_cw():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response = test_client.post("/cw/edit/Biomedical Electronics/Coursework 1",data={
            'title' : "Biomedical Electronics",
            "coursework_title": "Coursework 1",
            "breakdown": "41",
            "start_date": "2022-05-29T12:00"
        })
        # Checking the database
        cw = Coursework.query.filter_by(module_id = "ELEC60005", title = "Coursework 1").first()
        assert cw.breakdown == 41
        assert cw.start_date.date() == datetime(2022, 5, 29).date()
        assert response.status_code == 302
        # reset the database
        cw.breakdown = 10
        cw.start_date = datetime(2022, 5, 18,12,0,0,0,timezone_variable)
        db.session.commit()

def test_new_deadline():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response = test_client.post("/deadline/new/Biomedical Electronics",data={
            'id':'ELEC60005',
            'title':'Biomedical Electronics',
            'coursework_title' : "Coursework 2",
            "breakdown" : "100",
            "start_date" : "2022-06-29T12:00",
            "date" : "2022-06-30T12:00",
        })
        assert response.status_code == 302
        cw = Coursework.query.filter_by(module_id = "ELEC60005", title = "Coursework 2").first()
        deadline = Deadline.query.filter_by(module_id = "ELEC60005", coursework_id = "Coursework 2").first()
        assert cw.breakdown == 100
        assert cw.start_date.date() == datetime(2022, 6, 29).date()
        assert deadline.date.date() == datetime(2022, 6, 30).date()
        assert deadline.vote == "Up"
        db.session.delete(cw)
        db.session.delete(deadline)
        db.session.commit()

def test_staff_new_module():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']
        response = test_client.post("/staff/module/new",data={
            'id':'ELEC64321',
            'title':'TESTING_staff',
            'coursework_title' : "TESTCW_Staff",
            "ects": "14.00",
            "breakdown" : "100",
            "start_date" : "2022-06-29T12:00",
            "date" : "2022-06-30T12:00",
            "content": "TESTING TEXT"
        })
        mod = Module.query.filter_by(id="ELEC64321").first()
        cw = Coursework.query.filter_by(module_id = "ELEC64321", title = "TESTCW_Staff").first()
        deadline = Deadline.query.filter_by(module_id = "ELEC64321", coursework_id = "TESTCW_Staff").first()
        assert cw.breakdown == 100
        assert cw.start_date.date() == datetime(2022, 6, 29).date()
        assert mod.title == "TESTING_staff"
        assert mod.ects == 14
        assert mod.content == "TESTING TEXT"
        assert deadline.date.date() == datetime(2022, 6, 30).date()
        assert deadline.vote == "Up"
        assert response.status_code == 302
        db.session.delete(mod)
        db.session.delete(cw)
        db.session.delete(deadline)
        db.session.commit()


def test_staff_edit_cw():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']
        response = test_client.post("/staff/cw/edit/Biomedical Electronics/Coursework 1",data={
            'title' : "Biomedical Electronics",
            "coursework_title": "Coursework 1",
            "breakdown": "84",
            "start_date": "2022-05-28T12:00"
        })
        # Checking the database
        cw = Coursework.query.filter_by(module_id = "ELEC60005", title = "Coursework 1").first()
        assert cw.breakdown == 84
        assert cw.start_date.date() == datetime(2022, 5, 28).date()
        assert response.status_code == 302
        # reset the database
        cw.breakdown = 10
        cw.start_date = datetime(2022, 5, 18,12,0,0,0,timezone_variable)
        db.session.commit()

def test_staff_new_deadline():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']
        response = test_client.post("/staff/deadline/new/Communication Networks",data={
            'id':'ELEC60006',
            'title':'Communication Networks',
            'coursework_title' : "Coursework 34",
            "breakdown" : "99",
            "start_date" : "2022-06-29T14:00",
            "date" : "2022-06-30T14:00",
        })
        
        cw = Coursework.query.filter_by(module_id = "ELEC60006", title = "Coursework 34").first()
        deadline = Deadline.query.filter_by(module_id = "ELEC60006", coursework_id = "Coursework 34").first()
        assert cw.breakdown == 99
        assert cw.start_date.date() == datetime(2022, 6, 29).date()
        assert deadline.lecturer_id == "jbarria"
        assert deadline.date.date() == datetime(2022, 6, 30).date()
        assert response.status_code == 302
        assert deadline.vote == "Up"
        db.session.delete(cw)
        db.session.delete(deadline)
        db.session.commit()

def test_staff_edit_module():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']
        response = test_client.post("/staff/edit/Communication Networks",data={
            'id' : "ELEC60006",
            "title": "Communication Networks",
            "ects": "34",
            "content": "TESTING TESTING"
        })
        # Checking the database
        mod = Module.query.filter_by(id="ELEC60006").first()
        assert mod.ects == 34
        assert mod.content == "TESTING TESTING"
        assert response.status_code == 302
        # reset the database
        mod.content = ""
        mod.ects = 5
        db.session.commit()

def test_staff_schedule():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']
        response = test_client.post("/staff/scheduling",data={
            'c1' : "Biomedical Electronics - Coursework 1",
            "c2": "Communication Networks - Coursework 1",
            "c3": "Communication Networks - Coursework 2",
            "c4" : "---",
            "c5" : "---"
        })
        # Checking the database
        assert response.status_code == 200
        # reset the database

def test_schedule():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response_subscribe = test_client.get("/subscribed/ELEC60006")
        response_home = test_client.get("/home")
        assert response_home.status_code == 200
        assert response_subscribe.status_code == 302
        response = test_client.post("/scheduling",data={
            'c1' : "Biomedical Electronics - Coursework 1",
            "c2": "Communication Networks - Coursework 1",
            "c3": "---",
            "c4" : "---",
            "c5" : "Communication Networks - Coursework 2"
        })
        # Checking the database
        assert response.status_code == 200

def test_staff_gta():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']
        response = test_client.post("/staff/gta/Communication Networks",data={
            "title": "Communication Networks",
            "gta": "ep2917 - Poo, Andy",
        })
        # Checking the database
        mod = Module.query.filter_by(id="ELEC60006").first()
        gta = Student.query.filter_by(id="ep2917").first()
        assert gta in mod.gta_responsible 
        assert response.status_code == 302
        mod.gta_responsible.remove(gta)
        db.session.commit()
