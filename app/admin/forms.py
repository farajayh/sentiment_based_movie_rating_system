from app import app
from . import admin

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class Login_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], default='Admin')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
            
class Change_Password_Form(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('conf_new_password')])
    conf_new_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change')
    