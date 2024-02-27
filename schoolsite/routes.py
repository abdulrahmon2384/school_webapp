from flask import render_template, flash, request, url_for
from schoolsite import app
from schoolsite.forms import LoginForm
from schoolsite.models import Student, Teacher, Class, StudentAttendance, Result, StudentFee, Admin, TeacherAttendance, TeacherHistory, StudentHistory







@app.route('/', methods=['GET', 'POST'])
def home():
	form = LoginForm()
	if form.validate_on_submit():
		print("Hello World")
	return render_template("login.html", title="Log in", form=form)





@app.route('/guardian')
def parent():
	return render_template("guardians.html")



@app.route('/teacher')
def teacher():
	return render_template("teachers.html")



@app.route("/admin")
def admin():
	return render_template("admin.html")




