from schoolsite.app.models.student_model import Student, Class, StudentAttendance, Results, StudentFee, StudentHistory
from schoolsite.app.models.teacher_model import Teacher, TeacherHistory, TeacherAttendance
from schoolsite.app.models.admin_model import Admin, Event, Announcement
#from schoolsite.app import login_manager
'''
@login_manager.user_loader
def load_user(user_id):
	user_models = [Admin, Teacher, Student]
	for model in user_models:
		user = model.query.get(user_id)
		if user:
			return user
	return None
'''
