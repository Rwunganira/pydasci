
from app.main import bp
from datetime import datetime
from flask import render_template, flash, redirect, url_for,current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import PostForm




# @bp.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()
#     g.locale = str(get_locale())
    
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    # if form.validate_on_submit():
        
    #     post = Post(body=form.post.data, author=current_user)
    #     db.session.add(post)
    #     db.session.commit()
    #     flash(('Your comment  is now live!'))
    #     return redirect(url_for('main.index'))
    return render_template('index.html', title=('Home'))

   
