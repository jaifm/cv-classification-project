from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') #home route
def home():
    return render_template("index.html")
