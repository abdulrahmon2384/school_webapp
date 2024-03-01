from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
#login_manager.login_view = "login"




from schoolsite import routes, models


with app.app_context():
    if db.metadata.tables:
       db.create_all()
