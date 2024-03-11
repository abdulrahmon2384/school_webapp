from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from schoolsite.app import app
from schoolsite.app.functions import *

student_api_bp = Blueprint('student_api', __name__)


@student_api_bp.route('/api/student/performance', methods=['GET'])
@login_required
def performance():
    year = request.args.get('year')
    term = request.args.get('term')
    result_type = request.args.get('result_type')
    username = request.args.get('username')

    if not (term and year and result_type):
        return jsonify(
            {"error": "Please provide term, year, and result_type."}), 400

    filtered_data = get_performance_data(year, term, result_type, username)
    return jsonify({"results": filtered_data})


@student_api_bp.route('/api/attendance', methods=['GET'])
@login_required
def get_user_attendance():
    term = request.args.get('term')
    username = request.args.get('username', current_user.username)
    year = request.args.get('currentyear')

    if not (term and username):
        return jsonify({"error":
                        "Please provide term, username, and year."}), 400

    if not year:
        year = 'fake-year'

    if year != 'fake-year':  #implement if year equal current year
        role = current_user.role if username == current_user.username else None
        attendance = get_historical_or_current_attendance(username, term, role)
    else:
        attendance = get_historical_or_current_attendance(
            username, term, 'Student')

    if attendance:
        return jsonify({"attendance": attendance}), 200
    else:
        return jsonify({"error": "Attendance data not found."}), 404


#/api/attendance?term=first%20term&username=allen76
#/api/attendance?term=first%20term&username=flewis
