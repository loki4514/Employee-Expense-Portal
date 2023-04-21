from flask import render_template,flash,redirect,url_for,request,Response
from project.forms import RegistrationForm,LoginForm,CreateEmployee,EmpLoginForm,ExpenseForm
from project.forms import UpdateEmployee,DeleteForm,RequestRestForm,ResetPassword
from project import app,db,bcrypt,mail
from project.models import User,Employee,Expense
from flask_login import login_user,current_user,logout_user,login_required
import mimetypes
from flask_mail import Message
    

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/admin")
@login_required
def admin():
    return render_template('admin.html')


@app.route("/employee", methods=["GET", "POST"])
def employee():
    form = ExpenseForm()
    if form.validate_on_submit():
        # Process the form data
        expense = Expense.query.filter_by(empid='emp001').first()
        expense.date = form.date.data
        expense.amount = form.amount.data
        expense.picture = form.picture.data.read()
        expense.managerid = 'man001'
        expense.status = 'pending'
        db.session.commit()
        flash('Expense has been updated successfully!', 'success')
        return redirect(url_for('employee'))
    return render_template('employee.html', form=form)

import base64

@app.route("/manager")
def manager():
    expense = Expense.query.filter_by(managerid='man001').first()  # Retrieve the first expense record
    image_data = expense.picture
    
    mime_type = mimetypes.guess_type("image.jpg")[0]  # Replace "image.jpg" with the actual file name
    
    return Response(image_data, mimetype=mime_type)

# Create Employee details
@app.route("/register", methods=["GET","POST"])
def register():
    # creating a registration form passing as an instance

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User( name = form.name.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your Account created has been created !",'success')
        return redirect(url_for('login'))
    
    return render_template('register.html',title='Create Account',form=form)

@app.route("/update", methods=["GET", "POST"])
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
            return redirect(url_for("admin"))
        else:
            flash("Employee not found!", "error")
            return redirect(url_for("update"))

    return render_template("update.html", form=form)




@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect('next_page') if next_page else redirect(url_for('admin'))
        else:
            flash("Login unsucessful. Please check your email or password!!!")
    
    return render_template('login.html', title='Login', form=form)

@app.route("/emp",methods=["GET","POST"])
def emp():
    if current_user.is_authenticated:
        return redirect(url_for('employee'))
    form = EmpLoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(employeeid=form.employeeid.data).first()
        if employee and bcrypt.check_password_hash(employee.password, form.password.data):
            login_user(employee, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('employee'))
        else:
            flash('Login Unsuccessful. Please check Employee id and password', 'danger')
    return render_template('emp.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/create",methods = ["GET","POST"])
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
        return redirect(url_for('index'))
        
    return render_template('create.html',title = "Create Employee",form = form)

@app.route('/delete', methods=['POST','GET'])
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
        return redirect(url_for('admin'))
    return render_template('delete.html',title = 'Delete Employee',form = form)


def send_reset_email(user):
    token = user.get_reset_index()
    msg = Message('Password Reset Password',sender = 'noreplydemo.com',
                recipients= [user.email])
    
    msg.body = f'''
    To reset your passowrd, visit the following link:
    {url_for('reset_token',token = token,_external=True)}
    
    If you didn't make request then simply ignore this email and no change will be made.
    '''
    mail.send(msg)
    

@app.route("/reset_password",methods=["GET",'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # now we fetched the user from the database providing the user a passowrd rset link
        send_reset_email(user)
        flash('An Email has been sent with instruction to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password.html',title='Reset Password',form = form)

@app.route("/reset_password/<token>",methods=["GET",'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('reset_password'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Your Account created has been created !",'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',form = form)
