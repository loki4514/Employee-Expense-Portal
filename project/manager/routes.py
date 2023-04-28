from flask import Blueprint,session,render_template,redirect,url_for,flash,request
from project import db,bcrypt
from project.manager.forms import ManagerLoginForm,StatusForm
from project.models import Expense,Employee
import mimetypes
managers = Blueprint('managers',__name__)


import base64

@managers.route("/manager_login",methods = ["GET","POST"])
def manager_login():
    form = ManagerLoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(employeeid=form.managerid.data).first()
        if employee and employee.role == 'manager':
            if bcrypt.check_password_hash(employee.password, form.password.data):
                session['managerid'] = employee.employeeid
                session['name'] = employee.name
                return redirect(url_for('managers.manager'))
            else:
                flash("Please Check your Manager ID or Password",'danger')
        else:
            flash("Your are an employee only manager can access this page")
    return render_template('manager_login.html',form=form)


@managers.route("/manager",methods = ['GET','POST'])
def manager():
    expenses = Expense.query.filter_by(managerid=session['managerid'], status='pending').all()
    manager_list = [[str(expense.date),expense.amount,url_for('static', filename='bills/' + expense.image_file),expense.claimid] for expense in expenses]
    form = StatusForm()
    if form.validate_on_submit():
        claimid = request.form.get("claimid")
        expense = Expense.query.filter_by(claimid=claimid, managerid=session['managerid'], status='pending').first()
        if expense:
            if form.accepted.data  == True:
                expense.status = "accepted"
            elif form.rejected.data == True:
                expense.status = "rejected"
            db.session.commit()
            flash("Expense status updated successfully.")
            return redirect(url_for("managers.manager"))
        else:
            # flash("Invalid claim ID")
            flash("No Response yet")
            return redirect(url_for("managers.manager"))
        
    return render_template('manager.html', manager_list=manager_list,form = form)



@managers.route("/logout")
def logout():
    session.pop("managerid", None)
    session.pop("name", None)
    session.clear()
    return redirect(url_for("managers.manager_login"))