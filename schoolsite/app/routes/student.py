from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from schoolsite.app import app, db, bcrypt
from schoolsite.app.models import Announcement, Results, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement
from flask_login import login_user, current_user, logout_user, login_required
from schoolsite.app.functions import *
import calendar

student_bp = Blueprint('student', __name__)

school_name = "School Name"
terms = 'third term'
number_of_event = 3
number_of_annoucement = 1
table_row = 7
months = [
    'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct',
    'nov', 'dec'
]


@student_bp.route('/student/dashboard', methods=['GET'])
@login_required
def dashboard():
	page = "Dashboard"
	student_results = fetch_student_result(current_user.username)
	result = columns(student_results, ['year', 'term', 'result_type'])
	events = fetch_latest_events(number_of_event)
	announcements = fetch_latest_announcements(number_of_annoucement)
	return render_template("student/index.html",
	                       events=events,
	                       announcements=announcements,
	                       current_user=current_user,
	                       school_name=school_name,
	                       results=result,
	                       months=calendar.month_name)


@student_bp.route('/student/attendance', methods=['GET'])
@login_required
def attendance():
	page = 'Attendance Tracking'
	student_results = fetch_student_result(current_user.username)
	results = columns(student_results, ['year', 'term', 'result_type'])
	return render_template("student/attendance.html",
	                       results=results,
	                       months=calendar.month_name)


@student_bp.route('/student/class', methods=['GET'])
@login_required
def class_():
	page = 'Class Detail'
	class_details, teacher = fetch_class_details(current_user.class_id)
	top_student = get_total_marks(class_id=current_user.class_id, term=terms)
	user_scores = get_total_marks(student_username=current_user.username)
	return render_template("student/class.html",
	                       class_details=class_details,
	                       teacher=teacher,
	                       table_row=table_row,
	                       top_student=top_student,
	                       user_scores=user_scores)


@student_bp.route('/student/performance', methods=['GET'])
@login_required
def performance():
	page = "Performance"
	return render_template("student/performance.html")


@student_bp.route('/student/fee', methods=['GET'])
@login_required
def fee():
	page = "Student Fee"
	return render_template("student/fees.html")
