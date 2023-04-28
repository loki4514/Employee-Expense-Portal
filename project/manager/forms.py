from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length

class ManagerLoginForm(FlaskForm):
    managerid = StringField('Manager ID',validators=[DataRequired(),Length(2,20)])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    
    
class StatusForm(FlaskForm):
    rejected = SubmitField('Reject')
    accepted = SubmitField('Accept')