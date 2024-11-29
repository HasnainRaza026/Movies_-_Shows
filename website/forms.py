from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange

class EditForm(FlaskForm):
    my_review = StringField(
        'Your Review',
        validators=[
            DataRequired(message="Review is required."),
            Length(max=20)
        ]
    )

    edit_ranking = IntegerField(
        'Edit Ranking',
        validators=[DataRequired(message="Ranking is required."), NumberRange(min=1, max=10)]
    )
    
    submit = SubmitField('Login')
