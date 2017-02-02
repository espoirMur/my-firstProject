from . import eng
from flask_login import login_required, current_user
from ..models import Project,Employee,WorkStation
from flask import render_template, redirect, flash, url_for, abort, logging
from ..admin import ClientAssignFormWs, ClientAssignFormWSandEng
from .. import db
from ..controller import send_mail_flask


@login_required
@eng.route('/eng/assignToProject/<int:id>', methods=['GET', 'POST'])
def assignToProject(id):
    project = Project.query.get_or_404(id)
    print '---------------------------------------------------'
    print type(project.workStation)
    print '---------------------------------------------------'
    if project.type == 'frame instance only':  # for the case of project is for an employee only
        form = ClientAssignFormWs()
        if form.validate_on_submit():
            workStations = form.WorkStation.data
            project.workStation = workStations
            try:
                send_mail_flask(to=[project.employee.email], subject="You Have a New project ",
                                template='mail/new_Project',
                                project=project)  # sending mail to employee
                project.status = 'onProgress'
                db.session.add(project)
                db.session.commit()
                flash("Workstations Succesfull assign to project A confirmation mail has been send to them")
                return redirect('/admin/projectsviews/')
            except Exception as e:
                flash('an Error occurs When sending mail try again', category='error')
                return render_template('/admin/AssignEngineers.html', project=project, form=form)
    elif project.type == "frame instance and engineer":
        form = ClientAssignFormWSandEng()
        if form.validate_on_submit():
            workStations = form.WorkStation.data
            engineers = form.Engineers.data
            if len(engineers) < project.numberOfEngs:
                flash('The client need more ENGINEERS ', category='error')
                return render_template('/admin/AssignEngineers.html', project=project, form=form)
            project.engs = engineers
            project.workStation = workStations
            try:
                eng_mail = []  # contains mail of engineers
                for engi in engineers:
                    eng_mail.append(engi.email)
                send_mail_flask(eng_mail, 'You Have a New project ', 'mail/new_Project',
                                project=project)  # sending mail to employee
                project.status = 'onProgress'
                db.session.add(project)
                db.session.commit()
                flash("Engineers Succesfull assign to project A confirmation mail has been send to them")
                return redirect('/admin/projectsviews/')
            except Exception as e:

                flash('an Error occurs When sending mail try again', category='error')
                return render_template('/admin/AssignEngineers.html', project=project, form=form)
    return render_template('/admin/AssignEngineers.html', project=project, form=form)


@eng.route("/eng/MyDashboard")
@login_required
def myDashboard():
    check_eng()
    return render_template("/eng/MyDashboard.html", employee=current_user)


def check_eng():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_eng:
        abort(403)


@login_required
@eng.route('/eng/contactClient/<int:id>', methods=['GET', 'POST'])
def contactClient(id):
    check_eng()
    project = Project.query.get_or_404(id)
    client_mail=project.employee.email
    try:
        send_mail_flask(to=client_mail, subject="An Engineer Respond about You're Project", template='mail/new_Project',
                        project=project)
    except Exception as e:
        pass

    return render_template("/eng/MyDashboard.html", employee=current_user)


@login_required
@eng.route('/eng/runWorkStation/<int:id>', methods=['GET', 'POST'])
def runInstance(id):
    check_eng()
    workstation = WorkStation.query.get_or_404(id)
    return render_template('client/StartFrame.html', workstation=workstation)
