from flask import render_template, flash, request, url_for, redirect, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from schoolsite.app import app
from schoolsite.app.functions import *

student_api_bp = Blueprint('student_api', __name__)


def get_filtered_data(year, term, result_type):
    results = Results.query.filter_by(
        year=year,
        term=term,
        result_type=result_type,
        student_username=current_user.username).all()
    to_list = convert_to_dict(results)
    return to_list


@app.route('/api/performance', methods=['GET'])
@login_required
def performance():
    year = request.args.get('year')
    term = request.args.get('term')
    result_type = request.args.get('result_type')
    filtered_data = get_filtered_data(year, term, result_type)

    return jsonify({"results": filtered_data})


#   https://6c8f3853-e768-4117-9202-5a15bd1dcb23-00-1wfq2n3g69z4m.spock.replit.dev/api/performance?year=2023&term=first term&result_type=exam
