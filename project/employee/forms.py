from flask_wtf import FlaskForm
from datetime import datetime,timedelta
from wtforms import StringField,BooleanField,PasswordField,SubmitField,DateField,FloatField,FileField,ValidationError
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_wtf.file import FileRequired, FileAllowed
from project.models import Employee

class EmpLoginForm(FlaskForm):
    employeeid = StringField('Employee ID',validators=[DataRequired(),Length(2,20)])
    remember = BooleanField('Remember Me')
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    
class ExpenseForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    image_file = FileField('Picture', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Submit')
    
    
    def validate_date(self, date):
        date_str = date.data.strftime('%Y-%m-%d')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        if date < today - timedelta(days=30) or date > today:
            raise ValidationError('Date must be within the last 30 days')
    
class UpdateExpenseForm(FlaskForm):
    date = DateField('Date')
    amount = FloatField('Amount')
    image_file = FileField('Picture', validators=[ FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Submit')
    
    
    def validate_date(self, date):
        date_str = date.data.strftime('%Y-%m-%d')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        if date < today - timedelta(days=30) or date > today:
            raise ValidationError('Date must be within the last 30 days')
    
class RequestRestForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Submit')
    
    def validate_email(self,email):
        emp = Employee.query.filter_by(email=email.data).first()
        if emp is None:
            raise ValidationError("Employee not exist. Please check your employee id")
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')