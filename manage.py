#!/usr/bin/env python
# encoding: utf-8

from flask.ext.script import Manager
from rdr.application import app

import rdr.commands

manager = Manager(app)
manager.add_command("collect-static", rdr.commands.CollectStaticCommand())
manager.add_command("fill-mockup", rdr.commands.MockupCommand())

if __name__ == '__main__':
    manager.run()
