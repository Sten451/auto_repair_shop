from flask import render_template, Blueprint, url_for, redirect
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from auto_repair.models import Category_of_work
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
def home():
    products = Category_of_work.query.all()
    return render_template('main.html', products=products)


class MyModelView(ModelView):
    pass


class MyAdminView(AdminIndexView):
    """Класс позволяет входить в админ зону только администратору"""

    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.home'))
