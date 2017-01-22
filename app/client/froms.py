from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,validators,SelectField
from wtforms.validators import DataRequired,EqualTo


class BuisnessInformation(FlaskForm):
    Company=StringField('Company Name ', validators=[DataRequired()])
    country = SelectField('Country', choices=[('Be', 'Belguim'), ('ROU', 'Roumania'), ('OTH', 'Others')])
    adress = StringField(label="Address", validators=[DataRequired()])
    Description = StringField('Buisness Description')
    phone = StringField('Phone Number', [validators.Regexp(r'^0[0-9]([ .-]?[0-9]{2}){4}$')])
