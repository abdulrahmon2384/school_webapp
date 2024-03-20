from flask import Blueprint, request, jsonify
from flask_login import login_required
from schoolsite.app.functions.teacher_functions import *

teacher_api_bp = Blueprint('teacher_api', __name__)


@teacher_api_bp.route('/api/teacher/performance', methods=['GET'])
@login_required
def performance():
    year = request.args.get('year')
    term = request.args.get('term')
    result_type = request.args.get('result_type')
    subject = request.args.get('subject')
    class_id = request.args.get('class_id')

    if not all([class_id, year ,term]):
        return jsonify(
		{"error": "Please provide term, year, and class_id."}), 400

    results = fetch_performance_filtering(class_id, year, term, result_type, subject)
    return jsonify({"student":results})





