from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
import flask_login as login
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from ..models import Project
from flask_admin._backwards import ObsoleteAttr


class ProjectModelView(ModelView):
    can_delete = True  # disable model deletion
    page_size = 50  # the number of entries to display on the list view
    column_exclude_list = ['Password Hash']

    def is_accessible(self):
        return login.current_user.is_admin


class EmployeeModelView(ModelView):
    can_create = True
    can_edit = True
    can_delete = False
    page_size = 20
    def is_accessible(self):
        return login.current_user.is_admin


class ProjectsViews(BaseView):
    title = 'Project'
    @expose('/')
    def index(self):
        projects = Project.query.filter_by(status='pending')
        return self.render('/admin/projects.html', projects=projects)

    def is_accessible(self):
        return login.current_user.is_admin


class AdminIndex(AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_admin
