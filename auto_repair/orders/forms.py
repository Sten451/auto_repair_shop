from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError, Regexp
from flask_login import current_user
from auto_repair.models import User


class CreateOrderForm(FlaskForm):
    choices_model = [
        ('Audi', 'Audi'),
        ('BMW', 'BMW'),
        ('Mercedes', 'Mercedes'),
        ('Volkswagen', 'Volkswagen'),
        ('Lexus', 'Lexus'),
        ('Other', 'Other'),
    ]
    model = SelectField('Модель авто:', choices=choices_model,
                        render_kw={"placeholder": "Модель"})
    username = StringField('Ник пользователя:',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)], render_kw={"placeholder": "Введите свой логин"})
    lastname = StringField('Фамилия пользователя:',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)], render_kw={"placeholder": "Введите Фамилию"})
    firstname = StringField('Имя пользователя:',
                            validators=[DataRequired(),
                                        Length(min=2, max=20)], render_kw={"placeholder": "Введите Имя"})
    email = StringField('Email:',
                        validators=[DataRequired(), Email()],  render_kw={"placeholder": "Введите email"})
    

    checkbox = BooleanField('Private?')
    submit = SubmitField('Записаться на ремонт')

    """def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Это имя занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Этот email занят. Пожалуйста, выберите другой.')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError(
                'Этот телефон занят. Пожалуйста, выберите другой.')"""
