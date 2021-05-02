from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, InputRequired, Email
from wtforms.widgets.core import Input


class NewUserForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField ('Password', validators=[InputRequired()])
    fullname = StringField('Fullname', validators=[InputRequired()])
    email = StringField('Email', validators= [InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    biography = TextAreaField ("Biography", validators=[InputRequired()])
    photo = FileField('Upload Photo', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'Images Only!'])])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class AddNewCarForm(FlaskForm):
    make = StringField('Make', validators=[InputRequired()])
    model = StringField('Model', validators=[InputRequired()])
    colour = StringField('Colour', validators=[InputRequired()])
    year = StringField('Year', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    carType = SelectField('Car Type', choices=[("None","Select Type"), ("SUV", "SUV"), ("Sedan", "Sedan"),("Hybrid","Hybrid"),("Convertible", "Convertible"),("Sportscar", "Sportscar")], validators=[DataRequired()])
    transmission = StringField('Transmission', choices=[("None", "Select Transmission"), ("Automatic", "Automatic"), ("Manual","Manual")])
    description = TextAreaField('Description', validators=[InputRequired()])
    photo = FileField('Upload Photo', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only!')])


    class ExplorePageForm(FlaskForm):
        makeInquiry = StringField('Make', validators=[InputRequired()])
        modelInquiry = StringField('Model', validators=[InputRequired()])
        