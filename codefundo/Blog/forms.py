from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    Username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class VoterForm(FlaskForm):
    Voter_ID = StringField('Voter_ID', validators=[DataRequired()])
    Voter_ID_Confirm = StringField('Voter_ID_Confirm', validators=[DataRequired()])
    submit = SubmitField('Login')