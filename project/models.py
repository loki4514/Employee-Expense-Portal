
from project import db,user_login_manager
# ,emp_login_manager
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer
# from project import emp_login_manager
from flask_login import UserMixin
# UserMixin 

# it handles user login,user logout and authencation in general it handles user login session
@user_login_manager.user_loader
def load_user(id):
    return User.query.get(id)

# @emp_login_manager.user_loader
# def load_emp(employeeid):
#     return Employee.query.get(employeeid)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    # image_file = db.Column(db.string(20),unique=True,nullable=False)
    
    # here serilaize the secret key which is valid for 30 minutes and many more
    def get_reset_index(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        # passing a secrete key and expiring time so that it return a token only accessed by user only
        return s.dumps({'user_id':self.id})
        # serialize the data in the form of bytes and transmit over the network 
    
    @staticmethod
    # token accepts as a parameter 
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token,max_age=300)['user_id']
        except:
            return None
        return User.query.get(id)
    
    def __repr__(self):
        return f"User('{self.id},{self.name},{self.email}')"
    
# class Manager(db.Model):
#     managerid = db.Column(db.Integer,primary_key = True)
#     username = db.Column(db.String(20),unique=True,nullable=False)
#     name = db.Column(db.String(20),nullable=False)
#     email = db.Column(db.String(20),unique=True,nullable=False)
#     password = db.Column(db.String(60),unique=True,nullable=False)
    
#     def __repr__(self):
#         return f"User('{self.username},{self.name},{self.email}')"
    
class Employee(db.Model):
    employeeid = db.Column(db.String(10),primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),unique=True,nullable=False)
    role = db.Column(db.String(5),nullable=False)
    man_name = db.Column(db.String(30),nullable=False)
    managerid = db.Column(db.String(10), nullable=False)
    
    # def get_id(self):
    #     return str(self.employeeid)
    def get_reset_token_employee(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.employeeid})
    
    @staticmethod
    def verify_reset_token_employee(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=300)['user_id']
        except:
            return "Maybe there is error in creating and loading the token"
        return Employee.query.get(user_id)
    
    
    def __repr__(self):
        return f"Employee('{self.employeeid},{self.name},{self.email},{self.role},{self.man_name},{self.managerid}')"
    
    
class Expense(db.Model):
    claimid = db.Column(db.String(20),primary_key = True,nullable = False)
    empid = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(20), nullable=False)
    managerid = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    


    def __repr__(self):
            return f"Expense(claimid = {self.claimid},empid={self.empid}, date={self.date},image file = {self.image_file}, amount={self.amount}, managerid={self.managerid}, status={self.status})"