# encoding: utf-8

from __future__ import with_statement, absolute_import
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(root_path)

from rdr.application import app
from rdr.application.database import db

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = app.config.get("SQLALCHEMY_DATABASE_URI")
    context.configure(url=url, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine_conf = config.get_section(config.config_ini_section)
    engine_conf["sqlalchemy.url"] = app.config.get("SQLALCHEMY_DATABASE_URI")
    engine = engine_from_config(
        engine_conf,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    connection = engine.connect()

    from blinker import Namespace
    signals = Namespace().signal

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        signals=signals
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
        signals('on_complete').send(context)
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

