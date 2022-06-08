
from flaskdeadline import app


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/home')
        assert response.status_code == 200

def test_home_page_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.post('/home')
        assert response.status_code == 405

