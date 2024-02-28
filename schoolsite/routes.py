from flask import render_template, flash, request, url_for
from schoolsite import app, db
from schoolsite.forms import LoginForm
from schoolsite.models import Teacher, Student, Class



@app.route('/')
def index():
    teacher1 = Teacher(username=1, firstname="John", lastname="Doe")
    teacher2 = Teacher(username=2, firstname="Ola", lastname="Oluwa")
    teacher3 = Teacher(username=3, firstname="Azeez", lastname="Olumuyiwa")
    db.session.add_all([teacher1, teacher2, teacher3])
    db.session.commit()

    return render_template('index.html', teachers=[1,2,3])



@app.route('/g', methods=['GET', 'POST'])
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
