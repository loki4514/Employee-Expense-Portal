from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired,Length,Email

class ManagerLoginForm(FlaskForm):
    managerid = StringField('Manager ID',validators=[DataRequired(),Length(2,20)])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    


class StatusForm(FlaskForm):
    status_choices = [("Issue with Picture/File", "Issue with Picture/File"),
                    ("Expired Date/Issue with the Date", "Expired Date/Issue with the Date"),
                    ("Invalid Amount", "Invalid Amount")]
    
    
    reason_for_rejection = SelectField('Status', choices=status_choices)
    rejected = SubmitField('Reject')
    accepted = SubmitField('Accept')
    
    # def validate(self):
    #     if self.rejected.data and not self.reason_for_rejection.data:
    #         self.reason_for_rejection.errors.append('Reason for rejection is required.')
    #         return False
    #     return True

    
class DeleteAdmin(FlaskForm):
    email = StringField("Admin's Email",validators=[DataRequired(),Email()])
    submit = SubmitField("Delete Admin")