from schoolsite.app.models import Announcement, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement, Results
from flask_login import login_user, current_user
from flask import render_template, flash, request, url_for, redirect, jsonify
from datetime import datetime
import math, itertools, collections, sqlalchemy, typing, pytz
from sqlalchemy import func, case
from schoolsite.app import db
from collections import defaultdict

grades = {'A+': 90, 'A': 80, 'B': 70, 'C': 60, 'D': 50, 'F': 40}


def fetch_latest_events(n: int) -> list:
	ordered_event = Event.query.order_by(Event.date)
	top_events = ordered_event.limit(n).all()
	return top_events


def fetch_latest_announcements(n: int) -> list:
	ordered_announcement = Announcement.query.order_by(Announcement.created_at)
	top_announcements = ordered_announcement.limit(n).all()
	return top_announcements


def calculate_percentage(total_marks: int, marks_obtained: int) -> float:
	if total_marks == 0:
		return 0
	return (total_marks / marks_obtained) * 100


def fetch_grade(result, grades: dict = grades) -> str:
	marks_obtained = result.marks_obtain
	total_marks = result.total_mark
	percentage = calculate_percentage(total_marks, marks_obtained)
	for grade, lower_bound in grades.items():
		upper_bound = lower_bound + 10
		if lower_bound <= percentage < upper_bound:
			return grade
	return 'F'


def convert_date_string(date_string):
	date_obj = datetime.strptime(str(date_string), "%Y-%m-%d %H:%M:%S")
	formatted_date = date_obj.strftime("%Y-%m-%d")
	return formatted_date


def to_percentage(result) -> int:
	marks_obtained = result.marks_obtain
	total_marks = result.total_mark

	percentage = calculate_percentage(total_marks, marks_obtained)
	return int(percentage)


def convert_to_ngn_time(date_str):
	date_str = date_str.strftime('%a, %d %b %Y %H:%M:%S GMT')
	nigerian_timezone = pytz.timezone('Africa/Lagos')

	date_object = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
	nigerian_time = date_object.astimezone(nigerian_timezone)

	formatted_time = nigerian_time.strftime('%I:%M %p')
	return formatted_time


def attendance_to_dict(student_attendances: typing.Iterable) -> list:
	to_dict = [{
	    "morning_attendance":
	    convert_to_ngn_time(student_attendance.morning_attendance),
	    "evening_attendance":
	    convert_to_ngn_time(student_attendance.evening_attendance),
	    "comment":
	    student_attendance.comment,
	    "status":
	    student_attendance.status,
	    "date":
	    convert_date_string(student_attendance.morning_attendance),
	    "late_arrival":
	    True if student_attendance.late_arrival else False
	} for student_attendance in student_attendances]
	return to_dict


def results_to_dict(obj) -> list:
	to_dict = [{
	    "subject":
	    result.subject,
	    "year":
	    result.submission_date.year,
	    "term":
	    result.term,
	    "result_type":
	    result.result_type,
	    "grade":
	    fetch_grade(result),
	    "test_scores":
	    result.total_mark,
	    "percentage":
	    f"{to_percentage(result)}%",
	    "comments":
	    result.comment[:30] +
	    "..." if len(result.comment) > 20 else result.comment
	} for result in obj]
	return to_dict


def fetch_student_result(student_username: str) -> list:
	student_result = Results.query.filter_by(
	    student_username=student_username).all()
	to_list = results_to_dict(student_result)
	return to_list


def columns(dicts: typing.Iterable, columns: typing.Iterable) -> dict:
	result_columns = {}
	for column in columns:
		values = {row[column] for row in dicts}
		result_columns[column] = list(values)
	return result_columns


def fetch_historical_data(username: str,
                          year: str,
                          user: str,
                          month: str,
                          term: str = '') -> None:
	pass


def fetch_attendance(username: str, month: str, year: str, user: str) -> list:
	if user == 'Teacher':
		attendance_records = TeacherAttendance.query.filter(
		    TeacherAttendance.teacher_username == username,
		    sqlalchemy.func.extract(
		        'month', TeacherAttendance.morning_attendance) == int(month),
		    sqlalchemy.func.extract(
		        'year',
		        TeacherAttendance.morning_attendance) == int(year)).all()

	else:
		attendance_records = StudentAttendance.query.filter(
		    StudentAttendance.student_username == username,
		    sqlalchemy.func.extract(
		        'month', StudentAttendance.morning_attendance) == int(month),
		    sqlalchemy.func.extract(
		        'year',
		        StudentAttendance.morning_attendance) == int(year)).all()

	attendance_records_to_dict = attendance_to_dict(attendance_records)
	return attendance_records_to_dict


def fetch_performance_data(year, term, result_type, username):
	user = username if username else current_user.username
	results = Results.query.filter_by(year=year,
	                                  term=term,
	                                  result_type=result_type,
	                                  student_username=user).all()
	to_list = results_to_dict(results)
	return to_list


def fetch_historical_or_current_attendance(username, year, month, role):
	if role and role in ['Teacher', 'Admin']:
		attendance = fetch_historical_data(username, year, month, 'Teacher')
		if not attendance:
			attendance = fetch_historical_data(username, year, month,
			                                   'Student')
	else:
		attendance = fetch_attendance(username, month, year, user='Teacher')
		if not attendance:
			attendance = fetch_attendance(username,
			                              month,
			                              year,
			                              user='Student')

	return attendance


def convert_class_records_to_dict(records: typing.Iterable) -> dict:
	records_dict = {}
	students = Student.query.filter(Student.class_id == records.id).all()
	if students:
		gender = collections.Counter([student.gender for student in students])
		records_dict = {
		    "num_of_students": sum(gender.values()),
		    "num_of_male": gender['Male'],
		    "num_of_female": gender['Female'],
		    "name": records.class_name,
		    "subjects": records.class_subjects,
		    "books": records.class_books,
		    "timetable": records.class_time_table,
		}
		return records_dict
	return records_dict


def fetch_class_details(classid: str) -> tuple:
	class_records = Class.query.filter_by(id=classid).first()
	class_details_dict = convert_class_records_to_dict(class_records)
	teacher_about = class_records.teacher.about()
	return class_details_dict, teacher_about


def get_student_fullname(student_username):
	student = Student.query.filter_by(username=student_username).first()
	if student:
		student_username = str(student)
		return student_username
	return "Unknown"


def get_top_students(data):
	grouped_data = defaultdict(list)
	result = {}
	if data:
		for username, score, count, gender, image_link in data:
			percentage = calculate_percentage(score, count * 100)
			fullname = get_student_fullname(username)
			grouped_data[gender].append(
			    (fullname, gender, round(percentage, 1), image_link))

		if len(grouped_data) == 1:
			result = grouped_data
			return result

		result['Male'] = max(grouped_data['Male'])
		result['Female'] = max(grouped_data['Female'])
		return result


def get_total_marks(class_id=None,
                    student_username=None,
                    term=None,
                    subject=None):
	filters = []
	if class_id:
		filters.append(Results.class_id == class_id)
	if student_username:
		filters.append(Results.student_username == student_username)
	if term:
		filters.append(Results.term == term)
	if subject:
		filters.append(Results.subject == subject)

	if not any([class_id, student_username, term]):
		return []

	query = db.session.query(
	    Results.student_username, func.sum(Results.total_mark),
	    func.count(Results.total_mark),
	    Student.gender, Student.image_link).join(
	        Student, Results.student_username == Student.username).filter(
	            *filters).group_by(
	                Results.student_username, Student.gender).order_by(
	                    func.sum(Results.total_mark).desc()).all()

	top_students = get_top_students(query)
	return top_students
