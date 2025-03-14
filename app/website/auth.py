from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login') #login route
def login():
    return "<p>Login</p>"

@auth.route('/logout') #logout route
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up') #sign-up route
def sign_up():
    return "<p>Sign Up</p>"