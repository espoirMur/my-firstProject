import app
from flask import session,url_for,redirect,request,render_template
from flask_sqlalchemy import get_debug_queries
from flask_login import current_user
from flask import abort
from app import app_config
@app.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app_config.get("development").FLASKY_DB_QUERY_TIMEOUT:
             app.logger.warning(
               '  Slow query: % s\nParameters: % s\nDuration: % fs\nContext: % s\n' %
             (query.statement, query.parameters, query.duration,query.context
             ))
    return response


@app.route('/admin')
def adminPage():
    if not current_user.is_admin:
        abort(403)
    else:
        redirect('/admin')
    return redirect('/admin')
