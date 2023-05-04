from project import mail
from flask import current_app
import secrets,os
from flask import url_for, current_app
from flask_mail import Message


def send_reject(employee,expense):
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
    
def send_accept(employee,expense):
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