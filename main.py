
from flask import Flask, render_template, request, jsonify
from models import db
from forms import SignUpForm
from flask_cors import CORS
from datetime import timedelta

from views.login import lg
from views.logout import lgt
from views.users import us
from views.view_users import vu

app = Flask(__name__)
app.config['SECRET_KEY'] = 'spiritcodes'  # Secret key for sessions
app.permanent_session_lifetime = timedelta(minutes = 5)  # Setting the session to expire after 5 minutes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabling the modification tracker to avoid warnings in the console when running the app
CORS(app)       # Allow CORS requests from all origins (for development purposes)
db.init_app(app)  # Initialize SQLAlchemy with the Flask app


app.register_blueprint(lg, url_prefix='/admin')    # Registering the login blueprint with the app instance to create a login route in the app. url_prefix='/login' is the URL prefix for the login route
app.register_blueprint(us, url_prefix='/person')
app.register_blueprint(lgt, url_prefix='/down')
app.register_blueprint(vu, url_prefix='/people')

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return 'error: Page does not exist', 404

@app.errorhandler(500)
def handle_500_error(e):
    app.logger.error('Server Error: %s', (e))
    return "Internal Server Error", 500


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
@app.route('/home')
def user_name():
    name = 'SPIRIT'
    return render_template('index.html', name=name, sunny=False)


@app.route('/language')
def language():
    tech_stacks = [{'title': 'Beginner friendly framework for Python backend', 'framework': 'Flask'},
                   {'title': 'Best framework for mobile applications', 'framework': 'Flutter'}]
    return render_template('index.html', tech_stacks=tech_stacks)

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()  # initializing the signUpForm class
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)
    return render_template('Signup.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creating the database if it does not exist when the app is run directly
    app.run(host='0.0.0.0', port=5001)