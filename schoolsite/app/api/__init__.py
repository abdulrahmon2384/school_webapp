from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import student_api
from . import teacher_api
from . import admin_api

api_bp.register_blueprint(student_api.student_api_bp)
api_bp.register_blueprint(teacher_api.teacher_api_bp)
api_bp.register_blueprint(admin_api.admin_api_bp)
