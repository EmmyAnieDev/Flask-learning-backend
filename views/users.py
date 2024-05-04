from flask import session, flash, redirect, url_for, request, render_template, Blueprint
from models import UserDetails, db

us = Blueprint('user', __name__, template_folder='templates', static_folder='static')

@us.route('/user', methods=['POST', 'GET'])
def user():
    email = None            # Setting the email to None
    if 'user_profile' in session:               # Checks if the user_profile is already stored in the session.
        username = session['user_profile']     # get the username from the session
        if request.method == 'POST':             # Checking if the request method is POST and storing the email in the session.
            email = request.form['email']
            session['email'] = email  # Storing the email in the session
            found_user = UserDetails.query.filter_by(name=username).first() # Querying the database to check if the user exists.
            found_user.email = email # Updating the email in the database with the email from the form and committing the changes
            db.session.commit() # Committing the changes to the database any time we make changes to the database
            flash('Email was saved!')
        else:
            if 'email' in session:             #  Checks if the email is already stored in the session.
                email = session['email']               #  If the email is in the session, retrieves it.
        return render_template('user_profile.html', email=email)   # Renders the 'user_profile.html' template and passes the email data to it.
    else:
        flash('You are not logged in!', 'info')
        return redirect(url_for('login.login'))             # Redirecting to the login page if the user_profile key is not in the session