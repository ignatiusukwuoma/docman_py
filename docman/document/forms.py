from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateDocument(FlaskForm):
    """
    Form for users to create new document
    """
    title = StringField('Title', validators=[DataRequired()])
    access = SelectField('Access',
                         choices=[('public', 'Public'), ('private', 'Private'), ('role', 'Role')],
                         validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

