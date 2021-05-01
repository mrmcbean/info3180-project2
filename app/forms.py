from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from wtforms.widgets.core import Input


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
