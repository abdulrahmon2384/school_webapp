from flask import Blueprint, redirect, url_for
from flask_login import logout_user, login_required
from app import app

routes_bp = Blueprint('routes', __name__)

from . import student, teacher, home, admin

routes_bp.register_blueprint(home.home_bp)
routes_bp.register_blueprint(student.student_bp)
routes_bp.register_blueprint(teacher.teacher_bp)
routes_bp.register_blueprint(admin.admin_bp)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
