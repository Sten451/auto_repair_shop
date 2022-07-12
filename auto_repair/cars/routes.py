from flask import render_template, url_for, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from auto_repair.models import Auto_user, db
from auto_repair.cars.forms import CarFormUpdate, CarFormAdd


cars = Blueprint('cars', __name__)


@cars.route("/cars/my_car")
@login_required
def my_car():
    find_cars = Auto_user.query.filter_by(user_id=current_user.id).all()
    if len(find_cars) == 0:
        find_cars = None
    return render_template('car/user_car.html', cars=find_cars)


@cars.route("/cars/add_my_car", methods=['GET', 'POST'])
@login_required
def add_my_car():
    form = CarFormAdd()
    if form.validate_on_submit():
        new_car = Auto_user(model=form.model.data,
                            vin=form.vin.data, number=form.number.data, user_id=current_user.id)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('cars.my_car'))
    return render_template('car/add_car.html', form=form)


@cars.route("/cars/delete_car/<int:car_id>")
@login_required
def user_car_delete(car_id):
    car = Auto_user.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('cars.my_car'))


@cars.route("/cars/update_car/<int:car_id>", methods=['GET', 'POST'])
@login_required
def user_car_update(car_id):
    form = CarFormUpdate()
    car = Auto_user.query.get_or_404(car_id)
    if form.validate_on_submit():
        if car.user_id != current_user.id:
            abort(403)
        car.model = form.model.data
        car.vin = form.vin.data
        car.number = form.number.data
        db.session.commit()
        return redirect(url_for('cars.my_car'))
    elif request.method == 'GET':
        # pass
        form.model.data = car.model
        form.vin.data = car.vin
        form.number.data = car.number
    return render_template('car/update_car.html', form=form)
