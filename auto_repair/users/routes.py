from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from auto_repair.models import User, db, bcrypt
from auto_repair.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from auto_repair.users.utils import save_picture


users = Blueprint('users', __name__)


@users.route("/user/registration", methods=['POST', 'GET'])
def registrations():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password, firstname=form.firstname.data, lastname=form.lastname.data, phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('Ваша учетная запись была создана!'
              ' Теперь вы можете войти в систему', 'success')
        return redirect(url_for('users.authentication'))
    return render_template('registration.html', title='Register', form=form)


@users.route("/user/authentication", methods=['GET', 'POST'])
def authentication():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            #login_user(user, remember=form.remember.data)
            login_user(user)

            return redirect(url_for('users.account'))
        else:
            flash('Войти не удалось. Пожалуйста, '
                  'проверьте электронную почту и пароль', 'внимание')
    return render_template('authentication.html', title='Аутентификация', form=form)


@users.route("/user/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.username = form.username.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.email = form.email.data
        user.phone = form.phone.data
        db.session.commit()
        #flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.lastname.data = current_user.lastname
        form.firstname.data = current_user.firstname
        form.email.data = current_user.email
        form.phone.data = current_user.phone

    image_file = url_for('static', filename='img/lk/users/' +
                                            current_user.image_file)
    return render_template('account.html', title='Аккаунт',
                           image_file=image_file, form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
