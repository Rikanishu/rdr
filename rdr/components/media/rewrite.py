# encoding: utf-8

from rdr.application import app
import os
from flask import send_from_directory

if app.config.get('MEDIA_REWRITE', False):
    @app.route('/media/' + '<path:filename>')
    def rewrite_media(filename):
        cache_timeout = app.get_send_file_max_age(filename)
        return send_from_directory(
            os.path.abspath(
                os.path.join(app.config.get('ROOT_PATH'), 'public', 'media')
            ), filename, cache_timeout=cache_timeout
        )