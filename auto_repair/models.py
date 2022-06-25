from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Модель пользователя"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    #review = db.relationship('Review', backref='author', lazy=True)

    def __repr__(self):
        return f"Пользователь('{self.username}', " \
            f"'{self.email}', '{self.image_file}')"


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

    def __init__(self, model, vin, number):
        self.model = model
        self.vin = vin
        self.number = number


class Order_user(db.Model):
    """Модель заказа пользователя"""
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100), nullable=False)
    vin = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    # TODO: связь с машинами пользователя и работами


class Type_of_work(db.Model):
    """Модель видов работ"""
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # TODO: связь с машинами пользователя и работами
