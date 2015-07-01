### Some useful commands ###

==========================================================
Collect static to build (on production environment):
```python manage.py collect-static```

==========================================================
Compile LESS file to CSS:
```lessc "./less/bootstrap.less" > bootstrap.css```

And with compressing:
```lessc --compress "./less/bootstrap.less" > bootstrap.css```

===========================================================
Generate alembic auto migration:
```alembic revision --autogenerate --message "migration_name"```

Check the next upgrade SQL:
```alembic upgrade head --sql```

And to apply migration:
```alembic upgrade head```

To revert previous migration:
```alembic downgrade -1```

===========================================================
PIP install from requirements:
```pip install -r /path/to/requirements.txt```

PIP update all packages in venv:
```pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U```

PIP update alternative:
```pip install --upgrade --force-reinstall -r requirements.txt
pip install --ignore-installed -r requirements.txt```

===========================================================
Babel compile message
``pybabel compile -d rdr/application/translations/```

===========================================================
Celery run
```celery worker -A rdr.tasks.celery -l info -P prefork -c 16```

Celerybeat run
```celery beat -A rdr.tasks.celery```
