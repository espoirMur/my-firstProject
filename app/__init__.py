from flask import Flask, render_template, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from  config import app_config
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import smtplib,os
db = SQLAlchemy() #initialisation de la BD
log_manager =LoginManager()
mail = Mail()

"""smtpserver = smtplib.SMTP(app_config.get('development').MAIL_SERVER, app_config.get('development').MAIL_PORT)
smtpserver.ehlo()
smtpserver.starttls()"""
def create_app(config_name):
    #application factory
        if os.getenv('FLASK_CONFIG') == "production":
            app = Flask(__name__)
            app.config.from_object(app_config[config_name])
            app.config.update(
                SECRET_KEY=os.getenv('SECRET_KEY'),
                SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
            )
        else:
            app = Flask(__name__, instance_relative_config=True)
            app.config.from_object(app_config[config_name])
            app.config.from_pyfile('config.py')

    from .admin import admin
    admin.init_app(app)
        db.init_app(app)
        mail.init_app(app)  # Pour l'envoi des mails
        log_manager.init_app(app)
        log_manager.login_message = "You must be logged to see this page"
        log_manager.login_view = "auth.login"  # la vue qui gere les login
        migrate = Migrate(app, db)  # Migrate object to databases
        Bootstrap(app)
        from app import models
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        from .home import home as home_blueprint
        app.register_blueprint(home_blueprint)
        from .client import client as client_blueprint
        app.register_blueprint(client_blueprint)
        from .engineer import eng as eng_blueprint
        app.register_blueprint(eng_blueprint)

        # for error handling
        @app.errorhandler(403)
        def forbidden(error):
            return render_template('errors/403.html', title='Forbidden'), 403

        @app.errorhandler(404)
        def page_not_found(error):
            return render_template('errors/404.html', title='Page Not Found'), 404

        @app.errorhandler(500)
        def internal_server_error(error):
            return render_template('errors/500.html', title='Server Error'), 500

    @app.route('/admin')
    def adminPage():
        if not current_user.is_admin:
            abort(403)
        else:
            redirect('/admin')
        return redirect('/admin')

        return app




