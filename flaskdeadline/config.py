import os


class Config:
    SECRET_KEY = '1e84d9bd36571efbeb07f9ec09c60022'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')