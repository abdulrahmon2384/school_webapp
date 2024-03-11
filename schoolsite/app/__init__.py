from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = "secret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from schoolsite.app import models, routes, api, forms, functions
from schoolsite.app.routes import routes_bp
from schoolsite.app.api import api_bp

app.register_blueprint(routes_bp)
app.register_blueprint(api_bp)

from schoolsite.app.models.student_model import Student
from schoolsite.app.models.teacher_model import Teacher
from schoolsite.app.models.admin_model import Admin


@login_manager.user_loader
def load_user(user_id):
    user_models = [Admin, Teacher, Student]
    for model in user_models:
        user = model.query.get(user_id)
        if user:
            return user
    return None


with app.app_context():
    db.create_all()

#import schoolsite.app.generate_fake_data
