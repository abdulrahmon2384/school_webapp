from sqlalchemy import JSON
from schoolsite.app import db
from flask_login import UserMixin


class Teacher(db.Model, UserMixin):
    username = db.Column(db.String(100), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(300), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    qualification = db.Column(db.String(50), nullable=True)
    years_of_experience = db.Column(db.Integer, nullable=True)
    certifications = db.Column(db.String(200), nullable=True)
    teaching_specializations = db.Column(db.String(100), nullable=True)
    languages_spoken = db.Column(db.String(100), nullable=True)
    emergency_contact = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    hire_date = db.Column(db.Date, nullable=True)
    left_date = db.Column(db.Date, nullable=True)
    current_salary = db.Column(db.Integer, nullable=True)
    salarys = db.Column(db.JSON, nullable=True)
    subject_taught = db.Column(db.JSON, nullable=True)

    role = db.Column(db.String(50), default=None)
    key = db.Column(db.String(200), nullable=True)
    access = db.Column(db.Boolean, default=False)
    image_link = db.Column(db.String(200),
                           default='schoolsite/app/default.png')

    class_teacher = db.relationship("Class", backref="teacher", lazy="dynamic")
    attendance = db.relationship("TeacherAttendance",
                                 backref='teacher',
                                 lazy='dynamic')
    historys = db.relationship("TeacherHistory",
                               backref='teacher',
                               lazy='dynamic')

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def get_id(self):
        return self.username


class TeacherAttendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.String(50), nullable=False)
    morning_attendance = db.Column(db.DateTime, nullable=False)
    evening_attendance = db.Column(db.DateTime, nullable=True)
    comment = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    late_arrival = db.Column(db.Boolean, nullable=True)

    teacher_username = db.Column(db.String(200),
                                 db.ForeignKey('teacher.username'),
                                 nullable=False)


class TeacherHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=False)
    salarys = db.Column(JSON, nullable=True)
    attendance = db.Column(JSON, nullable=True)
    termclass = db.Column(JSON, nullable=True)
    role = db.Column(db.String(20), nullable=True)

    teacher_username = db.Column(db.String(200),
                                 db.ForeignKey('teacher.username'),
                                 nullable=False)
