from flask import Flask
from flask_admin import Admin
from auto_repair.config import Config
from auto_repair.main.routes import main, MyAdminView, MyModelView
from auto_repair.users.routes import users
from auto_repair.cars.routes import cars
from auto_repair.errors.handlers import errors
from auto_repair.models import db, login_manager, bcrypt, babel, mail
from auto_repair.models import User, Order_user, Mechanic


app = Flask(__name__)
app.config.from_object(Config)
admin = Admin(app, name='CarOne', index_view=MyAdminView(),
              template_mode='bootstrap4')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Order_user, db.session))
admin.add_view(MyModelView(Mechanic, db.session))

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(cars)
app.register_blueprint(errors)

login_manager.init_app(app)
bcrypt.init_app(app)
babel.init_app(app)
mail.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
