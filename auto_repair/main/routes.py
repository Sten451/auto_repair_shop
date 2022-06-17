from flask import render_template, Blueprint
from auto_repair.models import User

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return render_template('main.html')
