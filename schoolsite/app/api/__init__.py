from flask import Blueprint

api_bp = Blueprint('api', __name__)

from schoolsite.app.api.student_api import student_api_bp
from schoolsite.app.api.teacher_api import teacher_api_bp
from schoolsite.app.api.admin_api import admin_api_bp

api_bp.register_blueprint(student_api_bp)
api_bp.register_blueprint(teacher_api_bp)
api_bp.register_blueprint(admin_api_bp)
