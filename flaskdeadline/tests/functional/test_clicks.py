from flaskdeadline import app, db
from flaskdeadline.models import Student, Module, Lecturer, Deadline, Coursework, ACCESS
import datetime
from dateutil.tz import gettz

timezone_variable = gettz("Europe/London") 


def test_subscribe():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        user = Student.query.filter_by(id='cht119').first()
        mod = Module.query.filter_by(id="ELEC60010").first()
        if mod in user.module_taken:
            response = test_client.get("/subscribed/ELEC60010")
            assert mod not in user.module_taken
        else:
            response = test_client.get("/subscribed/ELEC60010")
            assert mod in user.module_taken
        
        print(response.data)


def test_vote_up():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        deadline = Deadline.query.filter_by(coursework_id = 'Coursework 1', student_id = 'cht119', module_id ='ELEC60005', date = datetime.datetime(2022, 6, 17,12,0,0,0,timezone_variable)).first()
        if deadline.vote == "Up":
            response = test_client.get("/Biomedical Electronics/Coursework 1/2022-06-17 12:00:00/up")
            assert deadline.vote == "Neutral"
        else:
            response = test_client.get("/Biomedical Electronics/Coursework 1/2022-06-17 12:00:00/up")
            assert deadline.vote == "Up"

def test_vote_down():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        deadline = Deadline.query.filter_by(coursework_id = 'Coursework 1', student_id = 'cht119', module_id ='ELEC60006', date = datetime.datetime(2022, 6, 18,12,0,0,0,timezone_variable)).first()
        if deadline.vote == "Down":
            response = test_client.get("/Communication Networks/Coursework 1/2022-06-18 12:00:00/down")
            assert deadline.vote == "Neutral"
        else:
            response = test_client.get("/Communication Networks/Coursework 1/2022-06-18 12:00:00/down")
            assert deadline.vote == "Down"

def test_staff_vote_up():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']
        deadline = Deadline.query.filter_by(coursework_id = 'Coursework 1', lecturer_id = 'jbarria', module_id ='ELEC60006', date = datetime.datetime(2022, 6, 18,12,0,0,0,timezone_variable)).first()
        if deadline.vote == "Up":
            response = test_client.get("/staff/Communication Networks/Coursework 1/2022-06-18 12:00:00/up")
            assert deadline.vote == "Neutral"
        else:
            response = test_client.get("/staff/Communication Networks/Coursework 1/2022-06-18 12:00:00/up")
            assert deadline.vote == "Up"

def test_staff_vote_down():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']
        deadline = Deadline.query.filter_by(coursework_id = 'Coursework 1', lecturer_id = 'jbarria', module_id ='ELEC60006', date = datetime.datetime(2022, 6, 18,12,0,0,0,timezone_variable)).first()
        if deadline.vote == "Down":
            response = test_client.get("/staff/Communication Networks/Coursework 1/2022-06-18 12:00:00/down")
            assert deadline.vote == "Neutral"
        else:
            response = test_client.get("/staff/Communication Networks/Coursework 1/2022-06-18 12:00:00/down")
            assert deadline.vote == "Down"