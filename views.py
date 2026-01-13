from main import app
from flask import render_template, redirect, url_for, session, flash, get_flashed_messages
from forms import *
import db.conn as conn
import db.DML as dml
import db.DQL as dql
from werkzeug.security import generate_password_hash
from functools import wraps
from flask_dance.contrib.google import google
from utils import shuffle_str, Status, Vote
from data_handling import get_data_by_title, get_title_by_imdb_from_api
import mysql.connector as MySQL

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
    if 'password' in session:
        info = {'username': session['username'], 'email': session['email'], 'password': session['password']}
        signal = 'Google'
    else:
        info = {'username': session['username'], 'email': session['email'], 'phone' : session['phone']}
        signal = 'Regular'
    session.clear()
    return render_template('success.html', signal = signal, info = info)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """
    Definition of the endpoint that will deal with the login page.
    """
    session['pre_home'] = True
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
    session['pre_home'] = True
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

@app.route('/home/<user_name>', methods = ['GET', 'POST'])
@login_required #Only logged user can access this page.
def home(user_name):
    """
    Definition of the endpoint that will give access to the home page. This is 
    exclusive for each user.
    """
    msg_response = get_flashed_messages()
    session['pre_home'] = False
    form = SearchMovieForm()
    DB = conn.my_connection()
    all_movies = dql.get_movies_by_user(DB, session['user_id'])
    number_of_movies = len(all_movies)
    information = dql.get_by_id(DB, session['user_id'])
    if form.validate_on_submit():
        session["movie"] = get_data_by_title(form.title.data)
        searched_movie = session["movie"]
    else:
        searched_movie = 'None'
    DB.close()
    return render_template('home.html',
                            information = information,
                            form = form,
                            searched_movie = searched_movie,
                            msg_response = msg_response,
                            all_movies = all_movies,
                            number_of_movies = number_of_movies)

@app.route('/logout')
def logout():
    session.clear() #Cleaning the session of the user. Now the user will be out of the system.
    return redirect(url_for('login'))

@app.route('/oauth_google')
def oauth_google():
    session['pre_home'] = True
    if google.authorized:
        response = google.get('/oauth2/v2/userinfo')
        data = response.json()
        username = data['given_name'] + '_' + data['id']
        DB = conn.my_connection()
        if not dql.check_if_user_exists(DB, username):
            password = shuffle_str(data['id'])
            dml.load_user(DB,
                        username = username,
                        password = generate_password_hash(password),
                        email = data['email'],
                        phone = None)
            DB.close()
            session['username'] = username
            session['email'] = data['email']
            session['password'] = password
            return redirect(url_for('success'))
        else:
            flash('The user given throughout Google already exists!')
            DB.close()
            return redirect(url_for('login'))
    return redirect(url_for('google.login'))

@app.route('/movie/<title>', methods = ['GET', 'POST'])
@login_required
def movie(title):
    complete_data = get_data_by_title(title)
    DB = conn.my_connection()
    information = dql.get_by_id(DB, session['user_id'])
    username = f'nickname={information["username"]}'
    
    if complete_data is None:
        DB.close()
        return render_template('movie_not_found.html', title = title, information = information, username = username)

    img = complete_data['Image']
    user_has_movie = dql.user_has_movie(DB, user_id = session['user_id'], title = title)
    imdb = complete_data['imdbID']
    form = CommentForm()

    if form.validate_on_submit():
        dml.load_comment(DB, user_id = session['user_id'], text = form.comment.data, imdb_id = imdb)
    
    comments = dql.get_comment_by_imdb(DB, imdb_id = imdb)

    for comment in comments:
        comment['up'] = dql.votes_per_comment(DB, comment_id = comment['comment_id'], option = 1)
        comment['down'] = dql.votes_per_comment(DB, comment_id = comment['comment_id'], option = 0)
        comment['is_up'] = dql.user_has_upvoted(DB, comment_id = comment['comment_id'], user_id = session['user_id'])
        comment['is_down'] = dql.user_has_downvoted(DB, comment_id = comment['comment_id'], user_id = session['user_id'])

    DB.close()
    return render_template('movie.html',
                            complete_data = complete_data,
                            img = img,
                            information = information,
                            username = username,
                            user_has_movie = user_has_movie,
                            imdb = imdb,
                            form = form,
                            comments = comments)

@app.route('/movie/add_a_movie')
@login_required
def add_movie():
    DB = conn.my_connection()
    try:
        username = dql.get_by_id(DB, session['user_id'])['username']
        my_movie = session['movie']
        dml.load_movie(DB,
                    imdb_id= my_movie['imdbID'],
                    user_id = session['user_id'],
                    title = my_movie['Title'],
                    release_date = my_movie['Released'],
                    runtime = my_movie['Runtime'],
                    genre = my_movie['Genre'],
                    director = my_movie['Director'],
                    writer = my_movie['Writer'],
                    actors = my_movie['Actors'],
                    description = my_movie['Description'],
                    imdbRating= my_movie['imdbRating'],
                    type_ = my_movie['Type'])
        flash(f'The movie "{my_movie['Title']}" was added to your list successfully')
        flash(str(Status.SUCCESS.value)) #This string won't be shown on HTML, but will give a context on the frontend.
    except MySQL.errors.IntegrityError as err:
        flash(f'The movie "{my_movie["Title"]}" is already inside your list, so you can\'t insert it again!')
        flash(str(Status.DUPLICATE.value)) #This string won't be shown on HTML, but will give a context on the frontend.
    except Exception as err:
        flash(f"We couldn't add this movie to your list. Try later!ERROR: {err}")
        flash(str(Status.ERROR.value)) #This string won't be shown on HTML, but will give a context on the frontend.
    finally:
        DB.close()
    return redirect(url_for('home', user_name = f'nickname={username}'))

@app.route('/del_movie/<movie_imdb>')
@login_required
def del_movie(movie_imdb):
    DB = conn.my_connection()
    title = dql.get_title_by_imdb(DB, movie_imdb)
    flash(f"\"{title}\" was removed successfully!")
    flash(str(Status.DELETION.value))
    username = dql.get_by_id(DB, session['user_id'])['username']
    dml.remove_movie(DB, user_id = session['user_id'], imdb_id = movie_imdb)
    DB.close()
    return redirect(url_for('home', user_name = f'nickname={username}'))

@app.route('/up_vote/<comment_id>')
@login_required
def up_vote(comment_id):
    DB = conn.my_connection()
    try:
        dml.load_vote_on_db(DB, user_id = session['user_id'], comment_id = comment_id, vote = Vote.LIKE.value)
    except MySQL.IntegrityError:
        if dql.user_has_downvoted(DB, comment_id = comment_id, user_id = session['user_id']):
            dml.update_vote(DB, comment_id = comment_id, user_id = session['user_id'], new_vote = Vote.LIKE.value)
        else:
            dml.delete_vote(DB, comment_id = comment_id, user_id = session['user_id'])
    finally:
        title = get_title_by_imdb_from_api(dql.get_imdb_by_comment(DB, comment_id))
        DB.close()
        return redirect(url_for('movie', title = title))

@app.route('/down_vote/<comment_id>')
@login_required
def down_vote(comment_id):
    DB = conn.my_connection()
    try:
        dml.load_vote_on_db(DB, user_id = session['user_id'], comment_id = comment_id, vote = Vote.UNLIKE.value)
    except MySQL.IntegrityError:
        if dql.user_has_upvoted(DB, comment_id = comment_id, user_id = session['user_id']):
            dml.update_vote(DB, comment_id = comment_id, user_id = session['user_id'], new_vote = Vote.UNLIKE.value)
        else:
            dml.delete_vote(DB, comment_id = comment_id, user_id = session['user_id'])
    finally:
        title = get_title_by_imdb_from_api(dql.get_imdb_by_comment(DB, comment_id))
        DB.close()
        return redirect(url_for('movie', title = title))