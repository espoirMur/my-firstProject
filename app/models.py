from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from app import db, log_manager,app_config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import date

#for generating password token for confirmation
Working_on =db.Table(
    'Working_on',
    db.Column('Eng_id',db.Integer,db.ForeignKey('employee.id')),
    db.Column('Project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('Start_Date',db.Date),
    db.Column('End_Date',db.Date)
)
class Address(db.Model):
    _tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    line1 = db.Column(db.String(60), index=True,nullable=True)
    line2 = db.Column(db.String(60), nullable=True)
    city =db.Column(db.String(60), nullable=True)
    state =db.Column(db.String(60), nullable=True)
    postal_code=db.Column(db.String(60))
class Company(db.Model):
    __tablename__='company'
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(64), nullable=True)
    website = db.Column(db.String(64), nullable=True)
    description=db.Column(db.String(128), nullable=True)
    country = db.Column(db.String(64), nullable=True, unique=False)


class Project(db.Model):
    _tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('pending', 'onProgress', 'WorkInProgress', 'completed'), nullable=False)
    type = db.Column(db.Enum('frame instance only', 'frame instance and engineer'), nullable=False)
    date = db.Column(db.Date)
    numberOfEngs = db.Column(db.Integer)
    workStation_id=db.Column(db.Integer,db.ForeignKey('workStation.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))  # if clients will save oders placed
    employee = db.relationship('Employee', back_populates="projects", foreign_keys=[employee_id])
    engs=db.relationship("Employee",secondary=Working_on,back_populates="worksOn")
    workStation = db.relationship('WorkStation', back_populates='projects')
    def validate(self):
        pass
    def change(self):
        pass
    def delete(self):
        pass
    def __repr__(self):
        return '<Project: {}>'.format(self.id)

class WorkStation(db.Model):
    __tablename__='workStation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    GPU=db.Column(db.Integer)
    RAM=db.Column(db.Integer)
    Disk=db.Column(db.Integer)
    projects = db.relationship('Project', back_populates='workStation')
    def __repr__(self):
        return '{}'.format(self.name)

class Employee(UserMixin,db.Model):
    __tablename__='employee'
    id = db.Column(db.Integer, primary_key=True )
    email = db.Column(db.String(60),index=True,unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    names = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_eng = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
    social_id=db.Column(db.String(64),nullable=True,unique=True)
    phone = db.Column(db.String(64), nullable=True, unique=False)
    registration_date=db.Column(db.Date,nullable=False,default=date.today())
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    address_id=db.Column(db.Integer, db.ForeignKey('address.id'))
    validate_id = db.Column(db.Integer, db.ForeignKey('project.id'))  # if admin will save projects validate by him
    projects = db.relationship('Project', foreign_keys=[Project.employee_id], )  # contatins projects placed for clients
    worksOn = db.relationship('Project', secondary=Working_on,
                              back_populates="engs")  # contains projects an engineer is working on
    validate = db.relationship('Project', foreign_keys=[validate_id])  # contains projects validates by an admin
    address=db.relationship('Address', foreign_keys=[address_id]) #contain user adress
    company = db.relationship('Company', foreign_keys=[company_id])
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


    def __repr__(self):
        return '{}'.format(self.username)
    def validateOder(self):
        #for admin
        pass
    def view_tasks(self):
        #for engineer
        pass
    def assignToEngineer(self):
        pass

@log_manager.user_loader
#call back fonction to load the user who is login from the database
def load_user(user_id):
    return  Employee.query.get(int(user_id))