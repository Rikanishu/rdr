# encoding: utf-8

from wtforms import validators, ValidationError
from rdr.modules.users.models import User
from sqlalchemy import func


class UniqueUser(object):

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        existed_user = User.query.filter(func.lower(User.email) == func.lower(field.data)).first()
        if existed_user:
            message = self.message
            if message is None:
                message = field.gettext('This email is already taken.')
            raise ValidationError({
                'reason': 'unique',
                'text': message
            })


class ClientValidatorAdapter(object):

    reason = 'other'
    validator = None

    def __init__(self, *args, **kwargs):
        if self.validator is None:
            raise Exception('Unknown validator class')
        self.validator_object = self.validator(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        try:
            self.validator_object.__call__(*args, **kwargs)
        except ValidationError as e:
            raise ValidationError({
                'reason': self.reason,
                'text': e.message
            })


class Required(ClientValidatorAdapter):

    reason = 'required'
    validator = validators.DataRequired


class Email(ClientValidatorAdapter):

    reason = 'email'
    validator = validators.Email


class EqualTo(ClientValidatorAdapter):

    reason = 'equal'
    validator = validators.EqualTo
