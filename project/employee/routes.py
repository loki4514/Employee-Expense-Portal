from flask import Blueprint,redirect,render_template,url_for,flash,request
from flask_login import current_user,logout_user,login_user,login_required
from project import db,bcrypt
from project.models import Employee
from project.employee.forms import EmpLoginForm,ExpenseForm
from project.models import Expense

employees = Blueprint('employees',__name__)



@employees.route("/employee", methods=["GET", "POST"])
@login_required
def employee():
    form = ExpenseForm()
    if form.validate_on_submit():
        # Process the form data
        expense = Expense()
        expense.empid = current_user.employeeid
        expense.date = form.date.data
        expense.amount = form.amount.data
        expense.picture = form.picture.data.read()
        expense.managerid = current_user.managerid
        expense.status = 'pending'
        db.session.add(expense)
        db.session.commit()
        flash('Expense has been updated successfully!', 'success')
        return redirect(url_for('employees.employee'))
    return render_template('employee.html', form=form,user=current_user)

@employees.route("/emp",methods=["GET","POST"])

def emp():
    if current_user.is_authenticated:
        return redirect(url_for('employees.employee'))
    form = EmpLoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(employeeid=form.employeeid.data).first()
        if employee and bcrypt.check_password_hash(employee.password, form.password.data):
            login_user(employee, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('employees.employee'))
        else:
            flash('Login Unsuccessful. Please check Employee id and password', 'danger')
    return render_template('emp.html', form=form)


@employees.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('employee.index'))
