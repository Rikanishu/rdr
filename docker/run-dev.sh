#!/usr/bin/env bash

set -e

cd /app
alembic upgrade head
python ./run_app.py