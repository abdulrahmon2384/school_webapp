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
    # List of school subjects
    subjects = [
        "Mathematics", "English Language", "Science", "Social Studies",
        "History", "Geography", "Computer Science", "Physical Education",
        "Art", "Music", "Biology", "Chemistry", "Physics", "Literature",
        "Foreign Language"
    ]

    # Return n random subjects
    return sample(subjects, n)


def generate_admin(n):
    admins = []
    for _ in range(n):
        admin = Admin(username=fake.user_name(),
                      firstname=fake.first_name(),
                      lastname=fake.last_name(),
                      email=fake.email(),
                      phonenumber=fake.phone_number(),
                      access=fake.boolean(),
                      key=hashed_password)
        admins.append(admin)
    return admins


def generate_teacher(n):
    teachers = []
    for _ in range(n):
        teacher = Teacher(username=fake.user_name(),
                          firstname=fake.first_name(),
                          lastname=fake.last_name(),
                          dob=fake.date_of_birth(),
                          address=fake.address(),
                          email=fake.email(),
                          phonenumber=fake.phone_number(),
                          gender=choice(['Male', 'Female']),
                          qualification=fake.job(),
                          hire_date=fake.date_this_decade(),
                          left_date=fake.date_this_decade(),
                          current_salary=randint(30000, 80000),
                          salarys={
                              'January': randint(30000, 80000),
                              'February': randint(30000, 80000),
                              'March': randint(30000, 80000)
                          },
                          role=fake.job(),
                          key=hashed_password,
                          access=fake.boolean(),
                          image_link=fake.image_url())
        teachers.append(teacher)
    return teachers


def generate_classes(n, teachers):
    classes = []
    for _ in range(n):
        class_name = fake.word(
        )  # You can customize this to generate more meaningful class names
        class_amount = fake.random_int(min=10000,
                                       max=50000)  # Adjust range as needed
        teacher = choice(teachers).username
        class_obj = Class(class_name=class_name,
                          class_amount=class_amount,
                          teacher_username=teacher)
        classes.append(class_obj)
    return classes
