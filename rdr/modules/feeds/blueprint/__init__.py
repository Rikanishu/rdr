# encoding: utf-8

from rdr.components.blueprints import RichBlueprint
from rdr.application import app

blueprint = RichBlueprint('feeds', __name__,
                          url_prefix="/feeds", template_folder='templates')

from . import feeds, articles, packages, offline_reading

app.register_blueprint(blueprint)