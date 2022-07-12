from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_login import current_user
from auto_repair.models import Auto_user


class CarFormAdd(FlaskForm):
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
    vin = StringField('VIN', validators=[DataRequired(), Length(min=17, max=17)], render_kw={
        "placeholder": "VIN номер"})
    number = StringField('Регистрационный знак', validators=[DataRequired()], render_kw={
        "placeholder": "Регистрационный знак"})
    submit = SubmitField('Добавить')

    def validate_vin(self, vin):
        car = Auto_user.query.filter_by(vin=vin.data).first()
        if car:
            raise ValidationError('Машина с таким VIN уже зарегистрирована')

    def validate_number(self, number):
        car = Auto_user.query.filter_by(number=number.data).first()
        if car:
            raise ValidationError(
                'Машина с таким номером уже зарегистрирована')


class CarFormUpdate(CarFormAdd, FlaskForm):
    submit = SubmitField('Изменить')

    def validate_vin(self, vin):
        car = Auto_user.query.filter_by(vin=vin.data).first()
        if car and current_user.id != car.user_id:
            raise ValidationError('Машина с таким VIN уже зарегистрирована')

    def validate_number(self, number):
        car = Auto_user.query.filter_by(number=number.data).first()
        if car and current_user.id != car.user_id:
            raise ValidationError(
                'Машина с таким номером уже зарегистрирована')
