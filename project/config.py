import os
# here every configuration are stored here
class Config:
    SECRET_KEY = '8e7b334da419398c10724c396620c7c4'
    # app secret key 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # database so that 
    MAIL_SERVER =  'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')