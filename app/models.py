from datetime import datetime
from flask_login import UserMixin,AnonymousUserMixin,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from app import db , login,admin 
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect,url_for


class User(UserMixin,db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True, index=True)
    email = db.Column(db.String,unique=True,index=True)
    password_hash = db.Column(db.String(128))
    last_seen=db.Column(db.DateTime,default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    user_role = db.Column(db.Integer,db.ForeignKey('role.id'))
    
    def __init__(self, **kwargs): # takes the user variables
        super(User, self).__init__(**kwargs)
        if self.role is  None:# if role in not defined 
            if self.email == current_app.config['ADMINS']: # check if the email is the same as in flask admin
                self.role = Role.query.filter_by(permissions=0xff).first()#assign the role to admin
            elif self.role is None:
                self.role= Role.query.filter_by(default=True).first()#otherwise assign the role of default


    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User{}>'.format(self.username) 
    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions
    def is_administrator(self):
        return self.can(Permissions.ADMINISTRATOR)
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False
login_manager.anonymousUser = AnonymousUser


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,unique=True, index=True)
    email = db.Column(db.String,unique=True,index=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    art_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,unique=True, index=True)
    text1 = db.Column(db.String,unique=True,index=True)

    comment = db.relationship('Post', backref='comment', lazy='dynamic')

    

    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return '<Article {}>'.format(self.title)

class Permissions:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTRATOR = 0xff
class Role(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name  = db.Column(db.String(64),unique = True)
    default = db.Column(db.Boolean,default = True, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')
    @staticmethod
    def insert_roles():
        roles = {'User':(Permissions.FOLLOW| Permissions.COMMENT |Permissions.WRITE_ARTICLES,True),
        'Moderator':(Permissions.FOLLOW| Permissions.COMMENT |Permissions.WRITE_ARTICLES| Permissions.MODERATE_COMMENTS,False),
        'Administator':(0xff,False )}
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name = r) 
            role.permissions = roles[r][0] 
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit() 
class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_administrator:
            return True

    def is_inaccessible(self,name,**kwargs):
        return redirect(url_for('login'))
admin.add_view(MyModelView(User, db.session, category="Team"))
admin.add_view(MyModelView(Role, db.session, category="Team"))
admin.add_view(MyModelView(Article, db.session, category="Team"))
admin.add_view(MyModelView(Post, db.session, category="Team"))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
