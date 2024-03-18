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

	filtered_data = fetch_performance_data(year, term, result_type, username)
	return jsonify({"results": filtered_data})


@student_api_bp.route('/api/attendance', methods=['GET'])
@login_required
def get_user_attendance():
	username = request.args.get('username')
	year = request.args.get('year')
	month = request.args.get('month')

	if not all([year, username, month]):
		return jsonify({"error":
		                "Please provide month, username, and year."}), 400

	if year == '2050':
		year = 'fake-year'

	if year != 'fake-year':  #implement if year equal current year
		role = current_user.role if username == current_user.username else None
		attendance = fetch_historical_or_current_attendance(
		    username, year, month, role)
	else:
		attendance = fetch_historical_or_current_attendance(
		    username, year, month, 'Student')

	if attendance:
		return jsonify({"attendance": attendance}), 200
	else:
		return jsonify({"error": "Attendance data not found."}), 404


@student_api_bp.route('/api/student/fee', methods=['GET'])
@login_required
def get_student_fee():
	year = request.args.get('year')
	term = request.args.get('term')
	user = request.args.get('username')
	class_id = request.args.get('class_id')

	if not (user and class_id):
		return jsonify({"error": "Please provide username and class_id."}), 400

	data = fetch_student_fee(class_id=class_id,
	                         student_username=user,
	                         term=term,
	                         year=year)
	return jsonify({'fee': data})


@student_api_bp.route('/api/student/fee_details', methods=['GET'])
@login_required
def return_student_class_fee():
	year = request.args.get('year')
	term = request.args.get('term')
	user = request.args.get('username')
	class_id = request.args.get('class_id')

	if not (user and class_id):
		return jsonify({"error": "Please provide username and class_id."}), 400

	results = get_fee_detail(user=user,
	                         class_id=class_id,
	                         term=term,
	                         year=year)
	return jsonify(results)
