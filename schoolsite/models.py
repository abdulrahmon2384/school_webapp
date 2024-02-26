from sqlalchemy import JSON
from schoolsite import db
from datetime import datetime





class Student(db.Model):
	student_username = db.Column(db.String(30), primary_key=True)
	firstname = db.Column(db.String(30), nullable=False)
	lastname = db.Column(db.String(30), nullable=False)
	gender = db.Column(db.String(1), nullable=False)
	dateofbirth = db.Column(db.DateTime, nullable=False)
	homeaddress = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(50), nullable=True)
	phonenumber = db.Column(db.String(20), nullable=False)

	previous_school = db.Column(db.String(50), nullable=True)
	nationality  = db.Column(db.String(30), nullable=True)
	hometown = db.Column(db.String(30), nullable=True)
	state = db.Column(db.String(30), nullable=True)
	role = db.Column(db.String(20), nullable=False)
	specialneeds = db.Column(db.String(50), nullable=True)
	languagespoken = db.Column(db.String(30), nullable=True)

	guardian_fullname = db.Column(db.String(50), nullable=True)
	guardian_address = db.Column(db.String(100), nullable=True)
	guardian_phonenumber = db.Column(db.String(20), nullable=True)
	guardian_email = db.Column(db.String(50), nullable=True)
	guardian_relation = db.Column(db.String(20), nullable=True)
	guardian_occupation = db.Column(db.String(20), nullable=True)
	classid = db.Column(db.Integer, db.ForeignKey('class.classid'), nullable=False)
	imagelink = db.Column(db.String(100), default=None)	




class Teacher(db.Model):
		teacher_username = db.Column(db.String(30), primary_key=True)
		firstname = db.Column(db.String(30), nullable=False)
		lastname = db.Column(db.String(30), nullable=False)
		subject_taught = db.Column(db.String(30), nullable=True)
		gender = db.Column(db.String(1), nullable=False)
		email = db.Column(db.String(50), nullable=True)
		phonenumber = db.Column(db.String(20), nullable=False)
		address = db.Column(db.String(200), nullable=False)
		dateOfbirth = db.Column(db.DateTime, nullable=False)

		past_experience = db.Column(db.String(50), nullable=True)
		qualifications = db.Column(db.String(100), nullable=True)
		employment_date = db.Column(db.DateTime, nullable=False)
		nationality = db.Column(db.String(30), nullable=True)
		languagespoken = db.Column(db.String(30), nullable=True)

		left_date = db.Column(db.DateTime, nullable=True)
		access = db.Column(db.Boolean, nullable=True)
		role = db.Column(db.String(20), nullable=False)
		image_link = db.Column(db.String(100), default=None)
		salary = db.Column(JSON, nullable=True)
		salary_paid = db.Column(JSON, nullable=True)








class Class(db.Model):
	classid = db.Column(db.Integer, primary_key=True)
	classname = db.Column(db.String(20), nullable=False)
	classlevel = db.Column(db.String(20), nullable=True)
	classcapacity = db.Column(db.String(20), nullable=True)
	classroomnumber = db.Column(db.String(20), nullable=True)
	teacher_username = db.Column(db.String(30), db.ForeignKey("teacher.teacher_username"), nullable=True)



