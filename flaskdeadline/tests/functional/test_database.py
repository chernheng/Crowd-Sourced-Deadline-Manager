
from flaskdeadline import app, db
from flaskdeadline.models import Student, Module, Lecturer, Deadline, Coursework


def test_subscribe():
    with app.test_client() as test_client:
        user = Student.query.filter_by(id='01566453').first()
        mod = Module.query.filter_by(id="ELEC60010").first()
        if mod in user.module_taken:
            response = test_client.get("/subscribed/ELEC60010")
            assert mod not in user.module_taken
        else:
            response = test_client.get("/subscribed/ELEC60010")
            assert mod in user.module_taken
        
        print(response.data)