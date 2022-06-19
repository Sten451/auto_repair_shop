from flask import Flask
from flask_admin import Admin
from config import Config
from main.routes import main
from users.routes import users
from models import db, login_manager


app = Flask(__name__)
app.config.from_object(Config)
admin = Admin(app, name='microblog', template_mode='bootstrap3')

app.register_blueprint(main)
app.register_blueprint(users)

login_manager.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
