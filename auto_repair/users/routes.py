from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from auto_repair.models import User, Order_user, Message, db, bcrypt
from auto_repair.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from auto_repair.users.utils import save_picture, send_reset_email


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
    return render_template('users/registration.html', title='Register', form=form)


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
    return render_template('users/authentication.html', title='Аутентификация', form=form)


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
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user.password = hashed_password
        db.session.commit()
        #flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.lastname.data = current_user.lastname
        form.firstname.data = current_user.firstname
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        #form.password.data = current_user.password

    image_file = url_for('static', filename='img/lk/users/' +
                                            current_user.image_file)
    return render_template('users/profile.html', title='Аккаунт',
                           image_file=image_file, form=form)


@users.route("/user/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/user/admin_orders_current", methods=['GET', 'POST'])
@login_required
def admin_orders_current():
    if current_user.admin:
        context = {}
        context['current_orders'] = Order_user.query.filter(
                Order_user.current_status != 'CLOSED')
        if request.method == 'POST':
            select_status = (request.form.get('select_status')).split(',')
            order = Order_user.query.filter_by(id=select_status[0]).first()
            order.current_status = select_status[1]
            db.session.commit()
        context['count_orders'] = Order_user.query.filter(
                Order_user.current_status != 'CLOSED').count()
        return render_template('admin/admin_orders_current.html', context=context)
    return redirect(url_for('main.home'))


@users.route("/user/admin_stat")
@login_required
def admin_stat():
    if current_user.admin:
        context = {}
        context['count_user'] = User.query.filter(User.admin != True).count()
        context['order_user'] = Order_user.query.count()
        context['title'] = 'Статистика'
        return render_template('admin/admin_statistics.html', context=context)
    return redirect(url_for('main.home'))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('На почту отправлено письмо с '
              'инструкциями по сбросу пароля.', 'info')
        return redirect(url_for('users.authentication'))
    return render_template('users/reset_password.html',
                           title='Сброс пароля', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Это недействительный или просроченный токен', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.\
            generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был обновлен! '
              'Теперь вы можете авторизоваться', 'success')
        return redirect(url_for('users.authentication'))
    return render_template('users/reset_token.html',
                           title='Сброс пароля', form=form)


@users.route("/user/admin_messages", methods=['GET', 'POST'])
@login_required
def admin_messages():
    if current_user.admin:
        context = {}
        context['messages_users'] = Message.query.filter(Message.
                                                     current_status_message != 'CLOSED')
        if request.method == 'POST':
            select_status = (request.form.get('select_status')).split(',')
            message = Message.query.filter_by(id=select_status[0]).first()
            message.current_status_message = select_status[1]
            db.session.commit()
        context['count_new_message'] = Message.query.filter(Message.
                                                            current_status_message != 'CLOSED').count()
        return render_template('admin/admin_messages.html', context=context)
    return redirect(url_for('main.home'))


@users.route("/user/support", methods=['GET'])
@login_required
def message_history():
    messages = Message.query.filter_by(user_id=current_user.id)
    return render_template('users/messages.html', messages=messages)


@users.route("/admin_messages_close", methods=['GET', 'POST'])
@login_required
def admin_messages_close():
    if current_user.admin:
        context = {}
        context['messages_users'] = Message.query.filter(Message.
                                                     current_status_message == 'CLOSED')
        if request.method == 'POST':
            select_status = (request.form.get('select_status')).split(',')
            message = Message.query.filter_by(id=select_status[0]).first()
            message.current_status_message = select_status[1]
            db.session.commit()
        context['count_new_message'] = Message.query.filter(Message.
                                                            current_status_message == 'CLOSED').count()
        return render_template('admin/admin_messages.html', context=context)
    return redirect(url_for('main.home'))