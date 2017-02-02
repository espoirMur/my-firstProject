from flask import Blueprint, redirect, request, url_for, abort
from app import db
from ..models import Employee, Project, Working_on, WorkStation
from . import views
from flask_admin import Admin
from .views import *
from .froms import *

admin = Admin(name='Admin Dashboard', template_mode='bootstrap3', index_view=AdminIndex())  # for administration tasks

# for handling administratives task of our application
project_view = ProjectsViews("Pending Projects")
admin.add_views(EmployeeModelView(WorkStation, db.session))
admin.add_views(ProjectModelView(Project, db.session))
admin.add_views(project_view)
adminblue = project_view.create_blueprint(admin)


# admin.add_views(AnalyticsView)

@adminblue.route("/assign/engineers/<int:id>", method=['GET', 'POST'])
def assignEngineer(id):
    return render_template("/admin/projects.html")
