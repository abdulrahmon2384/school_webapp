import random
from random import choice
from datetime import datetime, timedelta
from sqlalchemy import func
from schoolsite.models import Student, db, Teacher, Class, StudentAttendance, Results, StudentFee, Admin
from schoolsite import app, bcrypt






def geberate_fake_teacher():
	