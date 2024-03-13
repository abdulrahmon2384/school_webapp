from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from schoolsite.app import app, db, bcrypt
from schoolsite.app.forms import LoginForm
from schoolsite.app.models import Announcement, Results, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement
from flask_login import login_user, current_user, logout_user, login_required
from schoolsite.app.functions import *

home_bp = Blueprint('home', __name__)


def login_user_and_redirect(user, role, next_page):
	login_user(user, remember=True)
	if role == "head teacher":
		return redirect(url_for('routes.admin.dashboard'))
	return redirect(url_for(next_page))


@home_bp.route('/', methods=['GET', 'POST'])
def home():
	form = LoginForm()
	if form.validate_on_submit():
		user_type = request.form.get('user_type')
		username = form.username.data.lower()
		password = form.password.data
		#flash(f"username: {form.username.data}, password: {form.password.data}, usertype: {user_type}")
		if user_type == "student":
			user = Student.query.filter_by(username=username).first()
		elif user_type == "teacher":
			user = Teacher.query.filter_by(username=username).first()
		else:
			user = Admin.query.filter_by(username=username).first()

		if user and bcrypt.check_password_hash(user.key, password):
			if user_type == "student":
				return login_user_and_redirect(user, None,
				                               'routes.student.dashboard')
			elif user_type == "teacher":
				return login_user_and_redirect(user, user.role,
				                               'routes.teacher.dashboard')
			else:
				return login_user_and_redirect(user, None,
				                               'routes.admin.dashboard')

		return_error()

	return render_template("home/index.html", form=form)


@home_bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home/index.html'))
