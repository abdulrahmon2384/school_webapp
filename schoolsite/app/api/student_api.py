from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import app
from app.functions.student_function import *

student_api_bp = Blueprint('student_api', __name__)


@app.route('/api/performance', methods=['POST', 'GET'])
@login_required
def performance():
    student_results = get_student_result(current_user.username)
    return jsonify({"results": student_results})
