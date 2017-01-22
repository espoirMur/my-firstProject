from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,SelectField,IntegerField,validators,FormField
from wtforms.validators import DataRequired, Email, EqualTo
from ..models import Employee
from wtforms.fields.html5 import TelField
from wtforms_alchemy import PhoneNumberField



class PersonalInformation(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = PhoneNumberField(region='FI', display_format='national')
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
class BuisnessInformation(FlaskForm):
    Company=StringField('Company Name ', validators=[DataRequired()])
    country = SelectField('Country', choices=[('Be', 'Belguim'), ('ROU', 'Roumania'), ('OTH', 'Others')])
    adress = StringField(label="Address", validators=[DataRequired()])
    Description = StringField('Buisness Description')


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    names = StringField('Names', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = PhoneNumberField(region='FI', display_format='national')
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    def validate_mail(self,field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError("email already in use")
class ResetPasswordFormRequest(FlaskForm):
    email = StringField("Your mail",validators=[DataRequired(),Email()])
    submit=SubmitField("Continue")
    def validate_mail(self,field):
        if Employee.query.filter_by(email=field.data).first() is None:
            raise ValidationError("You are not Registred Yet in Our System")
        return True
class ResetPasswordForm(FlaskForm):
    email = StringField("Your mail", validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired(),EqualTo('confirm_password'),])
    confirm_password = PasswordField('Confirm Password')
    submit=SubmitField("Reset password")
