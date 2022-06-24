from flaskdeadline import app, db
from flaskdeadline.models import Student, Module, Lecturer, Deadline, Coursework, ACCESS


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
        response = test_client.get('/home')
        assert response.status_code == 200

def test_vote_down():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response = test_client.get('/home')
        assert response.status_code == 200

def test_staff_vote_up():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response = test_client.get('/home')
        assert response.status_code == 200

def test_staff_vote_down():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response = test_client.get('/home')
        assert response.status_code == 200