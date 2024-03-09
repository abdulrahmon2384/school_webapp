from flask import Blueprint, redirect, url_for
from flask_login import logout_user, login_required
from schoolsite.app import app

routes_bp = Blueprint('routes', __name__)

from schoolsite.app.routes.student import student_bp
from schoolsite.app.routes.teacher import teacher_bp
from schoolsite.app.routes.admin import admin_bp
from schoolsite.app.routes.home import home_bp

routes_bp.register_blueprint(home_bp)
routes_bp.register_blueprint(student_bp)
routes_bp.register_blueprint(teacher_bp)
routes_bp.register_blueprint(admin_bp)
