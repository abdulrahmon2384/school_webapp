from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from faker import Faker

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
fake = Faker()




from schoolsite import routes, models


with app.app_context():
    if db.metadata.tables:
       db.create_all()
