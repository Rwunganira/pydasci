from flask import render_template, url_for,redirect,flash,request
from app import db
from app.articles import bp
from app.articles.forms import ArticleForm

from flask_login import current_user, login_required
from app.models import Article
from app.decorators import permission_required
from app.models import Permissions


@bp.route('/article', methods=['GET', 'POST'])
@login_required
def article():
    if  current_user.is_administrator:
        form = ArticleForm()
        if form.validate_on_submit():
            article = Article(title=form.title.data,text1=form.text1.data)
            db.session.add(article)
            db.session.commit()
            flash('Article registered')
            return redirect(url_for('dashboard.dashboard'))
        return render_template('articles/article.html', title=('Article'), form=form)
    return render_template('auth/login.html')