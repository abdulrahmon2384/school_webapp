from sqlalchemy import JSON
from schoolsite import db
from datetime import datetime


class Teacher(db.Model):
    username = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)

    classteacher = db.relationship("Class", backref="teacher", lazy="dynamic")
    classstudents = db.relationship("Student",
                                    backref="teacher",
                                    lazy="dynamic")
    attendance = db.relationship("TeacherAttendance",
                                 backref='attendance',
                                 lazy='dynamic')


class Class(db.Model):
    classid = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(20), nullable=False)
    classamount = db.Column(db.Decimal, nullable=True)

    teacher_id = db.Column(db.Integer,
                           db.ForeignKey("teacher.username"),
                           nullable=True)
    students = db.relationship("Student", backref="class_", lazy="dynamic")


class Student(db.Model):
    username = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)

    teacher_id = db.Column(db.String(50),
                           db.ForeignKey("teacher.username"),
                           nullable=True)
    class_id = db.Column(db.Integer,
                         db.ForeignKey("class.classid"),
                         nullable=True)

    attendance = db.relationship("StudentAttendance",
                                 backref='attendance',
                                 lazy='dynamic')


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
    term = db.Column(db.String(20), nullable=False)
    month = db.Column(db.String(3), nullable=False)
    morning_attendance = db.Column(db.DateTime, nullable=False)
    evening_attendance = db.Column(db.DateTime, nullable=True)
    comment = db.Column(db.String(50), nullable=True)

    teacher_username = db.Column(db.String(30),
                                 db.ForeignKey('teacher.username'),
                                 nullable=False)
