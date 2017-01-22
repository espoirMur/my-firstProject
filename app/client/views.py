from .. import db
from ..models import Employee
from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from . import client
@client.route("/client/AccountInfo")
def viewInfo():
    return render_template("/client/MyDashboard.html")
@client.route("/client/MakeOder")
def makeOrder():
    return render_template("/client/MyDashboard.html")