from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from forms import SignUpForm
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'spiritcodes' # Secret key for sessions
app.permanent_session_lifetime = timedelta(seconds=20)  # Setting the session to expire after 5 minutes
CORS(app)       # Allow CORS requests from all origins (for development purposes)


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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True # Setting the session to be permanent
        result = request.form['nm']  #request.form comes in as a dict, meaning we can access each object with the key.
        session['user_profile'] = result # Storing the username in the session, so we can access it later/other pages, stores data in a cookie and as a dictionary
        flash('login Successful!' , 'info')
        return redirect(url_for('user'))
    else:
        if 'user_profile' in session:
            flash('Already logged in!', 'info')
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/user')
def user():
    if 'user_profile' in session:   # Checking if the user_profile key is in the session
        username = session['user_profile']
        return render_template('user_profile.html', user=username) # Rendering the user.html template with the username
    else:
        flash('You are not logged in!', 'info')
        return redirect(url_for('login'))  # Redirecting to the login page if the user_profile key is not in the session


@app.route('/logout')
def logout():
    flash('You have been logged out!', 'info')
    session.pop('user_profile', None)  # Remove data when user logout
    return redirect(url_for('login')) #  Redirect to login page when no sessions and user logout.


if __name__ != '__main__':
    pass
else:
    app.run(host='0.0.0.0', port=5001)