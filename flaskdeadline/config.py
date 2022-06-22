import os


class Config:
    SECRET_KEY = '1e84d9bd36571efbeb07f9ec09c60022'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml')
    SESSION_COOKIE_SECURE=True
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE='Lax'
    WTF_CSRF_ENABLED = False