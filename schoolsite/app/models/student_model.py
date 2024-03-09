from sqlalchemy import JSON
from schoolsite.app import db
from datetime import datetime
from flask_login import UserMixin
import uuid


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(50), nullable=False)
    class_fee = db.Column(db.Integer, nullable=True)
    class_subjects = db.Column(JSON, nullable=True)
    class_books = db.Column(JSON, nullable=True)
    class_description = db.Column(db.Text, nullable=True)
    class_time_table = db.Column(JSON, nullable=True)
    materials = db.Column(db.String(200), nullable=True)
    teacher_username = db.Column(db.Integer,
                                 db.ForeignKey("teacher.username"),
                                 nullable=True)
    students = db.relationship("Student", backref="class_", lazy="dynamic")
    result = db.relationship("Results", backref='class_', lazy='dynamic')
    fee = db.relationship("StudentFee", backref='class_', lazy='dynamic')
    student_historys = db.relationship("StudentHistory",
                                       backref='class_',
                                       lazy='dynamic')
    students_attendance = db.relationship("StudentAttendance",
                                          backref='class_',
                                          lazy='dynamic')


class Student(db.Model, UserMixin):
    username = db.Column(db.String(100), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(300), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    enroll_date = db.Column(db.Date, nullable=True)
    guardians_name = db.Column(db.String(50), nullable=True)
    guardians_email = db.Column(db.String(200), nullable=True)
    guardians_phonenumber = db.Column(db.String(20), nullable=True)
    guardians_relation = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    home_town = db.Column(db.String(200), nullable=True)
    local_government = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    key = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(50), default="Student")
    previous_school = db.Column(db.String(100), nullable=True)
    medical_information = db.Column(db.String(200),
                                    nullable=True)  # Medical Information
    parental_consent = db.Column(db.Boolean, default=True)  # Parental Consent
    notes = db.Column(db.Text, nullable=True)  # Notes
    languages_spoken = db.Column(db.String(100), nullable=True)
    image_link = db.Column(db.String(100),
                           default='schoolsite/app/default.png')
    access = db.Column(db.Boolean, default=False)

    class_id = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=True)
    attendance = db.relationship("StudentAttendance",
                                 backref='student',
                                 lazy='dynamic')
    result = db.relationship("Results", backref='student', lazy='dynamic')
    fee = db.relationship("StudentFee", backref='student', lazy='dynamic')
    history = db.relationship("StudentHistory",
                              backref='student',
                              lazy='dynamic')

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def get_id(self):
        return self.username


class StudentAttendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.String(50), nullable=False)
    morning_attendance = db.Column(db.DateTime, default=None)
    evening_attendance = db.Column(db.DateTime, default=None)
    comment = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    late_arrival = db.Column(db.Boolean, nullable=True)

    student_username = db.Column(db.String(200),
                                 db.ForeignKey("student.username"),
                                 nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=False)


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result_type = db.Column(db.String(50), nullable=False)
    term = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    marks_obtain = db.Column(db.Integer, nullable=False)
    total_mark = db.Column(db.Integer, nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String(1000), nullable=True)
    year = db.Column(db.String(20), nullable=False)

    student_username = db.Column(db.String(200),
                                 db.ForeignKey('student.username'),
                                 nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)


class StudentFee(db.Model):
    transaction_id = db.Column(db.String(50),
                               primary_key=True,
                               default=str(uuid.uuid4()))
    year = db.Column(db.String(20), nullable=False)
    term = db.Column(db.String(50), nullable=False)
    fee_amount = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(100), nullable=True)
    payment_status = db.Column(db.String(100), nullable=True)
    payment_note = db.Column(db.String(1000), nullable=True)

    student_username = db.Column(db.String(200),
                                 db.ForeignKey('student.username'),
                                 nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)


class StudentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    academy_year = db.Column(db.Integer, nullable=False)
    fee_paid = db.Column(JSON, nullable=True)
    exam_result = db.Column(JSON, nullable=True)
    attendance = db.Column(JSON, nullable=True)
    school_fees = db.Column(JSON, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    promotion_status = db.Column(db.String(50), nullable=True)
    behavioral_notes = db.Column(db.String(1000), nullable=True)
    achievements = db.Column(db.String(1000), nullable=True)
    special_programs = db.Column(db.String(1000), nullable=True)

    student_username = db.Column(db.String(200),
                                 db.ForeignKey('student.username'),
                                 nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    teacher_username = db.Column(db.String(200),
                                 db.ForeignKey("teacher.username"),
                                 nullable=True)
