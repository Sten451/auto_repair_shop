import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс параметров конфигурации"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_site.sqlite3'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    BABEL_DEFAULT_LOCALE = 'ru'

    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
