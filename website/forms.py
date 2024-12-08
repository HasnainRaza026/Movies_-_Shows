from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class Signup(FlaskForm):
    name = StringField('Enter Your Name', validators=[
        DataRequired(message="Please enter name."), 
        Length(max=120)
    ])
    email = StringField('Enter Email', validators=[
        DataRequired(message="Please enter email."), 
        Email(message="Please enter a valid email."),
        Length(max=120)
    ])
    password = PasswordField('Enter Password', validators=[
        DataRequired(message="Please enter a password."), 
        Length(min=8, max=20, message="Password must be between 8 and 20 characters.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    signup = SubmitField('Submit')


class Login(FlaskForm):
    email = StringField('Enter Email', validators=[
        DataRequired(message="Please enter email."), 
        Length(max=120)
    ])
    password = PasswordField('Enter Password', 
            validators=[DataRequired(message="Please enter password."), 
            Length(max=20)])
    login = SubmitField('Login')


class AddMovie(FlaskForm):
    title = StringField('Type movie name', validators=[DataRequired(message="Movie Title is required."), Length(max=120)])
    review = StringField('Give one sentence review', validators=[DataRequired(message="Review is required."), Length(max=20)])
    ranking = IntegerField('Add your ranking 1-10 (Optional)', validators=[Optional(), NumberRange(min=1, max=10)])
    add = SubmitField('Add')


class EditMovie(FlaskForm):
    review = StringField('Your Review', validators=[Optional(), Length(max=20)])
    ranking = IntegerField('Edit Ranking', validators=[Optional(), NumberRange(min=1, max=10)])
    edit = SubmitField('Edit')
