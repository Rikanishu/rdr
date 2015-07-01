# encoding: utf-8

from rdr.components.blueprints import RichBlueprint
from rdr.modules.users.session import login_required, session_user
from rdr.application import app

blueprint = RichBlueprint('dropbox', __name__,
                          url_prefix="/dropbox")

@blueprint.route('/auth-start')
@login_required
def auth_start():
    pass

app.register_blueprint(blueprint)