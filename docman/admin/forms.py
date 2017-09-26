from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RoleForm(FlaskForm):
    """
    Form to add a new role
    """
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
