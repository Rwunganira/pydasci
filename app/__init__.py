import logging 
from logging.handlers import RotatingFileHandler,SMTPHandler
import os
from flask import Flask,request,current_app
from flask_sqlalchemy import SQLAlchemy 
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin


#from flask_user import UserManager

db =SQLAlchemy()
admin = Admin()
migrate =Migrate(template_mode='bootstrap3')
login=LoginManager()
login.login_view='auth.login'
login.login_message=('Please login to access the page')
mail=Mail()
bootstrap=Bootstrap()
ckeditor = CKEditor()




def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    admin.init_app(app)
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app,db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    ckeditor.init_app(app)


    from  app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.articles import bp as articles_bp
    app.register_blueprint(articles_bp)
    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    

 


    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            #logger = logging.getLogger(__name__)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
                file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
                file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
    return app

from app import models

