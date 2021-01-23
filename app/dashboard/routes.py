

from flask import render_template,request, url_for, flash
from flask_login import current_user,login_required
from app import db 
from app.dashboard import bp
from app.models import Article, Post,Role,Permissions,User
#from app.articles.forms import
#from app.dashboard.forms import Article

from app.decorators import admin_required, permission_required


@bp.route('/admin')
@login_required
@admin_required
def for_admins_only():
 return "For administrators!"





@bp.route('/moderator')
@login_required
@permission_required(Permissions.MODERATE_COMMENTS)
def for_moderators_only():
 return "For comment moderators!"


@bp.route('/dashboard',methods=['GET','POST'])
#@login_required
#permission_required(Permissions.ADMINISTRATOR)
def dashboard():
	articles=Article.query.all()
	if articles is None:
		flash('No articles yet')
	
	return render_template('dashboard/articles.html',articles=articles,title='Articles')


@bp.route('/post/<string:id>/',methods=['GET'])
#@login_required
def post(id):
	post =Article.query.filter_by(id = id).first()

	return render_template('dashboard/post.html',post=post)