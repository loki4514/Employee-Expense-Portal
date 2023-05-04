from flask import Blueprint,redirect,render_template,url_for,flash,request,session
from project import db,bcrypt
from project.models import Employee
from project.employee.forms import EmpLoginForm,ExpenseForm,UpdateExpenseForm,RequestRestForm,ResetPasswordForm
from project.models import Expense
from project.employee.utils import save_picture,send_reset_email,send_claimid_mail_emp,send_claimid_mail_manager
import random

employees = Blueprint('employees',__name__)


def generate_unique_claimid():
    """Generates a unique 7-digit number for the claimid attribute."""
    while True:
        claimid = random.randint(1000000, 9999999)
        if not Expense.query.filter_by(claimid=claimid).first():
            return claimid
        


@employees.route("/employee", methods=["GET", "POST"])
def employee():
    if 'employeeid' not in session:
        return redirect(url_for('employees.emp'))
    form = ExpenseForm()
    if form.validate_on_submit():
        # Process the form data
        claimid = generate_unique_claimid()
        expense = Expense(claimid = claimid,
        empid = session['employeeid'],
        date = form.date.data,
        amount = form.amount.data,
        image_file  = save_picture(form.image_file.data),
        managerid = session['managerid'])
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense has sent successfully!', 'success')
        employee = Employee.query.filter_by(employeeid = session['employeeid']).first()
        send_claimid_mail_emp(employee,expense)
        send_claimid_mail_manager(employee,expense)
        return redirect(url_for('employees.approve'))
    
    return render_template('employee.html', form=form)

@employees.route("/emp",methods=["GET","POST"])

def emp():
    form = EmpLoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(employeeid=form.employeeid.data).first()
        if employee and bcrypt.check_password_hash(employee.password, form.password.data):
            session["employeeid"] = employee.employeeid
            session["managerid"] = employee.managerid
            session['name'] = employee.name
            return redirect(url_for('employees.employee'))
        else:
            flash('Login Unsuccessful. Please check Employee id and password', 'danger')
    return render_template('emp.html', form=form)


@employees.route('/approve')
def approve():  # replace with the actual employee ID
    if 'employeeid' not in session:
        return redirect(url_for('employees.emp'))
    page = request.args.get('page',1,type=int)
    expenses = Expense.query.filter_by(empid=session["employeeid"]).order_by(Expense.status.desc()).paginate(page=page, per_page=10)
    # print(expenses)
    if expenses:
        status_list = [[str(expense.date),expense.amount,expense.status] for expense in expenses]
        # print(f'the status list is {status_list}')
        if "rejected" in status_list:
            return redirect(url_for('employees.rejected'))
    else: 
        flash("Not yet sent any requests for expense claims")
        return redirect(url_for('employees.employee'))
    return render_template('approve.html',status_list=status_list,expenses=expenses)

@employees.route("/rejected",methods=["GET","POST"])
def rejected():
    if 'employeeid' not in session:
        return redirect(url_for('employees.emp'))
    form = UpdateExpenseForm()
    expense = Expense.query.filter_by(empid=session["employeeid"], status="rejected").first()
    if expense and form.validate_on_submit():
        print(expense)
        if form.date.data:
            expense.date = form.date.data
        if form.amount.data:
            expense.amount = form.amount.data
        if form.image_file.data:
            expense.image_file = save_picture(form.image_file.data, expense.image_file)
        expense.status = 'pending'
        flash("Expense is updated successfully. Wait for the Manager Response")
        db.session.commit()
        return redirect(url_for('employees.approve'))
    elif request.method == 'GET':
        form.date.data = expense.date
        form.amount.data = expense.amount
        form.image_file.data = url_for('static', filename='bills/' + expense.image_file)
    return render_template('rejected.html', form=form, expense=expense)

# creating password reset form 
# requestform is use to send a request to the user for reset the email 
# resetpasswordform is used to reset the actual password 
    
@employees.route("/emp_reset_pass",methods=['GET','POST'])
# route that sends the request of email for reset the password 
def reset_request():
    if 'employeeid' in session:
        return redirect(url_for('employees.emp'))
    form = RequestRestForm()
    if form.validate_on_submit():
        emp = Employee.query.filter_by(email=form.email.data).first()
        send_reset_email(emp)
        flash('An email has been sent, for reset your password','info')
        return redirect(url_for('employees.emp'))
    return render_template('emp_request.html',title = 'Reset Password',form = form)

@employees.route("/emp_reset_pass/<token>",methods=['GET','POST'])
# same route racceots the token as parameter 
def reset_token(token):
    if 'employeeid' in session:
        return redirect(url_for('employees.emp'))
    emp = Employee.verify_reset_token_employee(token)
    if emp is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('employees.emp_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        emp.password = hashed_password
        db.session.commit()
        flash('Your Password has been update! You are now able to log in')
        return redirect(url_for('employees.emp'))
    return render_template('emp_token.html',title='Reset Password',form = form)
            
        
@employees.route("/logout")
def logout():
    
    session.pop("employeeid", None)
    session.pop("managerid", None)
    session.pop("name",None)
    session.clear()
    return redirect(url_for("main.index"))