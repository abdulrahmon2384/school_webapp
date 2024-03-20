from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from schoolsite.app import app, db, bcrypt
from schoolsite.app.models import Announcement, Results, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement
from flask_login import login_user, current_user, logout_user, login_required
from schoolsite.app.functions.teacher_functions import *

teacher_bp = Blueprint('teacher', __name__)

school_name = "School OF Coding"
terms = 'third term'
number_of_event = 4
number_of_annoucement = 2
year = '2023'


@teacher_bp.route('/teachers/dashboard', methods=['GET'])
@login_required
def dashboard():
	page = "Dashboard"
	cl = Class.query.filter_by(teacher_username=current_user.username).first()
	top_student = get_total_marks(class_id=cl.id, term=terms, just_gen=False)

	male_student = top_student.get('Male')[0]
	female_student = top_student.get('Female')[0]

	summary = attendance_summary(cl.id, terms)
	attendancerate = summary.get("Overall_class_attendance")
	most_present = summary.get("class_frequently_present")
	most_absent = summary.get("class_frequently_absent")

	overview = class_overview(cl.id)
	insight = performance_insight(cl.id, terms)
	events = fetch_latest_events(number_of_event)
	announcements = fetch_latest_announcements(number_of_annoucement)
	return render_template("teacher/index.html",
	                       school_name=school_name,
	                       overview=overview,
	                       insight=insight,
	                       male_student=male_student,
	                       female_student=female_student,
	                       most_absent=most_absent,
	                       most_present=most_present,
	                       attendancerate=attendancerate,
	                       summary=summary,
	                       events=events,
	                       announcements=announcements,
	                       terms=terms,
	                       year=year,
	                       cl=cl,
	                       page=page)


@teacher_bp.route('/teachers/attendance', methods=['GET'])
@login_required
def attendance():
	page = "Attendance"
	cl = Class.query.filter_by(teacher_username=current_user.username).first()
	return render_template("teacher/attendance.html", page=page, cl=cl)


@teacher_bp.route('/teachers/performance', methods=['GET'])
@login_required
def performance():
	page = "Performance"
	cl = Class.query.filter_by(teacher_username=current_user.username).first()

	overview = class_overview(cl.id)
	announcements = fetch_latest_announcements(number_of_annoucement)
	insight = performance_insight(cl.id, terms)
	summary = attendance_summary(cl.id, terms)

	attendancerate = summary.get("Overall_class_attendance")
	return render_template("teacher/performance.html",
	                       page=page,
	                       cl=cl,
	                       overview=overview,
	                       announcements=announcements,
	                       attendancerate=attendancerate,
	                       insight=insight)


@teacher_bp.route('/teachers/update', methods=['GET'])
@login_required
def update():
	page = "Update"
	return render_template("teacher/update.html", page=page)
