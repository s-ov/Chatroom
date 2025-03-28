from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField,
    SubmitField,
    BooleanField,
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
)
from flask_babel import lazy_gettext as _l

from app.auth.models import User


class RegistrationForm(FlaskForm):
    "Handle registration form for user"

    username = StringField(_l('Ім\'я:'), validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторіть пароль:', 
        validators=[
            DataRequired(), 
            EqualTo('password')],
        )
    submit = SubmitField('Реєстрація')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Користувач з таким іменем вже зареєстрований.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('No such email. First, register.')
        

class LoginForm(FlaskForm):
    "Handle login form for user"
    username = StringField('Ім\'я:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ResetPasswordRequestForm(FlaskForm):
    "Handle form for password request sending."
    email = StringField(
        "Email", 
        validators=[DataRequired(), Email()],
        )
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    "Handle form for password request sending."
    password = PasswordField(
        "New Password", 
        validators=[DataRequired()],
        )
    password2 = PasswordField(
        "Repeat Password", 
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Confirm Password Reset")
