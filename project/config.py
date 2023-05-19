import os
# here every configuration are stored here
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # app secret key 
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # database so that 
    MAIL_SERVER =  'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')