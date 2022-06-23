
from flaskdeadline import app, db
from flaskdeadline.models import Student, Module, Lecturer, Deadline, Coursework, ACCESS


def test_add_module():
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        user = Student.query.filter_by(id='cht119').first()
        response = test_client.post("/edit/Biomedical Electronics",data={
            'id' : "ELEC61000",
            "title": "test",
            "ects": "20"
        })
        mod = Module.query.filter_by(id="ELEC61000").first()
        assert mod.ects == 20
        assert mod.title == 'test'
        assert response.status_code == 302
        mod.title = "Biomedical Electronics"
        db.session.commit()
   