from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  config import app_config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import smtplib
db = SQLAlchemy() #initialisation de la BD
log_manager =LoginManager()
mail = Mail()
"""smtpserver = smtplib.SMTP(app_config.get('development').MAIL_SERVER, app_config.get('development').MAIL_PORT)
smtpserver.ehlo()
smtpserver.starttls()"""
def create_app(config_name):
    #application factory
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    mail.init_app(app) #Pour l'envoi des mails
    log_manager.init_app(app)
    log_manager.login_message="You must be logged to see this page"
    log_manager.login_view = "auth.login" #la vue qui gere les login
    migrate = Migrate(app,db) #Migrate object to databases
    Bootstrap(app)
    from app import models
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint,url_prefix='/admin')
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    return app
