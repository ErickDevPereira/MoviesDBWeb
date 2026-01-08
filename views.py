from main import app
from flask import render_template, redirect, url_for, session, flash, get_flashed_messages
from forms import *
import db.conn as conn
import db.DML as dml
import db.DQL as dql
from werkzeug.security import generate_password_hash
from functools import wraps
from flask_dance.contrib.google import google
from utils import shuffle_str

def login_required(function):
    """
    Explanation: This is a decorator that must be applied over endpoints that
    require loggin to access some backend feature.
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return function(*args, **kwargs)
        return redirect(url_for('login'))
    
    return wrapper

@app.route('/sucess')
def success():
    """
    Definition of the endpoint that will allow us to access a success page.
    This page will be accessed after a succesfull registration.
    """
    return render_template('success.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """
    Definition of the endpoint that will deal with the login page.
    """
    msgs = get_flashed_messages()
    form = LoginForm()
    if form.validate_on_submit():
        DB = conn.my_connection()
        if dql.validate_user(DB, form.username.data, form.password.data):
            session['user_id'] = dql.get_id(DB, form.username.data) #Catches the id of the user that logged into the system.
            DB.close()
            return redirect(url_for('home', user_name = f'nickname={form.username.data}'))
        else:
            flash("This user doesn't exist or the password is wrong!")
            DB.close()
            return redirect(url_for('login'))
    fields = [form.username.errors, form.password.errors]
    return render_template('login.html', form = form, fields = fields, msgs = msgs)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """
    Definition of the endpoint that will deal with the registration page.
    """
    msgs = get_flashed_messages()
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        phone = form.phone.data
        email = form.email.data
        DB = conn.my_connection()
        if not dql.check_if_user_exists(DB, username):
            session['username'] = username
            session['email'] = email
            session['phone'] = phone
            dml.load_user(DB, username = username, password = generate_password_hash(password), email = email, phone = phone)
            DB.close()
        else:
            flash(f'The nickname "{username} has been used by someone"')
            DB.close()
            return redirect(url_for('register'))
        return redirect(url_for('success'))
    fields = [form.username.errors, form.password.errors, form.conf_password.errors, form.email.errors, form.phone.errors]
    return render_template('register.html', form = form, fields = fields, msgs = msgs)

@app.route('/home/<user_name>')
@login_required #Only logged user can access this page.
def home(user_name):
    """
    Definition of the endpoint that will give access to the home page. This is 
    exclusive for each user.
    """
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear() #Cleaning the session of the user. Now the user will be out of the system.
    return redirect(url_for('login'))

@app.route('/oauth_google')
def oauth_google():
    if google.authorized:
        response = google.get('/oauth2/v2/userinfo')
        data = response.json()
        DB = conn.my_connection()
        password = shuffle_str(data['id'])
        dml.load_user(DB, username = data['given_name'] + '_' + data['id'], password = password, email = data['email'], phone = None)
        DB.close()
        session['username'] = data['given_name'] + '_' + data['id']
        session['email'] = data['email']
        session['password'] = password
        return redirect(url_for('success'))
    return redirect(url_for('google.login'))