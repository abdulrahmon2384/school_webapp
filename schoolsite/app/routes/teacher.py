from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from app import app, db, bcrypt
from app.models import Announcement, Results, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement
from flask_login import login_user, current_user, logout_user, login_required
from functions.student_function import *

teacher_bp = Blueprint('teacher', __name__)


@app.route('/teacher')
@login_required
def teacher():
    return render_template("teacher.html")
