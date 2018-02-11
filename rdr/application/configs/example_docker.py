# encoding: utf-8

from defaults import DevelopmentConfig


class ApplicationConfig(DevelopmentConfig):
    CACHE_REDIS_HOST = 'redis'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_URL = 'redis://redis:6379'
    SQLALCHEMY_DATABASE_URI = "postgresql://root:root@postgres/rdr"
    CELERY_BROKER_URL = 'redis://redis:6379/15',
    CELERY_RESULT_BACKEND = 'redis://redis:6379/15'
    HOST = '0.0.0.0'