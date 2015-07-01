#!/usr/bin/env python
# encoding: utf-8

if __name__ == '__main__':
    from rdr.application import app
    is_debug_enabled = app.config.get('DEBUG', False)
    app.run(host=app.config.get('HOST', None), debug=is_debug_enabled, use_reloader=is_debug_enabled)
