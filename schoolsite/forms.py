from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email




class LoginForm(FlaskForm):
	username = StringField('User ID', validators=[DataRequired(), Length(min=4, max=20)])
	password = PasswordField('Secret Key', validators=[DataRequired(), Length(min=8)])
	login = SubmitField('Submit')