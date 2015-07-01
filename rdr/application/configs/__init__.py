# encoding: utf-8

# production environment used by default
# if you want change environment or customize some settings just copy and rename example.py to app.py

try:
    from app import ApplicationConfig as Config
except ImportError:
    from defaults import ProductionConfig as Config