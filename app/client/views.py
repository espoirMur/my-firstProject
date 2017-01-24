from .. import db
from ..models import Employee
from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from . import client
from .froms import AccountInfoFrom
@client.route("/client/AccountInfo")
@login_required
def viewInfo():
    return render_template("/client/MyDashboard.html")
@client.route("/client/MyDashboard")
@login_required
def myDashboard():
    return render_template("/client/MyDashboard.html",employee=current_user)
@client.route("/client/makeOrder")
@login_required
def makeOrder():
    return render_template("/client/MyDashboard.html",employee=current_user)
@login_required
@client.route('/client/AddInfo',methods=['GET', 'POST'])
def addInfo():
    form =AccountInfoFrom()
    if form.validate_on_submit():
        """company=form.comapanyInfo.data.get('company')
        companySite = form.comapanyInfo.data.get('companySite')
        country = form.comapanyInfo.data.get('country').choice
        print "-----------------------------------------------"
        print company+" "+companySite+" "+country"""
        print "Validation Succesfull"
        print "-----------------------------------------------"
    return render_template("/client/AddInfo.html",form=form,title="Add Information")