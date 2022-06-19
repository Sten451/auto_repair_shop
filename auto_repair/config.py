
class Config:
    """Класс параметров конфигурации"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_site.sqlite3'
    SECRET_KEY = '3d6f45a5fc12445dbac2f59c3b6c7cb1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
