from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST']) #login route
def login():
    data = request.form
    return render_template("login.html", text="Login", user="User")

@auth.route('/logout') #logout route
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST']) #sign-up route
def sign_up():
    return render_template("sign_up.html")