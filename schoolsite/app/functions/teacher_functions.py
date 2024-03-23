from schoolsite.app.models import Announcement, Teacher, Student, Class, Admin, Event, StudentAttendance, TeacherAttendance, TeacherHistory, StudentHistory, Announcement, Results, StudentFee
from schoolsite.app.functions.student_functions import get_total_marks, fetch_latest_events, fetch_latest_announcements, calculate_percentage, fetch_grade, fetch_class_details
from schoolsite.app import db
from typing import Dict, Any
from sqlalchemy import func, and_, distinct
from typing import Iterable
from datetime import datetime




def get_current_date():
	current_date = datetime.now()
	formatted_date = current_date.strftime("%B %d, %Y")
	return formatted_date




def performance_trend(percentage: int) -> str:
	if percentage >= 90:
		return "Excellent performance!"
	elif 80 <= percentage < 90:
		return "Very good performance."
	elif 70 <= percentage < 80:
		return "Good performance."
	elif 60 <= percentage < 70:
		return "Fair performance."
	else:
		return "Improving performance needed."


def class_overview(class_id: str) -> Dict[str, Any]:
	students_obj = Student.query.filter_by(class_id=class_id).all()
	subject_time = students_obj[0].class_.class_time_table['Times']
	schedule_time = [subject_time[0], subject_time[-1]]

	if students_obj:
		current_class = students_obj[0].class_
		num_students_enrolled = len(students_obj)
		schedule = schedule_time if current_class.class_time_table else ["Unknown", "Unknown"]

		data = {
		    "class_name": current_class.class_name,
		    "class_fee": current_class.class_fee,
		    "class_id": current_class.id,
		    "Student_enrolled": num_students_enrolled,
		    "schedule":
		    schedule_time if schedule_time else ["Unknown", "Unknow"]
		}
		return data
	else:
		return {}


def performance_insight(class_id: str, term: str) -> Dict[str, float]:
	try:
		average_score_per_exam = db.session.query(
		    Results.result_type.label("result_type"),
		    func.avg(Results.total_mark).label('average_score')).filter(
		        Results.class_id == class_id).group_by(
		            Results.result_type).order_by(
		                func.avg(Results.total_mark).desc()).all()

		data = {
		    score[0]: [score[0], round(score[1],1),
		               performance_trend(score[1])]
		    for score in average_score_per_exam
		}
		return {"average_score": data}
		
	except Exception as e:
		print(f"An error occurred: {str(e)}")
		return {}


def student_attendance_per(student_username: str, present: bool,
                                      class_id, term) -> Dict[str, Any]:
	student = Student.query.filter(
	    Student.username == student_username).first()
	if not student:
		return {"error": "Student not found"}

	query = StudentAttendance.query.filter_by(
	    student_username=student_username)
	if class_id and term :
		query = query.filter_by(class_id=class_id, term=term)

	student_attendance_records = query.all()
	total_records = len(student_attendance_records)

	if present:
		present_records = sum(1 for record in student_attendance_records
		                      if record.status in ('present', 'late'))
		attendance_rate = (present_records / total_records) * 100
	else:
		absent_records = sum(1 for record in student_attendance_records
		                     if record.status == 'absent')
		attendance_rate = (absent_records / total_records) * 100

	return {
	    "student_full_name": str(student),
	    "attendance_percentage": attendance_rate
	}


def get_class_attendance_percentage(class_id: int, present: bool,
                                    threshold: int, n: int,
                                    Total: bool,
								     term: str) -> Dict[str, Any]:
    students = Student.query.filter_by(class_id=class_id).all()
	
    if Total:
        num_of_day = StudentAttendance.query.filter_by(class_id=class_id, term=term).count()
        all_present = StudentAttendance.query.filter(and_(StudentAttendance.status.in_(["present", "late"]),
														  StudentAttendance.term == term, 
														  StudentAttendance.class_id == class_id)).count()
        overall_attendance_rate = calculate_percentage(all_present , num_of_day)
        return overall_attendance_rate
    else:
        frequent_students = []
        for student in students:
            student_attendance_records = StudentAttendance.query.filter_by(
			    student_username=student.username,
			    class_id=student.class_id,
			    term=term).all()
            total_records = len(student_attendance_records)

            if present:
                present_records = sum(1
				                      for record in student_attendance_records
				                      if record.status in ('present', 'late'))
                attendance_rate = (present_records / total_records) * 100
            else:
                absent_records = sum(1 for record in student_attendance_records
				                     if record.status == 'absent')
                attendance_rate = (absent_records / total_records) * 100
            if (present and attendance_rate >= threshold) or (not present and attendance_rate < threshold):
                frequent_students.append({
				    "student_full_name":
				    student,
				    "attendance_percentage":
				    round(attendance_rate,1)
				})
        if present:
            frequent_students.sort(key=lambda x: x["attendance_percentage"],
		                       reverse=True)
        else:
            frequent_students.sort(key=lambda x: x["attendance_percentage"])
			
        return frequent_students[:n] if len(frequent_students) >= n else frequent_students


def student_attendance_summary(class_id=None,
                               student_username=None,
                               present=True,
                               n=10,
                               threshold=0,
                               classes=False,
                               Total=False,
							   term=None) -> Dict[str, Any]:
	if student_username:
		return student_attendance_per(student_username, present,
		                                         class_id, term)
	elif classes:
		return get_class_attendance_percentage(class_id, present, threshold, n,
		                                       Total, term)
	else:
		return {"Coming soon": "Coming soon"}


def attendance_summary(class_id: str, term: str) -> Dict[str, Any]:
	Overall_class_attendance = student_attendance_summary(class_id=class_id,
														  classes=True,Total=True, term=term)
	class_frequently_present = student_attendance_summary(class_id=class_id,
	                                                      n=1,classes=True,
	                                                      threshold=60, term=term)
	class_frequently_absent = student_attendance_summary(class_id=class_id,
	                                                     n=1,classes=True,
	                                                     present=False,
	                                                     threshold=60, term=term)
	return {
	    "Overall_class_attendance": Overall_class_attendance,
	    "class_frequently_present": class_frequently_present,
	    "class_frequently_absent": class_frequently_absent
	}


def fetch_columns(class_id: str, username = None) -> Dict[str, Any]:
	valid_class = Results.query.filter_by(class_id=class_id)
	if not valid_class.first():
		return {"error": "Class not found"}

	distinct_years = Results.query.with_entities(distinct(Results.year).label("Years")).filter(Results.class_id == class_id)
	distinct_terms = Results.query.with_entities(distinct(Results.term).label("Terms")).filter(Results.class_id == class_id)
	distinct_types = Results.query.with_entities(distinct(Results.result_type).label("Type")).filter(Results.class_id == class_id)
	distinct_subjects = Results.query.with_entities(distinct(Results.subject).label("Subjects")).filter(Results.class_id == class_id)
	
	if username:
		valid_student = valid_class.filter_by(student_username=username) 
		if not valid_student.first():
			return {"error": "Student not found"}
			
		distinct_years = distinct_years.filter(Results.student_username == username)
		distinct_terms = distinct_terms.filter(Results.student_username == username)
		distinct_types = distinct_types.filter(Results.student_username == username)
		distinct_subjects = distinct_subjects.filter(Results.student_username == username)
		
	return {
		"Year": distinct_years.all(),
		"Term": distinct_terms.all(),
		"Type": distinct_types.all(),
		"Subject": distinct_subjects.all()
	 }


def sort_dict_by_value(dictionary):
	sorted_dict = dict(sorted(dictionary.items(), key=lambda x: x[1][2]))
	return sorted_dict


def calculate_age(birth_date):
	"""Calculate age from the given birth date."""
	today = datetime.today()
	age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
	return age


def student_var(class_id: str, username):
    query = Student.query.filter_by(class_id=class_id, username=username).first()
    name = str(query)
    gender = query.gender
    age = calculate_age(query.dob)
    return [name,  gender, age]



def image_link(student):
	query = Student.query.filter_by(username=student).first()
	return query.image_link



def fetch_performance_filtering(class_id: str,
			year: str,
			term: str,
			result_type=None,
			subject=None) -> dict:
	
    query = Results.query.filter_by(class_id= class_id, term=term, year=year)
    class_ = query.first()
	
    if not class_:
        print(f"either Class {class_id}, Term {term}, Year {year} not found.")
        return {}

    if result_type and result_type != "All":
        query = query.filter_by(result_type=result_type)
    if subject and subject != 'All':
        query = query.filter_by(subject=subject)

    results = (query.with_entities(Results.student_username, 
								   func.sum(Results.total_mark), 
								   func.sum(Results.marks_obtain)).group_by(Results.student_username).all())
    data = {student: student_var(class_id, student) +
		             [fetch_grade(total_mark, 
								  marks_obtain)] +
				     [student_attendance_per(student,
										    True, 
										    class_id, 
										    term).get("attendance_percentage"),
					  image_link(student),
					  calculate_percentage(total_mark, marks_obtain),
					 student]
		    for student, total_mark , marks_obtain in results}
    return data


def convert_to_valid_dict(input_dict):
    converted_dict = {}
    for key, value in input_dict.items():
        converted_dict[key] = [item[0] for item in value]
    return converted_dict



def last_n_session_attended(class_id: str, term: str,  n: int) -> Dict[str, Any]:
	dinstinct_dates = StudentAttendance.query.with_entities(distinct(StudentAttendance.morning_attendance)).filter(StudentAttendance.class_id == class_id, StudentAttendance.term == term).all()
	last_n = StudentAttendance.query.filter_by(class_id=class_id, term=term, morning_attendance= dinstinct_dates[n-1][0])
	return last_n.count(), dinstinct_dates[n-1][0]]