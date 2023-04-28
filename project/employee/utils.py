# from flask_mail import Message
# from flask import url_for
from project import mail
from flask import current_app
import secrets,os
from flask import url_for, current_app
from flask_mail import Message

def save_picture(form_picture, old_picture=None):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/bills', picture_fn)

    # Delete the old picture if it exists
    if old_picture:
        old_picture_path = os.path.join(current_app.root_path, 'static/bills', old_picture)
        if os.path.exists(old_picture_path):
            os.remove(old_picture_path)

    form_picture.save(picture_path)
    return picture_fn

# def send_reset_email(user):
#     token = user.get_reset_index()
#     msg = Message('Password Reset Password',sender = 'noreplydemo.com',
#                 recipients= [user.email])
    
#     msg.body = f'''
#     To reset your passowrd, visit the following link:
#     {url_for('reset_token',token = token,_external=True)}
    
#     If you didn't make request then simply ignore this email and no change will be made.
#     '''
#     mail.send(msg)

def send_reset_email(employee):
    token = employee.get_reset_token_employee()
    msg = Message('Password Reset Request',
                sender='noreply@demo.com',
                recipients=[employee.email])
    msg.body = f'''
    To reset your password visit the follwing link:
    {url_for('employees.reset_token',token = token,_external=True)}
    '''
    mail.send(msg)
    
    