"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, session
from FlaskWebProject1 import app
import FlaskWebProject1.db_handler as db


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    if session["logged_in"] is True:
        message = "Logged in!"
    else:
        message = "Logged out!"

    return render_template(
        'index.html',
        title='To Do',
        message=message,
        year=datetime.now().year,
    )


"""Beginning of login/register methods"""
@app.route('/login')
def login():
    """Renders the login page"""
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
    )


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # get form data
    email = request.form['email']
    password = request.form['password']

    # test credentials
    authenticated = db.check_credentials(email, password)

    if authenticated:
        # good credentials
        session["logged_in"] = True
        return home()
    
    # invalid credentials
    return render_template(
        "login.html",
        title="Login",
        error="Invalid email or password!",
        year=datetime.now().year
    )


@app.route('/register')
def register():
    """Renders the register page"""
    return render_template(
        'register.html',
        title='Register',
        year=datetime.now().year
    )


@app.route('/create_account', methods=['POST'])
def create_account():
    email = request.form['email']
    password = request.form['pass1']
    confirmation = request.form['pass2']

    # check if passwords match
    if password != confirmation:
        return render_template(
            'register.html',
            title='Register',
            error='Passwords did not match!',
            year=datetime.now().year
        )

    # check if user already exists
    if db.user_exists(email):
        return render_template(
            'register.html',
            title="Register",
            error="User already exists!",
            year=datetime.now().year
        )

    # insert user into database
    db.insert_user(email, password)

    # change session value
    session["logged_in"] = True

    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
"""End of login/register methods"""


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Azorel eschiuelul!',
        year=datetime.now().year,
        message='aici vor fi inregistrari'
    )
