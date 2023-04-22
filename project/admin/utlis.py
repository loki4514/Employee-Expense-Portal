from flask_mail import Message
from flask import url_for
from project import mail
from flask import current_app
def send_reset_email(user):
    token = user.get_reset_index()
    msg = Message('Password Reset Password',sender = 'noreplydemo.com',
                recipients= [user.email])
    
    msg.body = f'''
    To reset your passowrd, visit the following link:
    {url_for('reset_token',token = token,_external=True)}
    
    If you didn't make request then simply ignore this email and no change will be made.
    '''
    mail.send(msg)