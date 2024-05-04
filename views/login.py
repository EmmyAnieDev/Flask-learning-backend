# --------------------------------------   USING SESSIONS FOR LOGINS TO STORE SOME USER DATA -------------------------------

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

from models import UserDetails, db

db = SQLAlchemy() # Initializing the database

lg = Blueprint('login', __name__, template_folder='templates', static_folder='static')


@lg.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True # Setting the session to be permanent
        result = request.form['nm']  #request.form comes in as a dict, meaning we can access each object with the key.
        session['user_profile'] = result # Storing the username in the session, so we can access it later/other pages, stores data in a cookie and as a dictionary

        found_user = UserDetails.query.filter_by(name = result).first() # Querying the database to check if the user exists.
        if found_user: # Checking if the user exists
            session['email'] = found_user.email # Storing the email in the session
        else:
            new_user = UserDetails(name=result, email="") # Creating a new user with the username from the form and an empty email
            db.session.add(new_user) # Adding the new user to the database
            db.session.commit() # Committing the changes to the database any time we make changes to the database

        flash('login Successful!' , 'info')
        flash('welcome ' + result, 'info')
        return redirect(url_for('user.user'))
    else:
        if 'user_profile' in session:
            flash(f'Already logged in!', 'info')
            return redirect(url_for('user.user'))
        return render_template('login.html')


# --------------------------------------   HTTP METHODS (GET/POST) & RETRIEVING FORM DATA -------------------------------

# @app.route('/login', methods = ['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         result = request.form['nm']     #request.form comes in as a dict, meaning we can access each object with the key.
#         return redirect(url_for('user', username = result))
#     else:
#         return render_template('login.html')
#
# @app.route('/<username>')
# def user(username):
#     return f'<h1>{username}</h1>'