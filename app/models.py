from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from app import db, log_manager,app_config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import event

#for generating password token for confirmation

class Departement(db.Model):
    _tablename__ = 'departement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='departement', lazy='dynamic')
    def __repr__(self):
        return '<Department: {}>'.format(self.name)
class Role(db.Model):
    __tablename__='role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    permission = db.Column(db.Integer)
    default=db.Column(db.Boolean,default=False,index=True)
    employees = db.relationship('Employee', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
    @staticmethod
    def insert_roles():
        roles={'user':(Permission.FOLLOW |Permission.COMMENT |Permission.WRITE_ARTICLES,True),
               'Moderator':(Permission.FOLLOW | Permission.COMMENT |Permission.WRITE_ARTICLES |Permission.MODERATE_COMMENTS,False),
               'Administrator':(0xff,False)}
        for r in roles :
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.permission =roles[r][0]
            role.default=roles[r][1]
            db.session.add(role)
        db.session.commit()
class Employee(UserMixin,db.Model):
    __tablename__='employee'
    id = db.Column(db.Integer, primary_key=True )
    email = db.Column(db.String(60),index=True,unique=True)
    username = db.Column(db.String(60),index=True,unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    departement_id = db.Column(db.Integer,db.ForeignKey('departement.id'))
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    is_admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
    social_id=db.Column(db.String(64),nullable=True,unique=True)
    def generate_confirmation_token(self,expiration=3600):
        s=Serializer("YouCantSeeMee.123",expiration)
        return s.dumps({'confirm':self.id})
    def confirm_token(self,token):
        s=Serializer("YouCantSeeMee.123")
        try:
            data=s.loads(token)
        except:
            print "An error occur in token confirmation"
            return False
        if data.get('confirm')!=self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        db.session.commit()
        return True
    def generate_email_change_token(self,new_email,expiration=3600):
        s = Serializer("YouCantSeeMee.123", expiration)
        return s.dumps({'change_mail': self.id,'new_mail':new_email})
    def confirm_mail_andChange(self, token):
        s = Serializer("YouCantSeeMee.123")
        try:
            data = s.loads(token)
        except:
            print "An error occur in token confirmation"
            return False
        if data.get('change_mail') != self.id:
            return False
        new_mail=data.get('new_mail')
        if new_mail is None:
            return False
        if self.query.filter_by(email=new_mail).first() is not None:
            return False
        self.email=new_mail
        db.session.add(self)
        db.session.commit()
        return True
    def generate_password_change_token(self,expiration=3600):
        s = Serializer("YouCantSeeMee.123", expiration)
        return s.dumps({'confirm':self.id,'email':self.email})

    def confirm_Password_andChange(self, token, new_pass):
        s = Serializer("YouCantSeeMee.123")
        try:
            data = s.loads(token)
        except:
            print "An error occur in token confirmation"
            return False
        if data.get('confirm') != self.id or data.get('email') !=self.email:
            return False
        self.password=new_pass
        db.session.add(self)
        db.session.commit()
        return True
    @property
    def password(self):
        raise AttributeError('Password is not readable')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password (self,password):
        return check_password_hash(self.password_hash,password)
    def __init__(self,**kwargs):
        super(Employee,self).__init__(**kwargs)
        if self.role_id is None:
            if self.email==app_config.get('development').FLASKY_ADMIN:
                self.role_id=Role.query.filter_by(permission=0xff).first().id
            if self.role_id is None:
                self.role_id = Role.query.filter_by(default=True).first().id
    """def can(self,permissions):
        return self.role_id is not None and (self.role_id.permissions & permissions)==permissions
    def is_admin(self):
        return self.can(Permission.ADMINISTER)"""
    def __repr__(self):
        return '<Employee: {}>'.format(self.username)
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80
"""class AnonymuosUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    def is_admin(self):
        return False
    log_manager.anonymous_user=AnonymousUser


class OperationStatus(db.Model):
    __tablename__='operationStatus'
    id =db.Column(db.Integer,primary_key=True)
    code=db.Column('code',db.String(20),nullable=True)
    service=db.Column(db.String(20),nullable=False,default='facebook')
class Operation(db.Model):
    __tablename__='operation'
    id = db.Column(db.Integer, primary_key=True)
    operationStatus_id=db.Column(db.Integer,db.ForeignKey('operationStatus.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    status = db.relationship("operationStatus",foreign_keys=operationStatus_id)
    employees=db.relationship("employee",foreign_keys=employee_id)
event.listen(
        OperationStatus.__table__, 'after_create',
        DDL(INSERT INTO  operationStatus (id,code) VALUES (1,'pending'),(2, 'ok'),(3, 'error'); )
)"""


@log_manager.user_loader
#call back fonction to load the user who is login from the database
def load_user(user_id):
    return  Employee.query.get(int(user_id))