from flask import render_template ,abort
from flask_login import login_required,current_user
from . import home
#from decorator import permision_required,admin_required
@home.route('/')
def homepage():
    return  render_template('home/index.html',title="Welcome")
@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title="Dashboard")
@home.route('/admin/dashboard')
@login_required
#the route is protected you must be login as admin to see this page
def admin_dashboard():
    #Non-admin can't acess this pag:*
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html',title="Dashboard")
