import random
from random import choice, sample
from datetime import datetime, timedelta
from sqlalchemy import func
from schoolsite.models import Student, db, Teacher, Class, StudentAttendance, Results, StudentFee, Admin
from schoolsite import app, bcrypt
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


def generate_class_time_table():
    timetable = generate_class_timetable()
    time_slots = generate_class_time_slots()
    class_time_table = {"Times": time_slots}
    class_time_table.update(timetable)
    return class_time_table


# Generate fake admin data
def generate_fake_admin(n):
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
def generate_fake_teacher():
    teachers = []
    for _ in range(10):
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


def generate_fake_class(teachers):
    classes = []
    for _ in range(10):
        class_name = fake.word()
        class_fee = random.randint(20000, 50000)
        class_subjects = generate_random_subjects(10)
        class_books = {
            'books': generate_student_textbooks(5),
            'authors': [fake.name() for i in range(5)],
            'amounts': [random.randint(2000, 4000) for i in range(5)]
        }
        class_description = fake.text()
        class_time_table = generate_class_time_table
        class_materials = fake.url()
        teacher_username = choice(teachers).username

        class_instance = Class(class_name=class_name,
                               class_fee=class_fee,
                               class_subjects=class_subjects,
                               class_books=class_books,
                               class_description=class_description,
                               class_time_table=class_time_table,
                               class_materials=class_materials,
                               teacher_username=teacher_username)
        return class_instance


def generate_fake_student(n, classes):
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
                          class_id=choice(classes),
                          access=True)
        students.append(student)
    return students


def generate_fake_results(students, terms, result_types):
    results = []
    for student in students:
        for term in terms:
            for result_type in result_types:
                subjects = student.class_.class_subjects
                for subject in subjects:
                    result = Results(result_type=result_type,
                                     term=term,
                                     subject=subject,
                                     marks_obtain=100,
                                     total_mark=random.randint(40, 100),
                                     submission_date=fake.date_time_between(
                                         start_date="-1y", end_date="now"),
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


def generate_fake_attendance(model, persons, terms):
    attendance_list = []
    for person in persons:
        for term in terms:
            morning_attendance = fake.date_time_between(
                start_date=f"{term}-01", end_date=f"{term}-28")
            evening_attendance = fake.date_time_between(
                start_date=morning_attendance,
                end_date=f"{term}-28") if fake.boolean(
                    chance_of_getting_true=70) else None
            comment = fake.text() if fake.boolean(
                chance_of_getting_true=20) else None
            status = fake.random_element(
                elements=('Present', 'Absent', 'Late')) if fake.boolean(
                    chance_of_getting_true=80) else None
            late_arrival = fake.boolean(
                chance_of_getting_true=30) if status == 'Late' else None

            attendance_entry = model(term=term,
                                     morning_attendance=morning_attendance,
                                     evening_attendance=evening_attendance,
                                     comment=comment,
                                     status=status,
                                     late_arrival=late_arrival,
                                     student_username=person.username
                                     if isinstance(person, Student) else None,
                                     teacher_username=person.username
                                     if isinstance(person, Teacher) else None,
                                     class_id=person.class_id if isinstance(
                                         person, Student) else None)
            attendance_list.append(attendance_entry)
    return attendance_list
