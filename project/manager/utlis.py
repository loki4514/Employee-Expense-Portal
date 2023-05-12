from project import mail
from flask import current_app,flash,Response
import secrets,os
from flask import url_for, current_app
from flask_mail import Message
import os,boto3,mimetypes


import base64
def get_picture(file_name):
    bucket_name = "flasklara"
    session = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name='ap-southeast-2'
    )
    s3 = session.client('s3')
    try:
        content_type = 'image/png' if file_name.endswith('.png') \
                                   else 'application/pdf' if file_name.endswith('.pdf') \
                                   else 'image/jpg'
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': file_name,
                'ResponseContentType': content_type
            },
        )
        return url
    except Exception as e:
        print(f"Error retrieving image from S3: {e}")
        return None
    
    
def send_reject(employee, expense):
    try:
        msg = Message('Mail Regarding Expense Request',
                    sender='noreply@demo.com',
                    recipients=[employee.email])
        msg.body = f'''

        Dear {employee.name},

        We regret to inform you that your expense request has been rejected. For more information on the rejection reason and to re-approve the request, please visit the employee portal.

        Your claim ID is {expense.claimid}, and the conveyance amount requested is {expense.amount}. Kindly note that the re-approval process may take up to a few working days.

        Thank you for your cooperation.

        '''
        mail.send(msg)
        
    except Exception as e:
        flash(f"An error occurred while sending email: {str(e)}, but the claim has been updated successfully.", 'error')
    
        
    


def send_accept(employee, expense):
    try:
        msg = Message('Mail Regarding Expense Request',
                        sender='noreply@demo.com',
                        recipients=[employee.email])

        msg.body = f'''
            Dear {employee.name},

            We are pleased to inform you that your expense request has been accepted. Please wait for a few working days to receive the conveyance amount requested.

            Your claim ID is {expense.claimid}, and the conveyance amount requested is {expense.amount}. Kindly note that the payment process may take up to a few working days.

            Thank you for your cooperation.
        '''
        mail.send(msg)
    except Exception as e:
        flash("An error occurred while sending email. Employee's claim has been submitted successfully.", 'warning')