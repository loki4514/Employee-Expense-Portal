from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
# mail server i need



app = Flask(__name__)

app.config['SECRET_KEY'] = '8e7b334da419398c10724c396620c7c4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'register' # function name of our route 
login_manager.login_message_category = 'info'

# mail server and mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# setting env variable
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)




# emp_login_manager = LoginManager(app)
# emp_login_manager.login_view = 'emp' 
# emp_login_manager.login_message_category = 'info'


# login_manager_user = LoginManager()
# emp_login_manager = LoginManager()

# # associate each login manager with the appropriate blueprint
# login_manager_user.init_app(app)
# emp_login_manager.init_app(app)

# # specify the login view and message category for each login manager
# login_manager_user.login_view = 'register'
# login_manager_user.login_message_category = 'info'

# emp_login_manager.login_view = 'emp'
# emp_login_manager.login_message_category = 'info'

from project import routes