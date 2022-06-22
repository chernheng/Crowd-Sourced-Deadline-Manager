
from flaskdeadline import create_app, db
from flaskdeadline.models import Student, Module, Lecturer, Deadline, Coursework, ACCESS


def test_add_module():
    app =create_app()
    app.app_context().push() 
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        user = Student.query.filter_by(id='cht119').first()
        mod = Module.query.filter_by(id="ELEC60010").first()
        response = test_client.post("/edit/Biomedical Electronics",data={
            'id' : "ELEC61000",
            "title": "Biomedical Electronics",
            "ects": "20"
        })
        mod = Module.query.filter_by(id="ELEC61000").first()
        assert mod.ects == 20
        
        print(response.data)