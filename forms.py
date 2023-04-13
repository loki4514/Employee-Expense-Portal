from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,EmailField,RadioField
from wtforms.validators import DataRequired,Length,Email,EqualTo



class RegistrationForm(FlaskForm):
    username = StringField('User Name',validators=[DataRequired(),Length(2,20)])
    name = StringField('Employee Name',validators=[DataRequired(),Length(2,100)])
    email = EmailField('Employee Email',validators=[DataRequired(),Email()])
    
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('Create Employee')
    
    
class LoginForm(FlaskForm):
    username = StringField('User Name',validators=[DataRequired(),Length(2,20)])
    remember = BooleanField('Remember Me')
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    
class CreateEmployee(FlaskForm):
    employeeid = StringField('Employee Id',validators=[DataRequired(),Length(2,10)])
    name = StringField('Employee Name',validators=[DataRequired(),Length(2,20)])
    email = EmailField('Employee Email',validators=[DataRequired(),Length(2,30)])
    password = PasswordField('Employee Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo(password)])
    role = RadioField('Employee Type', choices=[('employee', 'Employee'), ('manager', 'Manager')], validators=[DataRequired()])
    man_name = StringField('Manager Name',validators=[DataRequired(),Length(2,20)])
    managerid = StringField("Manager Id",validators=[DataRequired(),Length(2,20)])
    submit = SubmitField('Create Account')