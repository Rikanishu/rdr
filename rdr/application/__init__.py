# encoding: utf-8

from __future__ import absolute_import
from flask import Flask
from rdr.application.configs import Config

app = Flask(__name__, static_folder=None)
app.config.from_object(Config)

from . import static
import rdr.components.csrf
import rdr.components.timezone
import rdr.components.media.rewrite

# For SQLAlchemy details logging

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# For Flask logging

# import logging
# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# app.logger.addHandler(ch)

# Application modules

import rdr.modules.files
import rdr.modules.home
import rdr.modules.users
import rdr.modules.feeds
import rdr.modules.subscribes