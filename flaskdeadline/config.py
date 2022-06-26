import os


class Config:
    SECRET_KEY = '1e84d9bd36571efbeb07f9ec09c60022'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml')
    SESSION_COOKIE_SECURE=True
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE='Lax'
    WTF_CSRF_ENABLED = False



# new_date = Deadline(title = "test", module_id = "ELEC60005", breakdown = 28, start_date = datetime.datetime(2022, 5,5,12,0,0,0,timezone_variable))
#         current_date = Deadline.query.filter_by(title = "Deadline 1", module_id = "ELEC60005").first()
#         current_date.breakdown = 100
#         current_date.start_date = datetime.datetime(2022, 1,1,12,0,0,0,timezone_variable)
#         db.session.add(new_date)
#         db.session.commit()
#         date = Deadline.query.filter_by(title = "test").first()
        
#         assert date.breakdown == 28
#         assert date.start_date.date() == datetime.datetime(2022, 5,5,12,0,0,0,timezone_variable).date()
#         assert current_date.breakdown== 100
#         assert current_date.start_date.date()== datetime.datetime(2022, 1,1,12,0,0,0,timezone_variable).date()
#         current_date.breakdown = 10
#         current_date.start_date = datetime.datetime(2022, 5, 18,12,0,0,0,timezone_variable)
#         db.session.delete(date)
#         db.session.commit()

