from datetime import datetime
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from auto_repair.models import Auto_user, Order_user, Name_of_work, Category_of_work, Mechanic, db


orders = Blueprint('orders', __name__)


@orders.route("/order/create", methods=['POST', 'GET'])
def create_order():
    products = Category_of_work.query.all()
    personal = Mechanic.query.all()
    car = Auto_user.query.all()
    if request.method == 'POST':
        work_id_list = request.form.getlist('check_box')
        auto_id = request.form.get('select_car')
        mechanic_id = request.form.get('select_person')
        date_work = request.form.get('select_datetime')
        date_work_datetime = datetime.strptime(date_work, "%Y-%m-%dT%H:%M")

        new_order = Order_user(
            date_work=date_work_datetime, user_id=current_user.id, mechanic_id=mechanic_id, auto_id=auto_id)
        db.session.add(new_order)
        db.session.commit()

        for work_id in work_id_list:
            work_id = Name_of_work.query.get(work_id)
            new_order.order_with_work.append(work_id)
        db.session.commit()
        return redirect(url_for('orders.order_history'))
    return render_template('orders/create_order.html', products=products, personal=personal, car=car)


@login_required
@orders.route("/order/history", methods=['GET'])
def order_history():
    my_orders = Order_user.query.filter_by(user_id=current_user.id)
    return render_template('orders/order_history.html', orders=my_orders)
