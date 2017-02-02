from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,validators,SelectField,IntegerField,FormField,TextField
from wtforms.validators import DataRequired,EqualTo,length,Email,ValidationError,Regexp


class Address(FlaskForm):
     line1= StringField('Address Line 1 ', validators=[DataRequired()])
     line2 = StringField('Address Line 2 ')
     city = StringField('City/Town/Village', validators=[DataRequired()])
     state = StringField('State/Province/Region', validators=[DataRequired()])
     postal_code=StringField('Postal code ', validators=[DataRequired()])

     def __init__(self, *args, **kwargs):
         #We need to desactivate token evaluation
         kwargs['csrf_enabled'] = False
         super(Address, self).__init__(*args, **kwargs)
class BuisnessInformation(FlaskForm):
    company=StringField('Company Name ', validators=[DataRequired()])
    companySite=StringField('Company Website')
    country = SelectField('Country', choices=[('Be', 'Belguim'), ('ROU', 'Roumania'), ('OTH', 'Others')])
    description = StringField('Buisness Description')
    phone = StringField('Phone Number', validators=[Regexp(r'^[+,0][0-9]{2}')])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(BuisnessInformation, self).__init__(*args, **kwargs)

class AccountInfoFrom(FlaskForm):
    comapanyInfo=FormField(BuisnessInformation)
    address=FormField(Address)
    submit = SubmitField('Validate')
class EditAdress(FlaskForm):
    line1 = StringField('Address Line 1 ', validators=[DataRequired()])
    line2 = StringField('Address Line 2 ')
    city = StringField('City/Town/Village', validators=[DataRequired()])
    state = StringField('State/Province/Region', validators=[DataRequired()])
    postal_code = StringField('Postal code ', validators=[DataRequired()])
    submit=SubmitField('Validate')
class EditComapny(FlaskForm):
    companyName = StringField('Company Name ', validators=[DataRequired()])
    website = StringField('Company Website')
    country = SelectField('Country', choices=[('Be', 'Belguim'), ('ROU', 'Roumania'), ('OTH', 'Others')])
    description = StringField('Buisness Description')
    submit=SubmitField('Validate')


class ProjectInfo(FlaskForm):
    type = SelectField('Type of Service', choices=[('frame instance only', 'frame instance only'),
                                                   ('frame instance and engineer', 'frame instance and engineer')],
                       validators=[DataRequired()])
    numberOfEngs = IntegerField('Number of Enginners', default=0)
    Submit = SubmitField('Validate')
