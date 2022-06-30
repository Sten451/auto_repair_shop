from flask import render_template, Blueprint
from flask import render_template, Blueprint, url_for, redirect
from flask_admin import expose, BaseView, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from auto_repair.models import User, login_manager
from flask_login import UserMixin, current_user

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return render_template('main.html')


class MyModelView(ModelView):
    pass


class MyAdminView(AdminIndexView):
    """Класс позволяет входить в админ зону только администратору"""

    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.home'))
