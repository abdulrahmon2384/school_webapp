from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from schoolsite.app import app, db, bcrypt
from schoolsite.app.models import Announcement, Results, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement
from flask_login import login_user, current_user, logout_user, login_required
from schoolsite.app.functions import *

student_bp = Blueprint('student', __name__)

school_name = "School Name"
number_of_event = 3
number_of_annoucement = 1
table_row = 7


@student_bp.route('/guardian', methods=['GET'])
@login_required
def parent():
    student_results = fetch_student_result(current_user.username)
    result = columns(student_results, ['year', 'term', 'result_type'])
    events = fetch_latest_events(number_of_event)
    announcements = fetch_latest_announcements(number_of_annoucement)
    class_details, teacher = fetch_class_details(current_user.class_id)
    return render_template("student/index.html",
                           events=events,
                           announcements=announcements,
                           current_user=current_user,
                           school_name=school_name,
                           results=result,
						   class_details=class_details, 
						   teacher=teacher,
						   table_row=table_row)
