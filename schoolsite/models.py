from sqlalchemy import JSON
from schoolsite import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user_models = [Admin, Teacher, Student]
    for model in user_models:
        user = model.query.get(user_id)
        if user:
            return model.query.get(user_id)
    return None


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    username = db.Column(db.String(50), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    access = db.Column(db.Boolean, nullable=True)
    key = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"
    
    def get_id(self):
        return self.username




class Teacher(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)

    role = db.Column(db.String(50), default=None)
    key = db.Column(db.String(50), nullable=True)
    access = db.Column(db.Boolean, nullable=True)

    classteacher = db.relationship("Class", backref="teacher", lazy="dynamic")
    classstudents = db.relationship("Student",
                                    backref="teacher",
                                    lazy="dynamic")
    attendance = db.relationship("TeacherAttendance",
                                 backref='teacher',
                                 lazy='dynamic')
    student_historys = db.relationship("StudentHistory",
                                       backref='teacher',
                                       lazy='dynamic')
    historys = db.relationship("TeacherHistory",
                               backref='teacher',
                               lazy='dynamic')

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def get_id(self):
        return self.username

class Class(db.Model):
    classid = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(50), nullable=False)
    classamount = db.Column(db.Integer, nullable=True)

    teacher_id = db.Column(db.Integer,
                           db.ForeignKey("teacher.username"),
                           nullable=True)
    students = db.relationship("Student", backref="class_", lazy="dynamic")
    result = db.relationship("Results", backref='class_', lazy='dynamic')
    fee = db.relationship("StudentFee", backref='class_', lazy='dynamic')
    student_historys = db.relationship("StudentHistory",
                                       backref='class_',
                                       lazy='dynamic')


class Student(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(50), default="Student")

    teacher_username = db.Column(db.String(50),
                                 db.ForeignKey("teacher.username"),
                                 nullable=True)
    class_id = db.Column(db.Integer,
                         db.ForeignKey("class.classid"),
                         nullable=True)

    attendance = db.relationship("StudentAttendance",
                                 backref='student',
                                 lazy='dynamic')
    result = db.relationship("Results", backref='student', lazy='dynamic')
    fee = db.relationship("StudentFee", backref='student', lazy='dynamic')
    student_historys = db.relationship("StudentHistory",
                                       backref='student',
                                       lazy='dynamic')

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def get_id(self):
        return self.username

class StudentAttendance(db.Model):
    __tablename__ = 'student_attendance'
    attendance_id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(50), nullable=False)
    morning_attendance = db.Column(db.DateTime, nullable=False)
    evening_attendance = db.Column(db.DateTime, nullable=True)
    comment = db.Column(db.String(1000), nullable=True)

    student_username = db.Column(db.String(50),
                                 db.ForeignKey("student.username"),
                                 nullable=False)


class TeacherAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(50), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    morning_attendance = db.Column(db.DateTime, nullable=False)
    evening_attendance = db.Column(db.DateTime, nullable=True)
    comment = db.Column(db.String(50), nullable=True)

    teacher_username = db.Column(db.String(30),
                                 db.ForeignKey('teacher.username'),
                                 nullable=False)


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_type = db.Column(db.String(50), nullable=False)
    term = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(30), nullable=False)
    marks_obtain = db.Column(db.Integer, nullable=False)
    total_mark = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    student_username = db.Column(db.String(50),
                                 db.ForeignKey('student.username'),
                                 nullable=False)
    class_id = db.Column(db.Integer,
                         db.ForeignKey('class.classid'),
                         nullable=False)


class StudentFee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(20), nullable=False)
    fee_amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=True)

    student_username = db.Column(db.String(50),
                                 db.ForeignKey('student.username'),
                                 nullable=False)
    class_id = db.Column(db.Integer,
                         db.ForeignKey('class.classid'),
                         nullable=False)


class StudentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    fee_paid = db.Column(JSON, nullable=True)
    exam_result = db.Column(JSON, nullable=True)
    attendance = db.Column(JSON, nullable=True)
    school_fees = db.Column(JSON, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    student_username = db.Column(db.String(50),
                                 db.ForeignKey('student.username'),
                                 nullable=False)
    class_id = db.Column(db.Integer,
                         db.ForeignKey('class.classid'),
                         nullable=False)
    teacher_username = db.Column(db.String(50),
                                 db.ForeignKey("teacher.username"),
                                 nullable=True)


class TeacherHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    salarys = db.Column(JSON, nullable=True)
    attendance = db.Column(JSON, nullable=True)
    termclass = db.Column(JSON, nullable=True)
    role = db.Column(db.String(20), nullable=True)

    teacher_username = db.Column(db.String(50),
                                 db.ForeignKey('teacher.username'),
                                 nullable=False)
