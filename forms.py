from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,EmailField
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
    
    