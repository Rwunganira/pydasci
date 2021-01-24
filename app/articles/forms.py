from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,BooleanField
from wtforms.validators import ValidationError,DataRequired,EqualTo
from app.models import Article # we import this database model because the registration form and usees it to check if user is not in database before commit
from flask_ckeditor import CKEditorField
class ArticleForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	text1= CKEditorField('Text', validators=[DataRequired()])

	submit = SubmitField('Click here to submit')