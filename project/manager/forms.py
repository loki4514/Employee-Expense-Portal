from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,DateField,FloatField,FileField,ValidationError
from wtforms.validators import DataRequired,Length

class ManLoginForm(FlaskForm):
    managerid = StringField('Manager ID',validators=[DataRequired(),Length(2,20)])
    remember = BooleanField('Remember Me')
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')