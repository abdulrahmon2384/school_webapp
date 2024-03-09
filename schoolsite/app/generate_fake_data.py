import random, uuid
from random import choice, sample
from datetime import datetime, timedelta
from schoolsite.app.models import Student, Teacher, Class, StudentAttendance, Results, StudentFee, Admin, TeacherAttendance, Event, Announcement
from schoolsite.app import app, bcrypt, db
from faker import Faker

fake = Faker()
password = "password"
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


def generate_random_subjects(n):
    subjects = [
        "Mathematics", "English Language", "Science", "Social Studies",
        "History", "Geography", "Computer Science", "Physical Education",
        "Art", "Music", "Biology", "Chemistry", "Physics", "Literature",
        "Foreign Language"
    ]
    return sample(subjects, n)


def generate_salary_data(year):
    salary_data = {}
    for month in range(1, 13):
        month_name = f'{year}-{month:02d}'
        salary_amount = random.randint(
            30000, 80000)  # Generate a random salary amount
        salary_data[month_name] = salary_amount
    return salary_data


def generate_yearly_salary_json(years):
    yearly_salary_json = {}
    for year in years:
        yearly_salary_json[year] = generate_salary_data(year)
    return yearly_salary_json


def generate_student_textbooks(n):
    textbooks = [
        "Mathematics for Beginners", "Science Explorers", "History Chronicles",
        "English Grammar Guide", "Art Appreciation 101",
        "Geography Adventures", "Computer Science Basics",
        "Literature Masterpieces", "Music Theory Fundamentals",
        "Economics Essentials", "Physics Fundamentals", "Chemistry Essentials",
        "Biology Basics", "Psychology Insights", "Sociology Essentials"
    ]
    return sample(textbooks, n)


def generate_class_timetable():
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetable = {}
    for day in days_of_week:
        timetable[day] = generate_random_subjects(7)
    return timetable


def generate_class_time_slots():
    time_slots = []
    current_time = "08:00"
    for _ in range(7):
        time_slots.append(current_time)
        current_time = (datetime.strptime(current_time, '%H:%M') +
                        timedelta(hours=1)).strftime('%H:%M')
    return time_slots


annoucement = [{
    "title": "School Holiday",
    "content":
    "Please be reminded that there will be no classes on Friday, March 15th, due to a scheduled school holiday. Enjoy your long weekend!",
    "date": "2024-03-15"
}, {
    "title": "Volunteer Opportunity",
    "content":
    "We're looking for parent volunteers to help with the upcoming school fair on April 5th. If you're interested, please contact the school office by March 20th.",
    "date": "2024-03-07"
}, {
    "title": "Uniform Reminder",
    "content":
    "A friendly reminder to all students: please ensure you are wearing the correct school uniform as outlined in the student handbook. Thank you for your cooperation.",
    "date": "2024-03-03"
}, {
    "title": "Library Book Return",
    "content":
    "All library books borrowed during the previous semester must be returned by Friday, March 8th. Overdue books will incur fines.",
    "date": "2024-03-05"
}]


def write_announcements_to_db(json_data):
    announcements = []
    for announcement in json_data:
        title = announcement['title']
        content = announcement['content']
        date = datetime.strptime(announcement['date'], '%Y-%m-%d').date()
        new_announcement = Announcement(title=title,
                                        content=content,
                                        created_at=date)
        announcements.append(new_announcement)
    return announcements


events = [{
    "name": "Parent-Teacher Meeting",
    "description":
    "A meeting between parents and teachers to discuss students' progress and address any concerns.",
    "date": "2024-04-15 18:00:00"
}, {
    "name": "School Open House",
    "description":
    "An event where prospective students and their families can visit the school, meet teachers, and learn about programs and facilities.",
    "date": "2024-05-03 10:00:00"
}, {
    "name": "Science Fair",
    "description":
    "A showcase of student projects and experiments related to various scientific topics.",
    "date": "2024-06-08 09:00:00"
}, {
    "name": "Field Day",
    "description":
    "A day of outdoor activities and sports competitions for students, often held at the end of the school year.",
    "date": "2024-07-20 08:30:00"
}, {
    "name": "Graduation Ceremony",
    "description":
    "A formal event to celebrate and recognize students who are completing their studies and moving on to the next phase of their lives.",
    "date": "2024-08-15 15:00:00"
}]


def add_events_to_database(events_lst):
    events = []
    for event_data in events_lst:
        name = event_data['name']
        description = event_data['description']
        date = datetime.strptime(event_data['date'], '%Y-%m-%d %H:%M:%S')

        # Create a new Event object
        new_event = Event(name=name, description=description, date=date)

        # Add the event to the database session
        events.append(new_event)
    return events


def generate_class_time_table():
    timetable = generate_class_timetable()
    time_slots = generate_class_time_slots()
    class_time_table = {"Times": time_slots}
    class_time_table.update(timetable)
    return class_time_table


# Generate fake admin data
def generate_fake_admins(n):
    adm = []
    for _ in range(n):
        admin = Admin(username=fake.user_name(),
                      firstname=fake.first_name(),
                      lastname=fake.last_name(),
                      email=fake.email(),
                      phonenumber=fake.phone_number(),
                      access=fake.boolean(),
                      key=hashed_password)
        adm.append(admin)
    return adm


# Generate fake teacher data
def generate_fake_teachers(n):
    teachers = []
    for _ in range(n):
        teacher = Teacher(
            username=fake.user_name(),
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            dob=fake.date_of_birth(),
            address=fake.address(),
            email=fake.email(),
            phonenumber=fake.phone_number(),
            gender=fake.random_element(elements=('Male', 'Female')),
            qualification=fake.random_element(elements=('Bachelor\'s Degree',
                                                        'Master\'s Degree',
                                                        'PhD')),
            years_of_experience=fake.random_number(digits=2),
            certifications=fake.sentence(),
            teaching_specializations=fake.word(),
            languages_spoken=fake.word(),
            emergency_contact=fake.phone_number(),
            notes=fake.text(),
            hire_date=fake.date_this_decade(),
            current_salary=fake.random_number(digits=5),
            role=fake.random_element(elements=('Teacher',
                                               'Assistant Teacher')),
            key=hashed_password,
            access=fake.boolean(),
            salarys=generate_yearly_salary_json([2021, 2022, 2023]),
            subject_taught=generate_random_subjects(3))
        teachers.append(teacher)
    return teachers


def generate_fake_classes(teachers, class_names):
    classes = []
    for class_ in class_names:
        class_name = class_
        class_fee = random.randint(20000, 50000)
        class_subjects = {'subjects': generate_random_subjects(10)}
        class_books = {
            'books': generate_student_textbooks(5),
            'authors': [fake.name() for i in range(5)],
            'amounts': [random.randint(2000, 4000) for i in range(5)]
        }
        class_description = fake.text()
        class_time_table = generate_class_time_table()
        class_materials = fake.url()
        teacher_username = choice(teachers).username

        class_instance = Class(class_name=class_name,
                               class_fee=class_fee,
                               class_subjects=class_subjects,
                               class_books=class_books,
                               class_description=class_description,
                               class_time_table=class_time_table,
                               materials=class_materials,
                               teacher_username=teacher_username)
        classes.append(class_instance)
    return classes


def generate_fake_students(n, classes):
    students = []
    for _ in range(n):
        student = Student(username=fake.user_name(),
                          firstname=fake.first_name(),
                          lastname=fake.last_name(),
                          dob=fake.date_of_birth(),
                          address=fake.address(),
                          email=fake.email(),
                          phonenumber=fake.phone_number(),
                          enroll_date=fake.date_this_decade(),
                          guardians_name=fake.name(),
                          guardians_email=fake.email(),
                          guardians_phonenumber=fake.phone_number(),
                          guardians_relation=choice(
                              ["Mother", 'Cousin', 'Uncle', 'Father']),
                          state=fake.state(),
                          home_town=fake.city(),
                          local_government=fake.city(),
                          gender=random.choice(['Male', 'Female']),
                          key=hashed_password,
                          previous_school=fake.company(),
                          medical_information=fake.sentence(),
                          parental_consent=fake.boolean(),
                          notes=fake.text(),
                          languages_spoken=fake.word(),
                          class_id=choice(classes).id,
                          access=True)
        students.append(student)
    return students


def generate_fake_results(students, terms, result_types):
    results = []
    for student in students:
        for term in terms:
            for result_type in result_types:
                subjects = student.class_.class_subjects['subjects']
                for subject in subjects:
                    date = fake.date_between(start_date='-1y', end_date='now')
                    result = Results(result_type=result_type,
									 year=str(date.year),
                                     term=term,
                                     subject=subject,
                                     marks_obtain=100,
                                     total_mark=random.randint(40, 100),
                                     submission_date=date,
                                     comment=fake.text(),
                                     student_username=student.username,
                                     class_id=student.class_id)
                    results.append(result)
    return results


def generate_fake_student_fees(students, years, terms):
    student_fees = []
    n = random.randint(1, 4)
    for student in students:
        for year in years:
            for term in terms:
                amount = [student.class_.class_fee // n] * n
                for fee_amount in amount:
                    fee_amount = random.randint(
                        5000, 20000)  # Generate a random fee amount
                    payment_date = fake.date_time_between_dates(
                        datetime.strptime(f"{year}-01-01", "%Y-%m-%d"),
                        datetime.strptime(f"{year}-12-31", "%Y-%m-%d"))
                    payment_method = fake.random_element(
                        elements=('Cash', 'Credit Card', 'Bank Transfer'))
                    payment_status = fake.random_element(elements=('Paid',
                                                                   'Unpaid'))
                    payment_note = fake.text()

                    student_fee = StudentFee(transaction_id=str(uuid.uuid4()),
                                             year=year,
                                             term=term,
                                             fee_amount=fee_amount,
                                             payment_date=payment_date,
                                             payment_method=payment_method,
                                             payment_status=payment_status,
                                             payment_note=payment_note,
                                             student_username=student.username,
                                             class_id=student.class_id)
                    student_fees.append(student_fee)
    return student_fees


def generate_fake_attendance(model, persons, terms, role='Student'):
    attendance_list = []
    for person in persons:
        for term, date in terms.items():
            random_date = fake.date_between(start_date=date[0],
                                            end_date=date[1])

            morning_attendance = random_date

            # Calculate evening attendance with a fixed time difference
            evening_attendance = morning_attendance + timedelta(
                hours=7) if morning_attendance else None

            comment = fake.text()
            status = fake.random_element(elements=('Present', 'Absent',
                                                   'Late'))
            late_arrival = fake.boolean(
                chance_of_getting_true=30) if status == 'Late' else None

            # Role-specific logic
            if role == 'Teacher':
                attendance_entry = model(term=term,
                                         morning_attendance=morning_attendance,
                                         evening_attendance=evening_attendance,
                                         comment=comment,
                                         status=status,
                                         late_arrival=late_arrival,
                                         teacher_username=person.username)
            else:
                attendance_entry = model(term=term,
                                         morning_attendance=morning_attendance,
                                         evening_attendance=evening_attendance,
                                         comment=comment,
                                         status=status,
                                         late_arrival=late_arrival,
                                         student_username=person.username,
                                         class_id=person.class_id)

            attendance_list.append(attendance_entry)
    return attendance_list


with app.app_context():
    db.create_all()
    admins = generate_fake_admins(2)
    db.session.add_all(admins)
    db.session.commit()

    teachers = generate_fake_teachers(10)
    db.session.add_all(teachers)
    db.session.commit()

    teachers = Teacher.query.all()
    class_names = [
        'KG1', "KG2", 'PRIMARY1', 'PRIMARY2', 'PRIMARY3', 'PRIMARY4',
        'PRIMARY5', 'PRIMARY6'
    ]
    classes = generate_fake_classes(teachers, class_names)
    db.session.add_all(classes)
    db.session.commit()

    classes = Class.query.all()
    students = generate_fake_students(100, classes)
    db.session.add_all(students)
    db.session.commit()

    years = [2023]
    students = Student.query.all()
    terms = ['first term', 'second term', 'third term']
    result_types = ['exam', 'assignment', 'quiz', 'test']

    results = generate_fake_results(students, terms, result_types)
    db.session.add_all(results)
    db.session.commit()

    students_fee = generate_fake_student_fees(students, years, terms)
    db.session.add_all(students_fee)
    db.session.commit()

    term = {
        'first term': [datetime(2023, 1, 1),
                       datetime(2023, 3, 31)],
        'second term': [datetime(2023, 4, 1),
                        datetime(2023, 7, 31)],
        'third term': [datetime(2023, 8, 1),
                       datetime(2023, 11, 30)]
    }
    students_attendance = generate_fake_attendance(StudentAttendance, students,
                                                   term)
    db.session.add_all(students_attendance)
    db.session.commit()

    teachrs_attendance = generate_fake_attendance(TeacherAttendance, teachers,
                                                  term, 'Teacher')
    db.session.add_all(teachrs_attendance)
    db.session.commit()

    evens_data = add_events_to_database(events)
    db.session.add_all(evens_data)
    db.session.commit()

    annoucements = write_announcements_to_db(annoucement)
    db.session.add_all(annoucements)
    db.session.commit()
    print("Done.......")
