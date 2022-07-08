import enum
import jwt
from datetime import datetime
from time import time
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_babel import Babel
from flask_mail import Mail
from flask import current_app


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
babel = Babel()
mail = Mail()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Модель пользователя"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    #review = db.relationship('Review', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        return jwt.encode(
            {'user_id': self.id, 'exp': time() + expires_sec},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['user_id']
        except Exception:
            return None
        return User.query.get(user_id)


class Review(db.Model):
    """Модель отзывов пользователей"""
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Auto_user(db.Model):
    """Модель автомобили пользователя"""
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    vin = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Mechanic(db.Model):
    """Модель персонала сервиса"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer)


class Category_of_work(db.Model):
    """Модель категорий работ"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    #price = db.Column(db.Integer, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Name_of_work(db.Model):
    """Модель видов работ"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category_of_work.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Status(enum.Enum):
    CONSIDERED = "Рассматривается"
    ACCEPTED = "Принят"
    WORK = "В работе"
    HOLD = 'Приостановлен до решения Заказчика'
    OVER = 'Ремонт окончен. Ожидается оплата'
    PAID = 'Оплачено'
    CLOSED = 'Закрыт'


class Order_user(db.Model):
    """Модель заказа пользователя"""

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mechanic_id = db.Column(
        db.Integer, db.ForeignKey('mechanic.id'), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey(
        'Name_of_work.id'), nullable=False
    )
    auto_id = db.Column(db.Integer, db.ForeignKey(
        'auto_user.id'), nullable=False)
    status = db.Column(db.Enum(Status), default=Status.CONSIDERED)
