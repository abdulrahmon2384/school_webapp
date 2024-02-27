from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
db = SQLAlchemy(app)

def has_tables():
	with app.app_context():
		db.reflect()
		return bool(db.metadata.tables)

	
def create_tables():
	db.create_all()


from schoolsite import routes, models
