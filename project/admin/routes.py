from flask import (Blueprint,flash,render_template,url_for,redirect,request)
from flask_login import current_user,login_required,logout_user,login_user,login_manager,set_login_view
from project import db,bcrypt,user_login_manager
from project.models import User,Employee
from project.admin.forms import (RegistrationForm,RequestRestForm,LoginForm,
                                ResetPassword,CreateEmployee,UpdateEmployee,DeleteForm)
from project.admin.utlis import send_reset_email

admins = Blueprint('admins',__name__)


@admins.route("/admin/login")
@login_required
def admin():
    return render_template('admin.html')



# Create Employee details
@admins.route("/register", methods=["GET","POST"])
def register():
    # creating a registration form passing as an instance

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User( name = form.name.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your Account created has been created !",'success')
        return redirect(url_for('admins.login'))
    
    return render_template('register.html',title='Create Account',form=form)






@admins.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admins.admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admins.admin'))
        else:
            flash("Login unsucessful. Please check your email or password!!!")
    
    return render_template('login.html', title='Login', form=form)



@admins.route("/create",methods = ["GET","POST"])
def create():
    form = CreateEmployee()
    if form.validate_on_submit():
        hashed_password1 = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')
        employee = Employee(employeeid = form.employeeid.data,
                            name = form.name.data,email = form.email.data,
                            password = hashed_password1,
                            role = form.role.data,
                            man_name = form.man_name.data,
                            managerid = form.managerid.data)
        db.session.add(employee)
        db.session.commit()
        flash(f"Your Account created has been created !",'success')
        return redirect(url_for('main.index'))
        
    return render_template('create.html',title = "Create Employee",form = form)


@admins.route("/update", methods=["GET", "POST"])
def update():
    form = UpdateEmployee()

    if form.validate_on_submit():
        employee = Employee.query.filter_by(employeeid=form.employeeid.data).first()
        if employee:
            # update employee fields
            if form.name.data:
                employee.name = form.name.data
            if form.email.data:
                employee.email = form.email.data
            if form.role.data:
                employee.role = form.role.data
            if form.man_name.data:
                employee.man_name = form.man_name.data
            if form.managerid.data:
                employee.managerid = form.managerid.data
            db.session.commit()
            flash("Employee updated successfully!", "success")
            return redirect(url_for("admins.admin"))
        else:
            flash("Employee not found!", "error")
            return redirect(url_for("admins.update"))

    return render_template("update.html", form=form)


@admins.route('/delete', methods=['POST','GET'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(employeeid=form.employeeid.data).first()
        if employee:
            db.session.delete(employee)
            db.session.commit()
            flash('Employee deleted successfully!', 'success')
        else:
            flash('Employee not found!', 'error')
        return redirect(url_for('admins.admin'))
    return render_template('delete.html',title = 'Delete Employee',form = form)

    

@admins.route("/reset_password",methods=["GET",'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # now we fetched the user from the database providing the user a passowrd rset link
        send_reset_email(user)
        flash('An Email has been sent with instruction to reset your password')
        return redirect(url_for('admins.login'))
    return render_template('reset_password.html',title='Reset Password',form = form)

@admins.route("/reset_password/<token>",methods=["GET",'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('admins.reset_password'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Your Account created has been created !",'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',form = form)

@admins.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('admins.admin'))