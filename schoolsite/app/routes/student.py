from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from app import app, db, bcrypt
from app.models import Announcement, Results, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement
from flask_login import login_user, current_user, logout_user, login_required
from functions.student_function import *

student_bp = Blueprint('student', __name__)

school_name = "School Name"
number_of_event = 6
number_of_annoucement = 2


@app.route('/guardian', methods=['GET'])
@login_required
def parent():
    student_results = get_student_result(current_user.username)
    result = get_columns(student_results, ['year', 'term', 'result_type'])
    events = get_latest_events(number_of_event)
    announcements = get_latest_announcements(number_of_annoucement)
    return render_template("guardians.html",
                           events=events,
                           announcements=announcements,
                           current_user=current_user,
                           school_name=school_name,
                           results=result)
