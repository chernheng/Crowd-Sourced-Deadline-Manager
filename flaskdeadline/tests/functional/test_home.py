
from flaskdeadline import create_app
ACCESS = {
    'student': 0,
    'staff': 1,
    'admin': 2
}

def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    app =create_app()
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response = test_client.get('/home')
        assert response.status_code == 200

def test_home_page_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    app =create_app()
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess['samlUserdata'] = True
            sess['id'] = 'cht119'
            sess['name'] = 'Tan, Chern'
            sess['email'] = 'chern.tan19@imperial.ac.uk'
            sess['access'] = ACCESS['student']
        response = test_client.post('/home')
        assert response.status_code == 405

def test_staff_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    app =create_app()

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']

        response = test_client.get('/staff')
        assert response.status_code == 200

def test_staff_page_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    app =create_app()
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session['samlUserdata'] = True
            session['id'] = 'jbarria'
            session['name'] = 'Javier Barria'
            session['email'] = 'j.barria@imperial.ac.uk'
            session['access'] = ACCESS['staff']

        response = test_client.post('/staff')
        assert response.status_code == 405

