from typing import Iterable
from schoolsite.app.models import Announcement, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement, Results
from flask_login import login_user, current_user
from flask import render_template, flash, request, url_for, redirect, jsonify
from datetime import datetime
import math

grades = {'A+': 90, 'A': 85, 'A-': 80, 'B+': 75, 'B': 70}


def get_latest_events(n: int) -> list:
    ordered_event = Event.query.order_by(Event.date)
    top_events = ordered_event.limit(n).all()
    return top_events


def get_latest_announcements(n: int) -> list:
    ordered_announcement = Announcement.query.order_by(Announcement.created_at)
    top_announcements = ordered_announcement.limit(n).all()
    return top_announcements


def calculate_percentage(total_marks: int, marks_obtained: int) -> float:
    return (total_marks / marks_obtained) * 100


def get_grade(result, grades: dict = grades) -> str:
    marks_obtained = result.marks_obtain
    total_marks = result.total_mark
    percentage = calculate_percentage(total_marks, marks_obtained)

    for grade, number in grades.items():
        if percentage >= number and percentage < number + 10:
            return grade


def convert_date_string(date_string):
    date_obj = datetime.strptime(str(date_string), "%Y-%m-%d %H:%M:%S")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def get_percentage(result) -> int:
    marks_obtained = result.marks_obtain
    total_marks = result.total_mark

    percentage = (total_marks / marks_obtained) * 100
    return int(percentage)


def attendance_to_dict(student_attendances: Iterable) -> list:
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
        get_grade(result),
        "test_scores":
        result.total_mark,
        "percentage":
        f"{get_percentage(result)}%",
        "comments":
        result.comment[:30] +
        "..." if len(result.comment) > 20 else result.comment
    } for result in obj]
    return to_dict


def get_student_result(student_username: str) -> list:
    student_result = Results.query.filter_by(
        student_username=student_username).all()
    to_list = results_to_dict(student_result)
    return to_list


def get_columns(dicts: dict, columns: Iterable) -> dict:
    result_columns = {}
    for column in columns:
        values = {row[column] for row in dicts}
        result_columns[column] = list(values)
    return result_columns


def get_historical_data(username: str,
                        term: str,
                        user: str,
                        year: str = '') -> None:
    pass


def get_attendance(username: str, term: str, user: str) -> list:
    if user == 'Teacher':
        attendance = TeacherAttendance.query.filter_by(
            teacher_username=username, term=term).all()
    else:
        attendance = StudentAttendance.query.filter_by(
            student_username=username, term=term).all()
    print(sum([1 for attendance in attendance if attendance]))
    to_dict = attendance_to_dict(attendance)
    return to_dict


def get_performance_data(year, term, result_type, username):
    user = username if username else current_user.username
    results = Results.query.filter_by(year=year,
                                      term=term,
                                      result_type=result_type,
                                      student_username=user).all()
    to_list = results_to_dict(results)
    return to_list


def get_historical_or_current_attendance(username, term, role):
    if role and role in ['Teacher', 'Admin']:
        attendance = get_historical_data(username, term, 'Teacher')
        if not attendance:
            attendance = get_historical_data(username, term, 'Student')
    else:
        attendance = get_attendance(username, term, 'Teacher')
        if not attendance:
            attendance = get_attendance(username, term, 'Student')

    return attendance
