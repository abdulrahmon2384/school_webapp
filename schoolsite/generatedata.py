import random
from random import choice
from datetime import datetime, timedelta
from sqlalchemy import func
from schoolsite.models import Student, db, Teacher, Class, StudentAttendance, Result, StudentFee, Admin
from schoolsite import app, bcrypt, fake


genders = ['M', 'F']


				   
					   















def add_student(n):
    for _ in range(n):
        student = Student(
            student_username=fake.user_name(),
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            gender=choice(genders),
            dateofbirth=fake.date_of_birth(minimum_age=10, maximum_age=20),
            homeaddress=fake.address(),
            email=fake.email(),
            phonenumber=fake.phone_number(),
            previous_school=fake.company(),
            nationality=fake.country(),
            hometown=fake.city(),
            state=fake.state(),
            current_status=fake.random_element(elements=('Inschool',
                                                         'Graduated',
                                                         'Dropped out')),
            role=fake.random_element(elements=('Student', None)),
            specialneeds=fake.random_element(elements=(None, 'Dyslexia',
                                                       'ADHD', 'Autism')),
            languagespoken=fake.random_element(elements=('English', 'Spanish',
                                                         'French')),
            guardian_fullname=fake.name(),
            guardian_address=fake.address(),
            guardian_phonenumber=fake.phone_number(),
            guardian_email=fake.email(),
            guardian_relation=fake.random_element(elements=('Parent',
                                                            'Grandparent',
                                                            'Sibling')),
            guardian_occupation=fake.job(),
            classid=Class.query.order_by(func.random()).first(),
            imagelink=None)
        db.session.add(student)
    db.session.commit()


def add_teachers(n):
    for _ in range(n):
        teacher = Teacher(teacher_username=fake.user_name(),
                          firstname=fake.first_name(),
                          lastname=fake.last_name(),
                          subject_taught={"Math", "Science", "English"},
                          gender=choice(["M", "F"]),
                          email=fake.email(),
                          phonenumber=fake.phone_number(),
                          address=fake.address(),
                          dateOfbirth=fake.date_of_birth(minimum_age=22,
                                                         maximum_age=60),
                          past_experience=fake.catch_phrase(),
                          qualifications=fake.sentence(),
                          employment_date=fake.date_time_this_decade(),
                          nationality=fake.country(),
                          languagespoken=fake.language_name(),
                          left_date=fake.date_time_this_decade()
                          if choice([True, False]) else None,
                          access=choice([True, False]),
                          role=choice(["Head Teacher", "Teacher"]),
                          image_link=fake.image_url(),
                          salary={
                              "basic": fake.random_number(4),
                              "bonus": fake.random_number(4)
                          },
                          salary_paid={"2022": fake.random_number(4)})
        db.session.add(teacher)
    db.session.commit()


def add_classes(n):
    for _ in range(n):
        classname = fake.word()
        classlevel = fake.word()
        classcapacity = random.randint(20, 40)
        classroomnumber = fake.random_int(100, 500)
        teacher = Teacher.query.order_by(func.random()).first()
        amount = random.randint(15000, 30000)
        classteacher = teacher.teacher_username if teacher else None
        new_class = Class(classname=classname,
                          classlevel=classlevel,
                          classcapacity=classcapacity,
                          classroomnumber=classroomnumber,
                          classamount=amount,
                          classteacher=classteacher)
        db.session.add(new_class)
    db.session.commit()


def add_StudentAttendance():
    students = Student.query.all()
    for student in students:
        morning_attendance = datetime.now().date() - timedelta(
            days=random.randint(1, 30))
        evening_attendance = None if not random.choice([
            True, False
        ]) else morning_attendance + timedelta(hours=random.randint(1, 7))
        status = random.choice(['Present', 'Absent', 'Late'])
        student_username = "example_student_username"
        comment = None if random.choice([True, False]) else fake.sentence()

        new_attendance = StudentAttendance(
            morning_attendance=morning_attendance,
            evening_attendance=evening_attendance,
            status=status,
            student_username=student_username,
            comment=comment)
        db.session.add(new_attendance)
    db.session.commit()


def add_fake_results():
    for term in ["First Term", "Second Term", "Third Term"]:
        for result in ["Test", "Exam", "Assignment"]:
            subjects = ['Math', 'Science', 'History', 'English', 'Art']
            students = Student.query.all()

            for student in students:
                for subject in subjects:
                    marks_obtain = random.randint(0, 100)
                    total_mark = 100
                    result = Result(student_username=student.student_username,
                                    classid=student.classid,
                                    result_type=result,
                                    term=term,
                                    subject=subject,
                                    marks_obtain=marks_obtain,
                                    total_mark=total_mark,
                                    date=datetime.now())
                    db.session.add(result)
    db.session.commit()


def add_student_fee():
    for term in ["First Term", "Second Term", "Third Term"]:
        students = Student.query.all()
        for student in students:
            student_class = Class.query.filter_by(
                classid=student.classid).first()
            fee_amount = random.randint(10000, student_class.amount)
            date = fake.date_time_between(start_date='-1y', end_date='now')
            status = fake.random_element(elements=('Paid', 'Pending', 'Late'))
            student_fee = StudentFee(student_username=student.student_username,
                                     classid=student.classid,
                                     term=term,
                                     fee_amount=random.randint(1000, 5000),
                                     date=date,
                                     status=status)
            db.session.add(student_fee)
    db.session.commit()


def add_TeacherAttendance():
    teachers = Teacher.query.all()
    for teacher in teachers:
        teacher_username = teacher
        term = fake.word()
        month = fake.month()
        morning_attendance = datetime.now().date() - timedelta(
            days=random.randint(1, 30))
        evening_attendance = None if not random.choice([
            True, False
        ]) else morning_attendance + timedelta(hours=random.randint(1, 7))
        comment = fake.text(max_nb_chars=50)

        attendance = TeacherAttendance(teacher_username=teacher_username,
                                       term=term,
                                       month=month,
                                       morning_attendance=morning_attendance,
                                       evening_attendance=evening_attendance,
                                       comment=comment)
        db.session.add(attendance)
    db.session.commit()
