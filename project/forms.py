from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField,EmailField,RadioField,DateField,FloatField,FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_wtf.file import FileRequired, FileAllowed
from project.models import User,Employee,Expense
from datetime import datetime,timedelta
from werkzeug.utils import secure_filename

class RegistrationForm(FlaskForm):
    name = StringField('Admin Name',validators=[DataRequired(),Length(2,100)])
    email = EmailField('Admin Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('Create Employee')
    

        
    def validate_email1(self,email):
        
        user = User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('Enter a valid email !')
    
    
class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(),Length(2,20)])
    remember = BooleanField('Remember Me')
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    
class EmpLoginForm(FlaskForm):
    employeeid = StringField('Employee ID',validators=[DataRequired(),Length(2,20)])
    remember = BooleanField('Remember Me')
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    
class ManLoginForm(FlaskForm):
    managerid = StringField('Manager ID',validators=[DataRequired(),Length(2,20)])
    remember = BooleanField('Remember Me')
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    
class CreateEmployee(FlaskForm):
    employeeid = StringField('Employee Id',validators=[DataRequired(),Length(2,10)])
    name = StringField('Employee Name',validators=[DataRequired(),Length(2,20)])
    email = EmailField('Employee Email',validators=[DataRequired(),Length(2,30)])
    password = PasswordField('Employee Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    role = RadioField('Employee Type', choices=[('employee', 'Employee'), ('manager', 'Manager')], validators=[DataRequired()])
    man_name = StringField('Manager Name',validators=[DataRequired(),Length(2,20)])
    managerid = StringField("Manager Id",validators=[DataRequired(),Length(2,20)])
    submit = SubmitField('Create Account')
    
    def validate_employeeid(self,employeeid):
        
        emp = Employee.query.filter_by(employeeid=employeeid.data).first() 
        if emp:
            raise ValidationError('That Username is taken')
    
    
        
    def validate_email2(self,email):
        
        emp = Employee.query.filter_by(email=email.data).first() 
        if emp:
            raise ValidationError('Enter a valid email !')
        
    def validate_Managerid(self,managerid):
        
        emp = Employee.query.filter_by(managerid = managerid.data).first() 
        if emp:
            raise ValidationError('That Username is taken')
        
        
class ExpenseForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    picture = FileField('Picture', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Submit')
    
    
    def validate_date(self, date):
        date_str = date.data.strftime('%Y-%m-%d')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        if date < today - timedelta(days=30) or date > today:
            raise ValidationError('Date must be within the last 30 days')

    # def validate_picture(self, picture):
    #     if picture.data:
    #         filename = secure_filename(picture.data.filename)
    #         if not any(filename.endswith(ext) for ext in ('.jpg', '.jpeg', '.png', '.gif')):
    #             raise ValidationError('Invalid file type')
    
class UpdateEmployee(FlaskForm):
    employeeid = StringField('Employee ID',validators=[DataRequired()])
    name = StringField('Employee Name')
    email = EmailField('Employee Email')
    role = RadioField('Employee Type', choices=[('employee', 'Employee'), ('manager', 'Manager')], validators=[DataRequired()])
    man_name = StringField('Manager Name')
    managerid = StringField("Manager Id")
    submit = SubmitField('Update Employee/Manager')
    
    # def validate_employeeid(self, employeeid):
    #     emp = Employee.query.filter_by(employeeid=employeeid.data).first()
    #     if emp and emp.employeeid != self.employeeid.data:
    #         raise ValidationError('That employee ID is taken')
    
    # def validate_email2(self,email):
        
    #     emp = Employee.query.filter_by(email=email.data).first() 
    #     if emp:
    #         raise ValidationError('Enter a valid email !')

    
    
    def validate_employeeid(self, employeeid):
        emp = Employee.query.filter_by(employeeid=employeeid.data).first()
        if emp and emp.employeeid != self.employeeid.data:
            raise ValidationError('That employee ID is taken')

    def validate_email(self, email):
        emp = Employee.query.filter_by(email=email.data).first()
        if emp and emp.email != self.email.data:
            raise ValidationError('Enter a valid email!')

    # def validate_managerid(self, managerid):
    #     emp = Employee.query.filter_by(managerid=managerid.data).first()
    #     if emp and emp.managerid != self.managerid.data:
    #         raise ValidationError('That manager ID is taken')
        
        
class DeleteForm(FlaskForm):
    employeeid = StringField('Employee ID',validators=[DataRequired()])
    submit = SubmitField('Delete Employee')
    
class RequestRestForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    submit = SubmitField('Reset Password Reset')
    
    def validate_email(self, email):
        emp = User.query.filter_by(email=email.data).first()
        if emp:
            raise ValidationError('Enter a valid email or Create an Account!')
        
        
class ResetPassword(FlaskForm):
    password = PasswordField('Employee Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    
    
