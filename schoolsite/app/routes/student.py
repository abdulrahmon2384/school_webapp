import calendar

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from schoolsite.app.functions import *

student_bp = Blueprint('student', __name__)

school_name = "School Name"
terms = 'third term'
number_of_event = 4
number_of_annoucement = 3
table_row = 7
payment_dew_date = "2024-10-05"


@student_bp.route('/student/dashboard', methods=['GET'])
@login_required
def dashboard():
	page = "Dashboard"
	events = fetch_latest_events(number_of_event)
	announcements = fetch_latest_announcements(number_of_annoucement)
	return render_template("student/index.html",
	                       events=events,
	                       announcements=announcements,
	                       current_user=current_user,
	                       school_name=school_name,
	                       months=calendar.month_name,
	                       page=page)


@student_bp.route('/student/attendance', methods=['GET'])
@login_required
def attendance():
	page = 'Attendance Tracking'
	student_results = fetch_student_result(current_user.username)
	results = columns(student_results, ['year', 'term', 'result_type'])
	user_scores = get_total_marks(student_username=current_user.username)
	return render_template("student/attendance.html",
	                       results=results,
	                       months=calendar.month_name,
	                       user_scores=user_scores,
	                       page=page)


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
	                       user_scores=user_scores,
	                       page=page)


@student_bp.route('/student/performance', methods=['GET'])
@login_required
def performance():
	page = "Performance"
	student_results = fetch_student_result(current_user.username)
	result = columns(student_results, ['year', 'term', 'result_type'])
	return render_template("student/performance.html",
	                       results=result,
	                       page=page)


@student_bp.route('/student/fee', methods=['GET'])
@login_required
def fee():
	page = "School Fee"
	student_results = fetch_student_result(current_user.username)
	result = columns(student_results, ['year', 'term', 'result_type'])
	return render_template("student/fees.html", results=result, payment_dew_date=payment_dew_date, page=page)
