from schoolsite.app.models import Announcement, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement, Results
from flask_login import login_user, current_user
from flask import render_template, flash, request, url_for, redirect, jsonify
from datetime import datetime
import math, itertools, collections, sqlalchemy, typing


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


def attendance_to_dict(student_attendances: typing.Iterable) -> list:
    to_dict = [{
        "morning_attendance":
        convert_date_string(student_attendance.morning_attendance),
        "evening_attendance":
        convert_date_string(student_attendance.evening_attendance),
        "comment":
        student_attendance.comment,
        "status":
        student_attendance.status,
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
                          term: str,
                          user: str,
                          year: str = '') -> None:
    pass


def fetch_attendance(username: str, term: str, user: str) -> list:
    if user == 'Teacher':
        attendance_records = TeacherAttendance.query.filter_by(
            teacher_username=username, term=term).all()
    else:
        attendance_records = StudentAttendance.query.filter_by(
            student_username=username, term=term).all()

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


def fetch_historical_or_current_attendance(username, term, role):
    if role and role in ['Teacher', 'Admin']:
        attendance = fetch_historical_data(username, term, 'Teacher')
        if not attendance:
            attendance = fetch_historical_data(username, term, 'Student')
    else:
        attendance = fetch_attendance(username, term, 'Teacher')
        if not attendance:
            attendance = fetch_attendance(username, term, 'Student')

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
    class_records = Class.query.filter_by(id=classid).all()[0]
    class_details_dict = convert_class_records_to_dict(class_records)
    teacher_about = class_records.teacher.about()
    return class_details_dict, teacher_about


def fetch_attendance_options(username: str, user_role: str) -> list:
    if user_role == 'Teacher':
        attendance_records = TeacherAttendance.query.with_entities(
            TeacherAttendance.term,
			sqlalchemy.func.extract('month',
                         TeacherAttendance.morning_attendance)).filter(
                             TeacherAttendance.teacher_username ==
                             username).distinct().all()
    else:
        attendance_records = StudentAttendance.query.with_entities(
            StudentAttendance.term,
			sqlalchemy.func.extract('month',
                         StudentAttendance.morning_attendance)).filter(
                             StudentAttendance.student_username ==
                             username).distinct().all()
    #dont worry about this it only conver the resul to key: value pair {key:[values , values]}
    attendance_to_dict = mapped_data = {term: [value for _, value in group] for term, group in itertools.groupby(attendance_records, key=lambda x: x[0])}
    return attendance_to_dict


def fetch_user_attendance_options(username: str) -> list:
    if username:
        user = Teacher.query.filter_by(username=username).first()
        if not user:
            user = Student.query.filter_by(username=username).first()

        if user:
            attendance_option = fetch_attendance_options(
                user.username, user.role)
            return attendance_option
    return attendance_option
