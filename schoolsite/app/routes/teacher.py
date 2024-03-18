from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from schoolsite.app import app, db, bcrypt
from schoolsite.app.models import Announcement, Results, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement
from flask_login import login_user, current_user, logout_user, login_required
from schoolsite.app.functions import *

teacher_bp = Blueprint('teacher', __name__)
school_name = "School OF Coding"


@teacher_bp.route('/teachers/dashboard', methods=['GET'])
@login_required
def dashboard():
	return render_template("teacher/index.html", school_name=school_name)


@teacher_bp.route('/teachers/attendance', methods=['GET'])
@login_required
def attendance():
	return render_template("teacher/attendance.html")


@teacher_bp.route('/teachers/performance', methods=['GET'])
@login_required
def performance():
	return render_template("teacher/performance.html")


@teacher_bp.route('/teachers/update', methods=['GET'])
@login_required
def update():
	return render_template("teacher/update.html")
