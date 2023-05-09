from flask import (Blueprint,flash,render_template,url_for,redirect,request,session,make_response)
from flask_login import current_user,login_required,logout_user,login_user
from project import db,bcrypt
from project.models import User,Employee
from project.admin.forms import (RegistrationForm,RequestRestForm,LoginForm,VerifyForm,
                                ResetPassword,CreateEmployee,UpdateEmployee,DeleteForm)
from project.admin.utlis import send_otp_email,send_reset_email
from datetime import datetime
import pytz
# from datetime import datetime

# aware_datetime = datetime.now(pytz.utc)
# naive_datetime = aware_datetime.astimezone(pytz.utc).replace(tzinfo=None)

admins = Blueprint('admins',__name__)


@admins.route("/admin")
@login_required
def admin():
    return render_template('admin.html')



# Create Employee details

@admins.route("/register", methods=["GET", "POST"])
def register():
    form1 = RegistrationForm()
    try:
        if form1.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form1.password.data).decode('utf-8')
            user = User(name=form1.name.data, email=form1.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            # send the OTP to the user's email address
            # db.session.add(user)
            # db.session.commit()
            # email = form1.email.data
            otp, expiry_time = send_otp_email(user.email,['lokeshrk89@gmail.com'])
            # store the OTP and expiry time in the session
            session['otp'] = bcrypt.generate_password_hash(otp).decode('utf-8')
            session['expiry_time'] = expiry_time
            flash("An OTP has been sent to your email address")
            print(user)
            return redirect(url_for('admins.verify_email', user=user.email))
    except Exception as e:
        db.session.rollback()
        flash("Something went wrong. Please try again later.")
    return render_template('register.html', title='Create Account', form1=form1)



@admins.route('/verify_email/<user>', methods=['GET', 'POST'])
def verify_email(user):
    try:
        user = User.query.filter_by(email=user).first()
        if not user:
            flash("User not found.", 'danger')
            return redirect(url_for('admins.register'))

        otp = session.get('otp')
        expiry_time = session.get('expiry_time')
        form2 = VerifyForm()
        attempts = session.get('attempts', 0)

        if form2.validate_on_submit():
            if bcrypt.check_password_hash(session['otp'], form2.otp.data) and expiry_time > datetime.now(pytz.utc).astimezone(pytz.UTC):
                session.pop('otp', None)
                session.pop('expiry_time', None)
                session.pop('attempts', None)
                user.flag = True
                db.session.commit()
                flash("Account has been created!", 'success')
                return redirect(url_for('admins.login'))
            else:
                attempts += 1
                session['attempts'] = attempts
                if attempts >= 3:
                    db.session.delete(user)
                    db.session.commit()
                    flash("Maximum number of attempts exceeded. Account has been deleted.", 'danger')
                    return redirect(url_for('admins.register'))
                else:
                    flash(f"Invalid OTP. You have {3-attempts} attempts left.", 'danger')
        else:
            if expiry_time and expiry_time < datetime.now(pytz.utc).astimezone(pytz.UTC):
                db.session.delete(user)
                db.session.commit()
                flash("Verification code has expired. Account has been deleted.", 'danger')
                return redirect(url_for('admins.register'))

        return render_template('verify_email.html', title='Create Account',form2=form2)

    except Exception as e:
        flash("An error occurred while verifying email.", 'danger')
        return redirect(url_for('admins.register'))




@admins.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admins.admin'))
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data) and user.flag == True:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admins.admin'))
            else:
                flash("Login unsuccessful. Please check your email or password!!!")
    except Exception as e:
        flash(f"An error occurred while processing your request", 'danger')
    return render_template('login.html', title='Login', form=form)



@admins.route("/create", methods=["GET", "POST"])
def create():
    if not current_user.is_authenticated:
        return redirect(url_for("admins.login"))
    form = CreateEmployee()
    try:
        if form.validate_on_submit():
            hashed_password1 = bcrypt.generate_password_hash(password=form.password.data).decode("utf-8")
            employee = Employee(
                employeeid=form.employeeid.data,
                name=form.name.data,
                email=form.email.data,
                password=hashed_password1,
                role=form.role.data,
                man_name=form.man_name.data,
                managerid=form.managerid.data,
                manager_email = form.manager_email.data
            )
            db.session.add(employee)
            db.session.commit()
            flash("A new employee has been created!", "success")
            return redirect(url_for("admins.admin"))
    except Exception as e:
        flash(f"An error occurred while creating a new employee: {str(e)}", "danger")
    return render_template("create.html", title="Create Employee", form=form)


@admins.route("/update", methods=["GET", "POST"])
def update():
    if not current_user.is_authenticated:
        return redirect(url_for('admins.login'))
    form = UpdateEmployee()
    
    try:
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
                if form.manager_email.data:
                    employee.manager_email = form.manager_email.data    
            
                db.session.commit()
                flash("Employee updated successfully!", "success")
                return redirect(url_for("admins.admin"))
            else:
                flash("Employee not found!", "error")
                return redirect(url_for("admins.update"))
    except Exception as e:
        flash("An error occurred while updating employee details!", "error")
        return redirect(url_for("admins.update"))

    return render_template("update.html",title = 'Update Employee', form=form)



@admins.route('/delete', methods=['POST','GET'])
def delete():
    if not current_user.is_authenticated:
        return redirect(url_for('admins.login'))
    form = DeleteForm()
    if form.validate_on_submit():
        try:
            employee = Employee.query.filter_by(employeeid=form.employeeid.data).first()
            if employee:
                db.session.delete(employee)
                db.session.commit()
                flash('Employee deleted successfully!', 'success')
            else:
                flash('Employee not found!', 'error')
        except Exception as e:
            flash(f'An error occurred while deleting employee: {str(e)}', 'error')
        return redirect(url_for('admins.admin'))
    return render_template('delete.html',title='Delete Employee',form=form)




@admins.route("/reset_password",methods=["GET",'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            # sending the password reset email
            send_reset_email(user)
        except Exception as e:
            flash('An error occurred while sending the reset email. Please try again later.', 'error')
            return redirect(url_for('admins.reset_password'))
        flash('An email has been sent with instructions to reset your password. This email will be valid for 5 minutes.')
        return redirect(url_for('admins.login'))
    return render_template('reset_password.html',title='Reset Password',form = form)


@admins.route("/reset_password/<token>",methods=["GET",'POST'])
def reset_token(token):
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        user = User.verify_token(token)
        if user is None:
            flash('This is an invalid or expired token','warning')
            return redirect(url_for('admins.reset_password'))
        form = ResetPassword()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash(f"Your Password has been reset successfully!",'success')
            return redirect(url_for('admins.login'))
        return render_template('reset_token.html',title = 'Reset Password',form = form)
    except Exception as e:
        flash(f"An error occurred while resetting your password. Error details: {str(e)}")
        return redirect(url_for('admins.login'))

@admins.route("/logout")
def logout():
    logout_user()
    session.clear()
    session.pop('_flashes', None)  
    return redirect(url_for('main.index'))