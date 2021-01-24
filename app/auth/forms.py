from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,BooleanField
from wtforms.validators import ValidationError,DataRequired,EqualTo
from app.models import User # we import this database model because the registration form and usees it to check if user is not in database before commit

class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password= StringField('Password', validators=[DataRequired()])
	remember_me =BooleanField('Remember me')
	submit = SubmitField('Click here to submit')
	
class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password= StringField('Password', validators=[DataRequired()])
	password2= StringField('Repeat Password', validators=[DataRequired(),EqualTo('password')])

	submit = SubmitField('Click here to register')


	def validate_user(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')