from flask import render_template, flash, request, url_for, redirect, jsonify
from schoolsite import app, db, bcrypt
from schoolsite.forms import LoginForm
from schoolsite.models import Announcement, Results, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement
from flask_login import login_user, current_user, logout_user, login_required
from schoolsite.methods import *

school_name = "School Name"
number_of_event = 6
number_of_annoucement = 2


@app.route('/', methods=['GET', 'POST'])
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
                return login_user_and_redirect(user, None, 'parent')
            elif user_type == "teacher":
                return login_user_and_redirect(user, user.role, 'teacher')
            else:
                return login_user_and_redirect(user, None, 'admin')

        return_error()

    return render_template("index.html", form=form)


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


@app.route('/api/performance', methods=['POST', 'GET'])
@login_required
def performance():
    student_results = get_student_result(current_user.username)
    return jsonify({"results": student_results})


@app.route('/teacher')
@login_required
def teacher():
    return render_template("teacher.html")


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
