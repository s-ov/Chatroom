from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    StringField, TextAreaField, SubmitField, PasswordField,
    )
from wtforms.validators import (
    DataRequired, Length, ValidationError,
    )

from app.auth.models import User



class EmptyForm(FlaskForm):
    "Handle follow or unfollow action"
    submit = SubmitField('Виконати')


class EditProfileForm(FlaskForm):
    "Handle user profile updating form"

    username = StringField('Ім\'я: ', validators=[DataRequired()])
    bio = TextAreaField('Про мене', validators=[Length(min=0, max=140)])
    submit = SubmitField('Зберегти')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Виберіть інше імя.')
            

class ProfilePictureForm(FlaskForm):
    profile_picture = FileField('Upload Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Upload')


class DeleteAccountForm(FlaskForm):
    """Form to confirm account deletion."""
    password = PasswordField("Enter your password:", validators=[DataRequired()])
    submit = SubmitField("Delete Account")
