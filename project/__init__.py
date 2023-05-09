from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
# mail server i need
from project.config import Config
from flask_migrate import Migrate


# app = Flask(__name__)
# app.config.from_object(Config)
# app.config['SECRET_KEY'] = '8e7b334da419398c10724c396620c7c4'
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'user.register' # function name of our route 
# login_manager.login_message_category = 'info'

# mail server and mail configuration
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# # setting env variable
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# mail = Mail(app)




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
# from project.main.routes import main
# from project.admin.routes import admin
# from project.employee.routes import employee
# from project.manager.routes import manager

# app.register_blueprint(main)
# app.register_blueprint(admin)
# app.register_blueprint(employee)
# app.register_blueprint(manager)


# login_manager = LoginManager(app)
# login_manager.login_view = 'user.register' # function name of our route 
# login_manager.login_message_category = 'info'
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
user_login_manager = LoginManager()
user_login_manager.login_view = 'admins.login'
user_login_manager.login_message_category = 'info'
# emp_login_manager = LoginManager()
# emp_login_manager.login_view = 'employees.emp'
# emp_login_manager.login_message_category = 'info'




mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    
    
    mail.init_app(app)
    
    

    # create login managers for admins and employees
    # user_login_manager = LoginManager()
    # user_login_manager.login_view = 'admins.login'
    # user_login_manager.login_message_category = 'info'

    # emp_login_manager = LoginManager()
    # emp_login_manager.login_view = 'employees.login'
    # emp_login_manager.login_message_category = 'info'

    # initialize login managers with app
    user_login_manager.init_app(app)
    # emp_login_manager.init_app(app)

    # import blueprints
    from project.main.routes import main
    from project.admin.routes import admins
    from project.employee.routes import employees
    from project.manager.routes import managers
    from project.errors.handlers import errors
    
    # register blueprints
    app.register_blueprint(main)
    app.register_blueprint(admins)
    app.register_blueprint(employees)
    app.register_blueprint(managers)
    app.register_blueprint(errors)

    # associate login managers with blueprints
    # user_login_manager.blueprint_login_views = {
    #     'admins': 'admins.login'
    # }
    # emp_login_manager.blueprint_login_views = {
    #     'employees': 'employees.emp'
    # }
    # @app.after_request
    # def add_header(response):
    #     response.headers['Cache-Control'] = 'no-store'
    #     return response
    
    
    return app

