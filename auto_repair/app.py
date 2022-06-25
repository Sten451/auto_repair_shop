from flask import Flask
from flask_admin import Admin
from auto_repair.config import Config
from auto_repair.main.routes import main
from auto_repair.users.routes import users
from auto_repair.models import db, login_manager, bcrypt
#from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object(Config)
admin = Admin(app, name='microblog', template_mode='bootstrap3')

app.register_blueprint(main)
app.register_blueprint(users)
#csrf = CSRFProtect(app)

login_manager.init_app(app)
bcrypt.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
