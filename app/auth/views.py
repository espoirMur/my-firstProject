from flask import flash, redirect, render_template, url_for, request,session
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .froms import LoginForm, RegistrationForm,ChangeEmailForm,ResetPasswordForm,ResetPasswordFormRequest
from .. import db
from ..models import Employee
from flask_sqlalchemy import get_debug_queries
from app import app_config
import os
import app
from datetime import date

from ..controller import send_mail_flask,AuthSignIn


# template_path=os.path.join(os.path.dirname(__file__), 'new_user')
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(names=form.names.data,
                            username=form.username.data,
                            email=form.email.data,
                            password=form.password.data,
                            registration_date=date.today())
        try :
            db.session.add(employee)
            db.session.commit()
            token = employee.generate_confirmation_token()
            send_mail_flask(employee.email, 'Confirm Your Account', 'mail/new_user', employee=employee, token=token)
            flash("Registration sucessfull a confirmation mail has been send to your account")
            login_user(employee,True)
            return redirect(url_for('auth.unconfirmed'))
        except Exception:
            db.session.delete(employee)
            db.session.commit()
            flash("Error While sending Confirmation mail Try again",category='error')
            return redirect(url_for('auth.register'))
            # redirect to loggin page
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the appropriate page according to this role
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('client.myDashboard'))
        # when login details are incorrect
        else:
            flash('Invalid email or password.',category="error")

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))


@auth.route('/confirm/<token>')
@login_required
def confirme(token):
    if current_user.confirmed:
        flash("You are already confirmed")
        return redirect(url_for('home.homepage'))
    if current_user.confirm_token(token):
        flash("You have confirmed your account")
    else:
        flash("Your confirmation link is invalid or expired", category="error")
    return redirect(url_for('home.homepage'))

@auth.before_app_request
def before_request():
    #ceci se passe avant toutes les requete une fois l'utilisateurt connecte et verifie si l'utilisateur est authentique
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.':
        session.clear()
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('client.myDashboard'))
    return render_template('auth/unconfirmed.html',employee=current_user)

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail_flask(current_user.email,'Confirm Your Account', 'mail/new_user',employee=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('home.homepage'))

@auth.route('/change-email', methods=['GET','POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email=form.email.data
            token=current_user.generate_email_change_token(new_email)
            send_mail_flask(new_email, 'Confirm your email address','mail/change_email',employee= current_user, token = token)
            flash('An email with instructions to confirm your new email '+ 'address has been sent to you.')
            return redirect(url_for('home.homepage'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_mail.html", form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.confirm_mail_andChange(token):
        flash ("Your email adress has beeen update")
    else:
        flash("Invalid request",category="error")
    return redirect(url_for("home.homepage"))

@auth.route('/reset',methods=['GET','POST'])
def reset_password_request():
    form=ResetPasswordFormRequest()
    email = form.email.data
    if form.validate_on_submit():
        if form.validate_mail(form.email):
            employee = Employee.query.filter_by(email=email).first()
            token=employee.generate_password_change_token()
            send_mail_flask(email, 'Change PassWord', 'mail/change_password',token=token,employee=employee)
            flash('An email with instructions to change your password has been sent to you.')
            return redirect(url_for('home.homepage'))
        else:
            flash("email not find please register" ,category="error")
    return render_template("auth/change_password.html",form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for("home.homepage"))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is None:
            flash("email is incorrect ",category="error")
            return redirect(url_for('auth.reset_password'))
        if employee.confirm_Password_andChange(token,form.password.data):
            flash ("Your Password adress has beeen update")
            return redirect(url_for('auth.login'))
        else:
            flash("Invalid request email not valid",category="error")
    return render_template("auth/change_password.html",form=form)

@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home.homepage'))
    oauth = AuthSignIn.get_provider(AuthSignIn,provider)
    print oauth
    return oauth.authorize()
@auth.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('client.myDashboard',employee=current_user))
    oauth= AuthSignIn.get_provider(AuthSignIn,provider)
    social_id,username,email,names=oauth.callback()
    if email is None:
        flash("Authentification failed", category='error')
        return redirect(url_for('home.register'))
    user = Employee.query.filter_by(email=email,social_id=social_id).first()
    if not user:
        user = Employee(email=email, username=username, names=names, social_id=social_id, confirmed=True)
        db.session.add(user)
        db.session.commit()
        login_user(user, True)
    else:
        flash("Authentification succesfull")
        login_user(user, True)
        return redirect(url_for('client.myDashboard'))
    flash("Authentification succefull")
    return redirect(url_for('home.homepage'))

""""@auth.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app_config.get("development").FLASKY_DB_QUERY_TIMEOUT:
             app.logger.warning(
               '  Slow query: % s\nParameters: % s\nDuration: % fs\nContext: % s\n' %
             (query.statement, query.parameters, query.duration,query.context
             ))
    return response"""
