from flask import render_template, flash, request, url_for
from schoolsite import app
from schoolsite.forms import LoginForm 






@app.route('/', methods=['GET', 'POST'])
def home():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Hello world')
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




