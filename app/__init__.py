from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  config import app_config
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy() #initialisation de la BD
log_manager =LoginManager()

def create_app(config_name):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    log_manager.init_app(app)
    log_manager.login_message="You must be logged to see this page"
    log_manager.login_view = "auth.login"
    migrate = Migrate(app,db) #Migrate object to databases
    from app import models
    return app

