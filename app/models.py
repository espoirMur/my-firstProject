from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from app import db, log_manager

class Departement(db.Model):
    _tablename__ = 'departement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='Departement', lazy='dynamic')
    def __repr__(self):
        return '<Department: {}>'.format(self.name)
class Role(db.Model):
    __tablename__='roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
class Employee(UserMixin,db.Model):
    __tablename__='employees'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60),index=True,unique=True)
    username = db.Column(db.String(60),index=True,unique=True)
    first_name = db.Column(db.String(60), index=True)
    Last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    departement_id = db.Column(db.Integer,db.ForeignKey('departement.id'))
    role_id = db.column(db.Integer,db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    @property
    def password(self):
        raise AttributeError('Password is not readable')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password (self,password):
        return check_password_hash(self.password_hash,password)
    def __repr__(self):
        return '<Employee: {}>'.format(self.username)
@log_manager.user_loader
def load_user(user_id):
    return  Employee.query.get(int(user_id))

