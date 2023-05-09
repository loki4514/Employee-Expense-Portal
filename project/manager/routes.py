from flask import Blueprint,session,render_template,redirect,url_for,flash,request
from project import db,bcrypt
from project.manager.forms import ManagerLoginForm,StatusForm,DeleteAdmin
from project.models import Expense,Employee,User
import mimetypes
from project.manager.utlis import send_reject,send_accept
managers = Blueprint('managers',__name__)


import base64

@managers.route("/manager_login", methods=["GET", "POST"])
def manager_login():
    form = ManagerLoginForm()
    try:
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
    except Exception as e:
        flash(f"An error occurred while logging in ", 'danger')
    return render_template('manager_login.html', form=form)



@managers.route("/manager", methods=['GET', 'POST'])
def manager():
    if 'managerid' not in session:
        return redirect(url_for('managers.manager_login'))
    
    try:
        page = request.args.get('page', 1, int)
        expenses = Expense.query.filter_by(managerid=session['managerid'], status='pending').paginate(page=page, per_page=5)
        manager_list = [[str(expense.date), expense.amount, url_for('static', filename='bills/' + expense.image_file), expense.claimid] for expense in expenses]
        form = StatusForm()

        if form.validate_on_submit():
            claimid = request.form.get("claimid")
            expense = Expense.query.filter_by(claimid=claimid, managerid=session['managerid'], status='pending').first()
            if expense:
                employee = Employee.query.filter_by(employeeid=expense.empid).first()
                if form.accepted.data == True:
                    expense.status = "accepted"
                    send_accept(employee, expense=expense)
                elif form.rejected.data == True:
                    expense.status = "rejected"
                    expense.reason_for_rejection = form.reason_for_rejection.data
                    send_reject(employee, expense=expense)
                db.session.commit()
                flash("Expense status updated successfully.")
                return redirect(url_for("managers.manager"))
            else:
                flash("No response yet.")
                return redirect(url_for("managers.manager"))

        return render_template('manager.html',title = 'Expense Request', manager_list=manager_list, expenses=expenses, form=form)
        
    except Exception as e:
        flash("An error occurred. Please try again later str{e}.")
        print(str(e))
        return redirect(url_for("managers.manager"))


@managers.route("/delete_admin",methods = ["POST","GET"])
def delete_admin():
    if 'managerid' not in session:
        return redirect(url_for('managers.manager_login'))
    form = DeleteAdmin()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email = form.email.data).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                flash("An Admin deleted successfully",'success')
            else:
                flash("Admin not found, please check admin's email",'warning')
                return redirect(url_for('managers.delete_admin'))
        except Exception as e:
            flash("An error occurred while deleting the admin.", 'danger')
            return redirect(url_for('managers.delete_admin'))
    return render_template("delete_admin.html",form = form)


@managers.route("/logout")
def logout():
    session.pop("managerid", None)
    session.pop("name", None)
    session.clear()
    return redirect(url_for("managers.manager_login"))