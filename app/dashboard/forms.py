
from flask_wtf import FlaskForm
from wtfforms import StringField,TextAreaField,BooleanField,PasswordField
from wtfforms.validators import ValidationError,DataRequired,EqualTo
from app.models import Dashboard

class CommentForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	submit = SubmitField('Click here to submit')