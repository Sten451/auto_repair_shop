from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError, Regexp
from flask_login import current_user
from models import User


class RegistrationForm(FlaskForm):
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
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=5, max=30)], render_kw={
                             "placeholder": "Введите пароль (5-30 символов)"})
    confirm_password = PasswordField('Подтвердить пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password')], render_kw={"placeholder": "Введите пароль повторно"})

    phone = StringField(label='Номер мобильного телефона', validators=[DataRequired(
    ), Regexp(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')], render_kw={"placeholder": "Номер мобильного телефона 11 цифр"})
    picture = FileField('Фото профиля',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
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
                'Этот телефон занят. Пожалуйста, выберите другой.')


class LoginForm(FlaskForm):
    username = StringField('Ник пользователя:', validators=[DataRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Введите свой логин"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={
                             "placeholder": "Введите свой пароль"})
    #remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Обновить фото профиля',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя занято. '
                                      'Пожалуйста, выберите другой')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email занят'
                                      'Пожалуйста, выберите другой')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Изменить пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунт с данным email-адресом '
                                  'отсутствует. '
                                  'Вы можете зарегистрировать его')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Переустановить пароль')
