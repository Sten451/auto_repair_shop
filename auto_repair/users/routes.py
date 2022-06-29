from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from auto_repair.models import User, Order_user, Auto_user, db, bcrypt
from auto_repair.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, CarForm
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
    return render_template('profile.html', title='Аккаунт',
                           image_file=image_file, form=form)


@users.route("/user/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/user/cars", methods=['GET', 'POST'])
@login_required
def user_car():
    form = CarForm()
    car = Auto_user.query.filter_by(user_id=current_user.id).first()
    if car:  # ! Если у него есть машина, то можем изменять
        if form.validate_on_submit():
            car.model = form.model.data
            car.vin = form.vin.data
            car.number = form.number.data
            db.session.commit()
            return redirect(url_for('users.user_car'))
        elif request.method == 'GET':
            form.model.data = car.model
            form.vin.data = car.vin
            form.number.data = car.number
            context = {}
            context['car'] = str(car.id)
            return render_template('/user_car.html', context=context, form=form)
    return render_template('/user_car.html', context=context, form=form)


@users.route("/user/delete_car/<int:car_id>")
@login_required
def user_car_delete(car_id):
    print('car_id', car_id)
    car = Auto_user.query.get_or_404(car_id)
    if Auto_user.user_id != current_user.id:
        abort(403)
    db.session.delete(car)
    db.session.commit()
    return render_template('/user_car.html')


@users.route("/user/admin_orders_current")
@login_required
def admin_orders_current():
    if current_user.admin:
        context = {}
        context['count_user'] = User.query.filter(User.admin != True).count()
        context['title'] = 'Текущие заказы'
        context['current_orders'] = Order_user.query.filter(
            Order_user.status != 'Закрыт')
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
