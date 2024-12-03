from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional

class AddMovie(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired(message="Movie Title is required."), Length(max=120)])
    review = StringField('Your Review', validators=[DataRequired(message="Review is required."), Length(max=20)])
    ranking = IntegerField('Add Ranking 1-10 (Optional)', validators=[Optional(), NumberRange(min=1, max=10)])
    add = SubmitField('Add')

class EditMovie(FlaskForm):
    review = StringField('Your Review', validators=[Optional(), Length(max=20)])
    ranking = IntegerField('Edit Ranking', validators=[Optional(), NumberRange(min=1, max=10)])
    edit = SubmitField('Edit')
