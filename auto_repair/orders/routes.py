from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from auto_repair.models import Auto_user, User, Order_user, Name_of_work, Category_of_work, Mechanic, db
from auto_repair.orders.forms import CreateOrderForm


orders = Blueprint('orders', __name__)


@orders.route("/order/create", methods=['POST', 'GET'])
def create_order():
    products = Category_of_work.query.all()
    personal = Mechanic.query.all()
    car = Auto_user.query.all()
    if request.method == 'POST':
        work_id = request.form.getlist('check_box')
        auto_id = request.form.get('select_car')
        mechanic_id = request.form.get('select_person')
        date_work = request.form.get('select_datetime')
        print(work_id)
        print(mechanic_id)
        print(auto_id)
        print(date_work)

        f = datetime.strptime(date_work, "%Y-%m-%dT%H:%M")
        #datetime.strptime(date_work, dateFormatter)
        print('f', type(f), f)

        new_order = Order_user(
            date_work=f, user_id=current_user.id, mechanic_id=mechanic_id, work_id=work_id, auto_id=auto_id)
        print('new_order', new_order)
        db.session.add(new_order)
        db.session.commit()
        print('new_order', new_order)
        """flash('Ваша учетная запись была создана!'
              ' Теперь вы можете войти в систему', 'success')
        return redirect(url_for('users.authentication'))"""
    elif request.method == 'GET':
        pass

    return render_template('orders/create_order.html', products=products, personal=personal, car=car)
