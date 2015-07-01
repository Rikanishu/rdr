# encoding: utf-8

from rdr.components.forms import Form
from wtforms import StringField, PasswordField, validators
from rdr.modules.users.validators import UniqueUser, Required, Email, EqualTo


class RegistrationForm(Form):

    email = StringField('Email', [
        Required(),
        Email(),
        UniqueUser()
    ])
    username = StringField('Username', [Required()])
    password = PasswordField('Password', [Required()])


class ProfileSettingsForm(Form):

    username = StringField('User Name', [validators.DataRequired()])


class ChangePasswordForm(Form):

    old_password = StringField('Old Password', [Required()])
    new_password = StringField('New Password', [Required()])
    confirm_new_password = StringField('Confirm New Password', [
        Required(),
        EqualTo('new_password')
    ])