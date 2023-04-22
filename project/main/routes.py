from flask import Blueprint,render_template,request
main = Blueprint('main',__name__)

@main.route("/")
@main.route("/index")
def index():
    return render_template('index.html')
