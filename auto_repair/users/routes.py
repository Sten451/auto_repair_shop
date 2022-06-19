from flask import render_template, Blueprint


users = Blueprint('users', __name__)


@users.route("/user/registration")
def registrations():
    return render_template('registration.html')


@users.route("/user/authentication")
def authentication():
    return render_template('authentication.html')


@users.route("/user/account")
def account():
    return render_template('account.html')
