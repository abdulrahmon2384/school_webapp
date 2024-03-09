from flask_login import LoginManager
from .student_model import Student, Class, StudentAttendance, Results, StudentFee, StudentHistory
from .teacher_model import Teacher, TeacherHistory, TeacherAttendance
from .admin_model import Admin, Event, Announcement

login_manager = LoginManager()


# Register the user_loader function
@login_manager.user_loader
def load_user(user_id):
    user_models = [Admin, Teacher, Student]
    for model in user_models:
        user = model.query.get(user_id)
        if user:
            return user
    return None
