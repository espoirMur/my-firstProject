from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from ..models import Employee, WorkStation


class ClientAssignFormWSandEng(FlaskForm):
    """
    Form for admin to assign engineers and WorkSations to employees
    """
    Engineers = QuerySelectMultipleField(query_factory=lambda: Employee.query.filter_by(is_eng=True),
                                         get_label="names")
    WorkStation = QuerySelectField(query_factory=lambda: WorkStation.query.all(),
                                   get_label="name", allow_blank=True)
    submit = SubmitField('Submit')


class ClientAssignFormWs(FlaskForm):
    WorkStation = QuerySelectField(query_factory=lambda: WorkStation.query.all(),
                                   get_label="name", allow_blank=True)
    submit = SubmitField('Submit')
