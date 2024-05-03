from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from forms import SignUpForm
from flask_cors import CORS
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'spiritcodes' # Secret key for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disabling the modification tracker to avoid warnings in the console when running the app
app.permanent_session_lifetime = timedelta(seconds=20)  # Setting the session to expire after 5 minutes
CORS(app)       # Allow CORS requests from all origins (for development purposes)

db = SQLAlchemy(app) # Initializing the database


#   --------------------------   LEARNING VIEWS, ROUTE AND VARIABLE RULES    ---------------------------
# @app.route('/home')
# def home_page():
#     return jsonify({'message': 'home page'})
#
# @app.route('/login')
# def login_page():
#     return jsonify({'message': 'login here'})
#
# @app.route('/signup')
# def signup_page():
#     return jsonify({'message': 'signup here'})
#
# @app.route('/user', methods = ['POST'])
# def show_user_profile():
#     return f'User profile for emmy'

# @app.route('/user/<username>')
# def show_user_profile(username):
#     # This view function will receive the username from the URL
#     return f'User profile for {username}'


# --------------------------------   TEMPLATES WITH JINJA 2    ------------------------------------------------
@app.route('/')
def user_name():
    name = 'SPIRIT'
    return render_template('index.html', name=name, sunny=False)


@app.route('/language')
def language():
    tech_stacks = [{'title': 'Beginner friendly framework for Python backend', 'framework': 'Flask'},
                   {'title': 'Best framework for mobile applications', 'framework': 'Flutter'}]
    return render_template('index.html', tech_stacks=tech_stacks)


# ----------------------------------    WEB FORMS IN FLASK     ---------------------------------------------------


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()  # initializing the signUpForm class
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)
    return render_template('Signup.html', form=form)


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


# --------------------------------------   USING SESSIONS FOR LOGINS TO STORE SOME USER DATA -------------------------------

@app.route('/view_users') # Creating a view function that checks if the user is logged in
def view_users():
    return render_template('view_users.html', values = User.query.all()) # Rendering the view_users.html template with all the users in the database

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True # Setting the session to be permanent
        result = request.form['nm']  #request.form comes in as a dict, meaning we can access each object with the key.
        session['user_profile'] = result # Storing the username in the session, so we can access it later/other pages, stores data in a cookie and as a dictionary

        found_user = User.query.filter_by(name = result ).first() # Querying the database to check if the user exists.
        if found_user: # Checking if the user exists
            session['email'] = found_user.email
        else:
            new_user = User(name=result, email="" ) # Creating a new user with the username from the form and an empty email
            db.session.add(new_user) # Adding the new user to the database
            db.session.commit() # Committing the changes to the database any time we make changes to the database

        flash('login Successful!' , 'info')
        return redirect(url_for('user'))
    else:
        if 'user_profile' in session:
            flash('Already logged in!', 'info')
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None            # Setting the email to None
    if 'user_profile' in session:               # Checking if the user_profile key is in the session
        username = session['user_profile']
        if request.method == 'POST':             # Checking if the request method is POST and storing the email in the session.
            email = request.form['email']
            session['email'] = email
            found_user = User.query.filter_by(name=username).first() # Querying the database to check if the user exists.
            found_user.email = email # Updating the email in the database with the email from the form and committing the changes
            db.session.commit() # Committing the changes to the database any time we make changes to the database
            flash('Email was saved!')
        else:
            if 'email' in session:             # Checking if the email key is in the session and storing the email in the email variable if it is.
                email = session['email']               # get the email from the session
        return render_template('user_profile.html', email=email)            # Rendering the userprofile.html template with the email
    else:
        flash('You are not logged in!', 'info')
        return redirect(url_for('login'))             # Redirecting to the login page if the user_profile key is not in the session


@app.route('/logout')
def logout():
    session.pop('user_profile', None)  # Remove data when user logout
    session.pop('email', None) # Remove data when user logout
    flash(f'You have been logged out! {user}' , 'info')
    return redirect(url_for('login')) #  Redirect to login page when no sessions and user logout.


# --------------------------------   DATABASE MODELS    ------------------------------------------------
class User(db.Model): # Creating a User class that inherits from db.Model
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, email): # Creating an __init__ method that initializes the username and email
        self.name = name
        self.email = email
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creating the database if it does not exist when the app is run directly
    app.run(host='0.0.0.0', port=5001)