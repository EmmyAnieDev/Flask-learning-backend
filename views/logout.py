from flask import session, flash, redirect, url_for, Blueprint

lgt = Blueprint('logout', __name__, template_folder='templates', static_folder='static')


@lgt.route('/logout')
def logout():
    session.pop('user_profile', None)  # Remove data when user logout
    session.pop('email', None) # Remove data when user logout
    flash(f'You have been logged out!' , 'info')
    return redirect(url_for('login.login')) #  Redirect to login page when no sessions and user logout.