from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,ValidationError
from wtforms import validators
class ManagerLoginForm(FlaskForm):
    managerid = StringField('Manager ID',validators=[DataRequired(),Length(2,20)])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    


class StatusForm(FlaskForm):
    status_choices = [
        ("", ""),
        ("Issue with Picture/File", "Issue with Picture/File"),
        ("Expired Date/Issue with the Date", "Expired Date/Issue with the Date"),
        ("Invalid Amount", "Invalid Amount"),
        ("Non Acceptance", "Non Acceptance")
    ]
    
    def validate_reason_for_rejection(form, field):
        if form.rejected.data and not field.data:
            raise ValidationError("Reason for rejection is required.")
    
    reason_for_rejection = SelectField(
        'Reason for rejection', default="", choices=status_choices
    )
    
    rejected = SubmitField('Reject')
    accepted = SubmitField('Accept')
    # submit_rejection = SubmitField('Submit Rejection')

    # def validate(self):
    #     if self.rejected.data and not self.reason_for_rejection.data:
    #         self.reason_for_rejection.errors.append('Reason for rejection is required.')
    #         return False
    #     return True

    
class DeleteAdmin(FlaskForm):
    email = StringField("Admin's Email",validators=[DataRequired(),Email()])
    submit = SubmitField("Delete Admin")