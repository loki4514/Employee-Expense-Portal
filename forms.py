from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo



class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(2,20)])
    name = StringField('username',validators=[DataRequired(),Length(2,100)])
    email = StringField('email',validators=[DataRequired(),Email])
    
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('password',validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('Create Employee')
    
    
class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(2,20)])
    remember = BooleanField('None')
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    
    