from flask import render_template, flash, request, url_for, redirect
from schoolsite import app, db, fake, bcrypt
from schoolsite.forms import LoginForm
from schoolsite.models import Teacher, Student, Class, Admin

password = "password"
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
school_name = "Hello world"


@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Welcome {form.username.data}', 'success')
        #return redirect(url_for("parent"))
    return render_template("index.html", form=form)


@app.route('/guardian')
def parent():
    return render_template("guardians.html")


@app.route('/teacher')
def teacher():
    return render_template("teachers.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")
