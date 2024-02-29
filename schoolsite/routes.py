from flask import render_template, flash, request, url_for
from schoolsite import app, db
from schoolsite.forms import LoginForm
from schoolsite.models import Teacher, Student, Class


school_name = "Hello world"



@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    return render_template("index.html", title=school_name, form=form)


@app.route('/guardian')
def parent():
    return render_template("guardians.html")


@app.route('/teacher')
def teacher():
    return render_template("teachers.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")
