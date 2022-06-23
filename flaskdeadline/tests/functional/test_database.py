
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