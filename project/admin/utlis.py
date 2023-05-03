from flask_mail import Message
from flask import url_for
from project import mail
from flask import current_app
import random
import string
from datetime import datetime, timedelta
from flask import jsonify
import pyotp,base64

def send_reset_email(user):
    token = user.get_reset_index()
    msg = Message('Password Reset Password',sender = 'noreplydemo.com',
                recipients= [user.email])
    
    msg.body = f'''
    To reset your passowrd, visit the following link:
    {url_for('admins.reset_token',token = token,_external=True)}
    
    If you didn't make request then simply ignore this email and no change will be made.
    '''
    mail.send(msg)
    
# def generate_otp():
#     return ''.join(random.choices(string.digits, k=6))

# def save_otp(sendermail):
#     otp = generate_otp()
#     expiration = datetime.now() + timedelta(minutes=5)
#     # store the OTP, email, and expiration time in a database or a cache
#     # you can use SQLAlchemy or Redis, for example
#     # ...
    # return otp,expiration    

def send_otp_email(sendermail, companymail):
    totp = pyotp.TOTP(base64.b32encode(current_app.config['SECRET_KEY'].encode()))
    otp_code = totp.now()
    otp_cache = {'otp_cached': otp_code, 'creation_time': datetime.now()}
    
    # Set the OTP validity duration to 5 minutes
    otp_validity_duration = timedelta(minutes=5)
    
    # Add the OTP and its expiry time to your cache or database
    otp_cache['expiry_time'] = otp_cache['creation_time'] + otp_validity_duration
    
    msg = Message(subject='Your OTP for account registration', sender=sendermail, recipients=companymail)
    msg.body = f'''
    An account creation request has been raised by one of your HR Provide them this OTP: {otp_code}, or else simply ignore this mail.Note: This OTP is valid for 5 minutes only.
    '''
    
    mail.send(msg)
    
    # Return the OTP and its expiry time to be used for verification
    return otp_cache['otp_cached'], otp_cache['expiry_time']

    
