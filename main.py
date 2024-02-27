from schoolsite import app, db, has_tables, create_tables
from schoolsite.models import Student, Teacher

def check_and_create_tables() -> None:
	if not has_tables():
		create_tables()
		
if __name__ == "__main__":
	check_and_create_tables()
	app.run(host='0.0.0.0', port=8080, debug=True)
