# encoding: utf-8

from flask import request
from werkzeug.exceptions import BadRequest

from rdr.components.blueprints import RichBlueprint
from rdr.components.helpers import json
from rdr.modules.files.images import ImageStorage
from rdr.modules.users.models import Profile
from rdr.modules.users.session import login_required
from rdr.modules.users.session import user_session

from rdr.application.database import db
from rdr.application import app

blueprint = RichBlueprint('files', __name__, template_folder='templates')

@blueprint.route('/images/upload/user', methods=['POST'])
@json.wrap
@login_required
def user_image_upload():
    identity = user_session.identity
    if 'file' not in request.files:
        raise BadRequest('Invalid request')
    f = request.files['file']

    # if not (0 < f.content_length < app.config['IMAGE_UPLOAD_MAX_SIZE']):
    #    raise BadRequest('Invalid file size')

    storage = ImageStorage(f.stream, 'user-image')
    if not storage.in_format(app.config['IMAGE_UPLOAD_ALLOWED_EXTENSIONS']):
        raise BadRequest('Invalid image format')

    original_model = storage.save()
    big_thumb = storage.copy().fit(132, 132).save_thumbnail('middle')
    small_thumb = storage.copy().fit(32, 32).save_thumbnail('small')

    db.session.add(original_model)
    db.session.commit()

    profile = Profile.query.filter(Profile.user_id == identity.id).one()
    profile.image_id = original_model.id
    db.session.commit()

    return {
        'orig': original_model.src(),
        'middle': big_thumb.src(),
        'small': small_thumb.src()
    }

app.register_blueprint(blueprint)
