
from project import db,user_login_manager
# ,emp_login_manager
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer
from project import emp_login_manager
from flask_login import UserMixin
# UserMixin 

# it handles user login,user logout and authencation in general it handles user login session
@user_login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@emp_login_manager.user_loader
def load_emp(employeeid):
    return Employee.query.get(employeeid)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    # image_file = db.Column(db.string(20),unique=True,nullable=False)
    
    def get_reset_index(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['user_id']
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
    
class Employee(db.Model,UserMixin):
    employeeid = db.Column(db.String(10),primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),unique=True,nullable=False)
    role = db.Column(db.String(5),nullable=False)
    man_name = db.Column(db.String(30),nullable=False)
    managerid = db.Column(db.String(10), nullable=False)
    
    # def get_id(self):
    #     return str(self.employeeid)
    
    
    
    def __repr__(self):
        return f"Employee('{self.name},{self.email},{self.role},{self.man_name},{self.managerid}')"
    
    
class Expense(db.Model):
    empid = db.Column(db.String(20),primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    picture = db.Column(db.LargeBinary, nullable=True)
    managerid = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    
    

    def __repr__(self):
        return f"Expense(empid={self.empid}, date={self.date}, amount={self.amount}, managerid={self.managerid}, status={self.status},picture = {self.picture})"