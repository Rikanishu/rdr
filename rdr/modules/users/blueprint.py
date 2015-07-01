# encoding: utf-8

from datetime import datetime, timedelta
from rdr.application import app
from rdr.application.database import db
from rdr.components.blueprints import RichBlueprint
from rdr.components.helpers import json
from rdr.modules.users.session import user_session, login_required
from rdr.modules.users.forms import RegistrationForm, ProfileSettingsForm, ChangePasswordForm
from rdr.modules.users.models import User, Profile
from werkzeug.datastructures import MultiDict

blueprint = RichBlueprint('users', __name__,
                          url_prefix="/users", template_folder='templates')



@blueprint.route('/auth', methods=['POST'])
@json.wrap
def auth():
    body = json.get_request_body()
    login = body['login']
    password = body['password']
    user = User.query.filter(db.func.lower(User.email) == db.func.lower(login)).first()
    if user and user.check_password(password):
        user_session.identity = user
        return {
            'success': True,
            'user': user.to_dict()
        }
    return {
        'success': False,
        'user': None
    }


@blueprint.route('/quit', methods=['POST'])
@json.wrap
@login_required
def _quit():
    user_session.quit()
    return {
        'success': True
    }


@blueprint.route('/signup', methods=['POST'])
@json.wrap
def signup():

    if not app.config['SIGNUP_ENABLED']:
        return {
            'success': False,
            'message': 'Signup is not enabled'
        }

    form = RegistrationForm(MultiDict(json.get_request_body()))
    if not form.validate():
        return {
            'success': False,
            'errors': form.errors_dict
        }

    data = form.data
    user = User(
        email=data['email'],
        password=data['password'],
        username=data['username']
    )
    db.session.add(user)
    db.session.commit()

    profile = Profile(user_id=user.id)
    db.session.add(profile)
    db.session.commit()

    user_session.identity = user

    return {
        'success': True,
        'user': user.to_dict()
    }


@blueprint.route('/settings/change-profile-settings', methods=['POST'])
@json.wrap
@login_required
def change_profile_settings():
    identity = user_session.identity
    data = json.get_request_body()
    form = ProfileSettingsForm(MultiDict({
        'username': data['username']
    }))
    if not form.validate():
        return {
            'success': False,
            'errors': form.errors_dict
        }

    user = User.query.filter(User.id == identity.id).one()
    user.username = form.data['username']
    db.session.commit()

    return {
        'success': True
    }


@blueprint.route('/settings/change-password', methods=['POST'])
@json.wrap
@login_required
def change_password():
    identity = user_session.identity
    data = json.get_request_body()
    form = ChangePasswordForm(MultiDict({
        'old_password': data['oldPassword'],
        'new_password': data['newPassword'],
        'confirm_new_password': data['confirmNewPassword']
    }))
    if not form.validate():
        return {
            'success': False,
            'errors': form.errors_dict
        }

    user = User.query.filter(User.id == identity.id).one()
    form_data = form.data
    if not user.check_password(form_data['old_password']):
        raise json.InvalidRequest('Invalid password')
    user.password = form.data['new_password']
    db.session.commit()

    return {
        'success': True
    }


@blueprint.route('/settings/lang-change', methods=['POST'])
@json.wrap
@login_required
def lang_change():
    data = json.get_request_body()
    if user_session.is_auth:
        prof = Profile.query.filter(Profile.user_id == user_session.identity.id).one()
        prof.lang = data['language']
        db.session.commit()
    return {
        'success': True
    }


@blueprint.route('/activity-checking', methods=['POST'])
@json.wrap
@login_required
def activity_checking():
    success = False
    if user_session.is_auth:
        identity = User.query.filter(User.id == user_session.identity.id).one()
        if not identity.last_visit or (datetime.now() - identity.last_visit) >= timedelta(minutes=5):
            identity.last_visit = datetime.now()
            db.session.commit()
            success = True
    return {
        'success': success
    }

app.register_blueprint(blueprint)