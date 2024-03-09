from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from schoolsite.app import app, db, bcrypt
from schoolsite.app.models import Announcement, Results, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement
from flask_login import login_user, current_user, logout_user, login_required
from schoolsite.app.functions import *

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/admin")
@login_required
def admin():
    return render_template("admin.html")
