from flask import render_template, Blueprint, request, url_for, redirect
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from auto_repair.models import Category_of_work, Message, User, db
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def home():
    products = Category_of_work.query.all()
    if request.method == 'POST':
        title = request.form.get('subject')
        message = request.form.get('message')
        name_user = request.form.get('name')
        email_user = request.form.get('email')
        user_request = User.query.filter_by(username=name_user).first()
        if user_request:
            user_id = user_request.id
        else:
            user_id = None
        
        new_message = Message(
            title=title, user_id=user_id, name_user=name_user, message=message, email_user=email_user)
        db.session.add(new_message)
        db.session.commit()
        
        if current_user.is_authenticated:
            return redirect(url_for('users.account'))
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


"""@main.route("/support", methods=['GET', 'POST'])
def send_message():
    #products = Category_of_work.query.all()
    #personal = Mechanic.query.all()
    #car = Auto_user.query.filter_by(user_id=current_user.id)
    if request.method == 'POST':
        title = request.form.getlist('subject')
        message = request.form.get('message')
        name_user = request.form.get('name')
        email_user = request.form.get('email')
        new_message = Message(
            title=title, name_user=name_user, message=message, email_user=email_user)
        db.session.add(new_message)
        db.session.commit()
    return redirect(url_for('main.home'))
    #return render_template('main.html', products=products)"""
