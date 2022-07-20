from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email


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