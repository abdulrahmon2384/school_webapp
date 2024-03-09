from typing import Iterable
from app.models import Announcement, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement, Results
from flask_login import login_user, current_user
from flask import render_template, flash, request, url_for, redirect, jsonify


def get_latest_events(n: int) -> list:
    ordered_event = Event.query.order_by(Event.date)
    top_events = ordered_event.limit(n).all()
    return top_events


def get_latest_announcements(n: int) -> list:
    ordered_announcement = Announcement.query.order_by(Announcement.created_at)
    top_announcements = ordered_announcement.limit(n).all()
    return top_announcements


def get_grade(result) -> str:
    marks_obtained = result.marks_obtain
    total_marks = result.total_mark

    percentage = (total_marks / marks_obtained) * 100

    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    else:
        return 'F'


def get_percentage(result) -> int:
    marks_obtained = result.marks_obtain
    total_marks = result.total_mark

    percentage = (total_marks / marks_obtained) * 100
    return int(percentage)


def convert_to_dict(obj) -> list:
    to_dict = [{
        "subject": result.subject,
        "year": result.submission_date.year,
        "term": result.term,
        "result_type": result.result_type,
        "grade": get_grade(result),
        "test_scores": f"{get_percentage(result)}%",
        "comments": result.comment
    } for result in obj]
    return to_dict


def get_student_result(student_username: str) -> list:
    student_result = Results.query.filter_by(
        student_username=student_username).all()
    to_list = convert_to_dict(student_result)
    return to_list


def get_columns(dicts: dict, columns: Iterable) -> dict:
    result_columns = {}
    for column in columns:
        values = {row[column]
                  for row in dicts}  # Convert to set to remove duplicates
        result_columns[column] = list(values)  # Convert back to list
    return result_columns
