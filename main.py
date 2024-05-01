from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'spiritcodes'

# Allow CORS requests from all origins (for development purposes)
CORS(app)


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


#--------------------------------   TEMPLATES WITH JINJA 2    ------------------------------------------------
@app.route('/')
def user_name():
    name = 'SPIRIT'
    return render_template('index.html', name=name, sunny=False)


@app.route('/language')
def language():
    tech_stacks = [{'title': 'Beginner friendly framework for Python backend', 'framework': 'Flask'},
                   {'title': 'Best framework for mobile applications', 'framework': 'Flutter'}]
    return render_template('index.html', tech_stacks=tech_stacks)


#----------------------------------    WEB FORMS IN FLASK     ---------------------------------------------------
from forms import SignUpForm


@app.route('/signup')
def sign_up():
    form = SignUpForm()   # initializing the signUpForm class
    return render_template('Signup.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
