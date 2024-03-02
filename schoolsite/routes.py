from flask import render_template, flash, request, url_for, redirect
from schoolsite import app, db, bcrypt
from schoolsite.forms import LoginForm
from schoolsite.models import Teacher, Student, Class, Admin
from flask_login import login_user, current_user, logout_user, login_required


school_name = "MySchool private"




def login_user_and_redirect(user, role, next_page):
    login_user(user, remember=True)
    if role == "head teacher":
        return redirect(url_for('admin'))
    return redirect(url_for(next_page))

def return_error():
    flash("Invalid username or password", "danger")





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



@app.route('/guardian')
@login_required
def parent():
    return render_template("guardians.html")


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



