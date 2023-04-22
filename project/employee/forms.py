from flask_wtf import FlaskForm
from datetime import datetime,timedelta
from wtforms import StringField,BooleanField,PasswordField,SubmitField,DateField,FloatField,FileField,ValidationError
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileRequired, FileAllowed

class EmpLoginForm(FlaskForm):
    employeeid = StringField('Employee ID',validators=[DataRequired(),Length(2,20)])
    remember = BooleanField('Remember Me')
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    
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
    
