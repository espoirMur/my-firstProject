from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,validators,SelectField,IntegerField,FormField,TextField
from wtforms.validators import DataRequired,EqualTo,length,Email,ValidationError

class Address(FlaskForm):
     line1= StringField('Address Line 1 ', validators=[DataRequired()])
     line2 = StringField('Address Line 2 ')
     city = StringField('City/Town/Village', validators=[DataRequired()])
     state = StringField('State/Province/Region', validators=[DataRequired()])
     PostalCode=StringField('Postal code ', [validators.DataRequired()])
class BuisnessInformation(FlaskForm):
    company=StringField('Company Name ', validators=[DataRequired()])
    companySite=StringField('Company Website')
    country = SelectField('Country', choices=[('Be', 'Belguim'), ('ROU', 'Roumania'), ('OTH', 'Others')])
    Description = StringField('Buisness Description')
    phone = StringField('Phone Number', [validators.Regexp(r'^[+,0][0-9]{2}')])

class AccountInfoFrom(FlaskForm):

    comapanyInfo=FormField(BuisnessInformation)
    address=FormField(Address)
    submit = SubmitField('Validate')

