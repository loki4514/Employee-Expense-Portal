from flask import Flask,render_template,flash,redirect,url_for
from forms import RegistrationForm,LoginForm,CreateEmployee
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SECRET_KEY'] = '8e7b334da419398c10724c396620c7c4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    name = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),unique=True,nullable=False)
    # image_file = db.Column(db.string(20),unique=True,nullable=False)
    
    def __repr__(self):
        return f"User('{self.username},{self.name},{self.email}')"
    
class Manager(db.Model):
    managerid = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    name = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),unique=True,nullable=False)
    
    def __repr__(self):
        return f"User('{self.username},{self.name},{self.email}')"
    
class Employee(db.Model):
    employeeid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    name = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),unique=True,nullable=False)
    role = db.Column(db.String(5),nullable=False,default="Employee")
    man_name = db.Column(db.String(30),unique=True,nullable=False)
    managerid = db.Column(db.Integer, db.ForeignKey('manager.managerid'), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username},{self.name},{self.email}')"
    

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
@app.route("/register", methods=["GET","POST"])
def register():
    # creating a registration form passing as an instance
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!",'success')
        return redirect(url_for('admin'))
    
    return render_template('register.html',title='Create Employee',form=form)

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

@app.route("/create",methods = ["GET","POST"])
def create():
    form = CreateEmployee()
    return render_template('create.html',title = "Create Employee",form = form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    