from flask import Flask,render_template,flash,redirect,url_for
from forms import RegistrationForm,LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '8e7b334da419398c10724c396620c7c4'


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/employee")
def employee():
    return render_template('employee.html')

@app.route("/manager")
def manager():
    return render_template('manager.html')


# Create Employee details
@app.route("/create", methods=["GET","POST"])
def create():
    # creating a registration form passing as an instance
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!",'success')
        return redirect(url_for('admin'))
    
    return render_template('create.html',title='Create Employee',form=form)

@app.route("/update")
def update():
    
    return render_template('update.html')

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "abc" and  form.password.data == "1234":
            flash('Sucessfully logged in','success')
            return redirect(url_for('admin'))
        
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
            
    
    return render_template('login.html', title='Login', form=form)




if __name__ == '__main__':
    app.run(debug=True)
    