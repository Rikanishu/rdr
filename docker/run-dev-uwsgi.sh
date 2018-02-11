#!/usr/bin/env bash

set -e

cd /app
alembic upgrade head
uwsgi --ini /app/tools/uwsgi/uwsgi-dev.example.ini