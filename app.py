from flask import Flask,render_template


app = Flask(__name__)


posts = [
    
    {
        'author' : "abc",
        "no of post" : 1
    },
    {
        'author' : "jgj",
        "no of post" : 2
    }
    
]
@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/admin")
def admin():
    return render_template('admin.html',posts=posts)

@app.route("/employee")
def employee():
    return render_template('employee.html')

@app.route("/manager")
def manager():
    return render_template('manager.html')


if __name__ == '__main__':
    app.run(debug=True)
    