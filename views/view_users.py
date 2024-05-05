from flask import render_template, Blueprint

from models import UserDetails


vu = Blueprint('view_users', __name__, template_folder='templates', static_folder='static')

@vu.route('/view_users')  # Creating a view function that checks if the user is logged in
def view_users():
    return render_template('view_users.html', values = UserDetails.query.all())  # Rendering the view_users.html template with all the users in the database