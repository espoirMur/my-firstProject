from .. import db
from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from . import client
from .froms import AccountInfoFrom, EditAdress, EditComapny, ProjectInfo
from ..models import Company, Employee, Address, Project, WorkStation
from datetime import date
@client.route("/client/AccountInfo")
@login_required
def viewInfo():
    return render_template("/client/MyDashboard.html")
@client.route("/client/MyDashboard")
@login_required
def myDashboard():
    return render_template("/client/MyDashboard.html",employee=current_user)


@client.route("/client/makeProject", methods=['GET', 'POST'])
@login_required
def makeProject():
    form = ProjectInfo()
    if request.method == 'GET':
        form.numberOfEngs.data == 0
    if form.validate_on_submit():
        project = Project(type=form.type.data,
                          numberOfEngs=form.numberOfEngs.data,
                          status='pending',
                          date=date.today())
        employee = current_user
        db.session.add(project)
        employee.projects.append(project)
        db.session.commit()
        flash("A New Project Has Been create you will be notifity When ENginner will be asign")
        return redirect(url_for('client.myDashboard'))
    return render_template("/client/NewProject.html", title='New Project', form=form)
@login_required
@client.route('/client/AddInfo/<int:id>',methods=['GET', 'POST'])
def addInfo(id):
    employee= Employee.query.get_or_404(id)
    form =AccountInfoFrom(request.form)
    if form.validate_on_submit():
        comp = Company(companyName=form.comapanyInfo.data.get('company'),
                       website=form.comapanyInfo.data.get('companySite'),
                       country=form.comapanyInfo.data.get('country'),
                       description=form.comapanyInfo.data.get('description'))
        address = Address(line1=form.address.data.get('line1'),
                          line2=form.address.data.get('line2'),
                          city=form.address.data.get('city'),
                          state=form.address.data.get('state'),
                          postal_code=form.address.data.get('postal_code'))
        phone = form.comapanyInfo.data.get('phone')
        db.session.add(address)
        db.session.add(comp)
        employee.phone = phone
        employee.address = address
        employee.company = comp
        db.session.add(employee)
        db.session.commit()
        flash("Information Sucessfull update")
        return redirect(url_for('client.myDashboard'))
    return render_template("/client/AddInfo.html",form=form,title="Add Information")


@login_required
@client.route('/client/editAdress/<int:id>',methods=['GET', 'POST'])
def editAdrees(id):
    employee= Employee.query.get_or_404(id)
    address=Address.query.get_or_404(employee.address.id)
    form=EditAdress(obj=address)
    if request.method == 'GET':
        form.city.data=address.city
        form.line1.data = address.line1
        form.line2.data = address.line2
        form.postal_code.data= address.postal_code
    if form.validate_on_submit():
        form.populate_obj(address)
        employee.address = address
        db.session.add(employee)
        db.session.commit()
        flash("information succefull add")
        return redirect(url_for('client.myDashboard'))
    return render_template("/client/AddInfo.html",form=form,title="Edit Information")
@login_required
@client.route('/client/editCompany/<int:id>',methods=['GET', 'POST'])
def editCompany(id):
    employee= Employee.query.get_or_404(id)
    company=Company.query.get_or_404(employee.company.id)
    form=EditComapny(obj=company)
    if request.method == 'GET':
        form.country.data = company.country
        form.companyName.data = company.companyName
        form.website.data = company.website
        form.description.data=company.description
    if form.validate_on_submit():
        form.populate_obj(company)
        print employee.company.companyName
        employee.company = company
        db.session.add(employee)
        db.session.commit()
        flash("information succefull add")
        return redirect(url_for('client.myDashboard'))
    return render_template("/client/AddInfo.html",form=form,title="Edit Information")


@login_required
@client.route('/client/contactEngineers/<int:id>', methods=['GET', 'POST'])
def contactEngi(id):
    engineer = Employee.query.filter_by(is_eng=True, id=id).first()
    return render_template('client/contactEngineer.html', engineer=engineer)


@login_required
@client.route('/client/runWorkStation/<int:id>', methods=['GET', 'POST'])
def runInstance(id):
    workstation = WorkStation.query.get_or_404(id)
    return render_template('client/StartFrame.html', workstation=workstation)
