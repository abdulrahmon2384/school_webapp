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
	
	current_status = db.Column(db.String(30), nullable=True)
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
	
	def __repr__(self):
		return f"Student('{self.student_username}', '{self.firstname}', '{self.lastname}', '{self.gender}'" \
	

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
	
		def __repr__(self):
			return f"Teacher('{self.teacher_username}', '{self.firstname}', '{self.lastname}', '{self.gender}' '{self.subject_taught}'"


class Class(db.Model):
	classid = db.Column(db.Integer, primary_key=True)
	classname = db.Column(db.String(20), nullable=False)
	classlevel = db.Column(db.String(20), nullable=True)
	classcapacity = db.Column(db.String(20), nullable=True)
	classroomnumber = db.Column(db.String(20), nullable=True)
	teacher_username = db.Column(db.String(30), db.ForeignKey("teacher.teacher_username"), nullable=True)


class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    morning_attendance = db.Column(db.Date, nullable=False)
    evening_attendance = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(10), nullable=False)
    student_username = db.Column(db.String(30), db.ForeignKey('student.student_username'), nullable=False)
    comment = db.Column(db.String(50), nullable=True)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_username = db.Column(db.String(30), db.ForeignKey('student.student_username'), nullable=False)
    classid = db.Column(db.Integer, db.ForeignKey('class.classid'), nullable=False)
    result_type = db.Column(db.String(20), nullable=False)
    term = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(30), nullable=False)
    marks_obtain = db.Column(db.Integer, nullable=False)
    total_mark = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class StudentFee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_username = db.Column(db.String(30), db.ForeignKey('student.student_username'), nullable=False)
    classid = db.Column(db.Integer, db.ForeignKey('class.classid'), nullable=False)
    term = db.Column(db.String(20), nullable=False)
    fee_amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=True)


class TeacherAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_username = db.Column(db.String(30), db.ForeignKey('teacher.teacher_username'), nullable=False)
    term = db.Column(db.String(20), nullable=False)
    month = db.Column(db.String(10), nullable=False)
    morning_attendance = db.Column(db.DateTime, nullable=False)
    evening_attendance = db.Column(db.DateTime, nullable=True)
    comment = db.Column(db.String(50), nullable=True)


class StudentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_username = db.Column(db.String(30), db.ForeignKey('student.student_username'), nullable=False)
    classid = db.Column(db.Integer, db.ForeignKey('class.classid'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    teacher_username = db.Column(db.String(30), nullable=True)
    fee_paid = db.Column(JSON, nullable=True)
    exam_result = db.Column(JSON, nullable=True)
    attendance = db.Column(JSON, nullable=True)
    school_fees = db.Column(db.Integer, nullable=True)


class TeacherHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_username = db.Column(db.String(30), db.ForeignKey('teacher.teacher_username'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    salarys = db.Column(JSON, nullable=True)
    attendance = db.Column(JSON, nullable=True)
    termclass = db.Column(JSON, nullable=True)
    role = db.Column(db.String(20), nullable=False)


class Admin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable=False)
	firstname = db.Column(db.String(30), nullable=False)
	lastname = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	phonenumber = db.Column(db.String(20), nullable=False)
	access = db.Column(db.Boolean, nullable=False)


	def __repr__(self):
		return f"Admin('{self.username}', '{self.firstname}', '{self.lastname}', '{self.email}', 'Access={self.access}'"
    

