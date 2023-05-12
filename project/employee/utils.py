# from flask_mail import Message
# from flask import url_for
from project import mail
from flask import current_app,flash
import secrets,os
from flask import url_for, current_app
from flask_mail import Message
import boto3

# def save_picture(form_picture, old_picture=None):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     bucket_name = "flasklara"
#     s3 = boto3.resource("s3")
#     picture_path = s3.Bucket(bucket_name).upload_fileobj(form_picture,picture_fn)
#     # picture_path = os.path.join(current_app.root_path, 'static/bills', picture_fn)

#     # Delete the old picture if it exists
#     if old_picture:
#         old_picture_path = os.path.join(current_app.root_path, 'static/bills', old_picture)
#         if os.path.exists(old_picture_path):
#             os.remove(old_picture_path)

#     form_picture.save(picture_path)
#     return picture_fn
def save_picture(form_picture, old_picture=None):
    # Generate a random filename
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    # Upload the picture to S3
    bucket_name = "flasklara"
    session = boto3.Session(
                    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                    region_name='ap-southeast-2')
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Key=picture_fn, Body=form_picture, ContentType=form_picture.content_type)

    # Delete the old picture if it exists
    if old_picture:
        bucket.delete_objects(Delete={"Objects": [{"Key": old_picture}]})

    return picture_fn

def send_reset_email(employee):
    try:
        token = employee.get_reset_token_employee()
        msg = Message('Password Reset Request',
                    sender='noreply@demo.com',
                    recipients=[employee.email])
        msg.body = f'''
To reset your password visit the follwing link :
{url_for('employees.reset_token',token = token,_external=True)}
        '''
        mail.send(msg)
    except Exception as e:
        # log the exception and display a user-friendly error message
        
        flash("An error occurred while sending the password reset email. Please try again later.")

    
def send_claimid_mail_emp(employee,expense):
    try:
        msg = Message('Mail Regarding Expense Request',
                    sender='noreply@demo.com',
                    recipients=[employee.email])

        msg.body = f'''

Dear {employee.name},

This is to inform you that your expense request has been successfully submitted. Please note that it is currently pending approval from the Manager.

Your claim ID is {expense.claimid}, and the conveyance amount requested is {expense.amount}. Kindly note that the approval process may take up to few working days.

Thank you for your cooperation.

'''
        mail.send(msg)
    except Exception as e:
        # Log the error
        print(f"An error occurred while sending email: {str(e)}")
        # Show a message to the user that the email couldn't be sent
        flash("An error occurred while sending email for an employee. Your claim has been submitted successfully.", 'warning')

def send_claimid_mail_manager(employee,expense):
    try:
        msg = Message('Mail Regarding Expense Request',
                        sender='noreply@demo.com',
                        recipients=[employee.manager_email]      ) #
    

        msg.body = f'''
Subject: Approval Needed for Employee Expense Request

Hey {employee.man_name},

Just wanted to give you a heads up that an employee has submitted an expense request that needs your approval. Here are the details:

Claim ID: {expense.claimid}
Date: {expense.date}
Amount: {expense.amount}

Can you please approve the request on the company website at your earliest convenience? Thanks a bunch!


Cheers,
Lara Capital Management   
'''
        mail.send(msg)
    except Exception as e:
        # Log the error

        # Show a message to the user that the email couldn't be sent
        flash("An error occurred while sending for an email for Manager. Your claim has been submitted successfully.", 'warning')

