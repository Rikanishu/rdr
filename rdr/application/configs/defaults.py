# encoding: utf-8

import os

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))
APP_PATH = os.path.join(ROOT_PATH, "../../")


class ProductionConfig(object):
    """
    An example of standard development config.
    """

    """
    Secret key for Flask application.
    """
    SECRET_KEY = 'SecredKey'

    """
    Salt that will be mixed with user password to make better hash.
    """
    USERS_PWD_SALT = 'SecretSalt'

    """
    Is CSRF protection enabled in applcation.
    """
    CSRF_ENABLED = True

    """
    Flask application debug mode.
    """
    DEBUG = False

    """
    Default application timezone.
    """
    TIMEZONE = 'UTC'

    """
    Rewrite static "/media/*" routes for requests into static-bundle extension.
    """
    STATIC_REWRITE = False

    """
    Environment for static data handling.
    """
    STATIC_ENV = "prod"

    """
    Static bundle options.
    """
    STATIC_BUNDLE_INPUT_PATH = 'public/src'
    STATIC_BUNDLE_OUTPUT_PATH = 'public/build'
    STATIC_BUNDLE_ENV = 'production'
    STATIC_BUNDLE_REWRITE = False
    STATIC_BUNDLE_COPY_ONLY_BUNDLES = True

    """
    Disable standard media rewirte provided by Flask.
    """
    MEDIA_REWRITE = False

    """
    User agent for external HTTP queries.
    """
    DEFAULT_USER_AGENT = 'RSS-Feeds-Parser/0.1'

    """
    Root folder for project.
    """
    ROOT_PATH = ROOT_PATH

    """
    App folder in sources.
    """
    APP_PATH = APP_PATH

    """
    Host to listen.
    """
    HOST = '0.0.0.0'

    """
    Database configuration URI.
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://rdr:rdr@localhost/rdr"

    """
    Cache options.
    """
    CACHE_KEY_PREFIX = 'rdr.'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_URL = 'redis://localhost:6379'

    """
    Celery options.
    """
    CELERY_BROKER_URL = 'redis://localhost:6379/15',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/15'

    """
    Provider for fulltext searching.
    You can use Newspaper or Diffbot providers.
    """
    ARTICLES_FULLTEXT_PROVIDER = 'rdr.modules.feeds.full_text.newspaper.NewspaperProvider'

    """
    Elastic search options.
    """
    ELASTIC_SEARCH_ENABLED = False
    ELASTIC_SEARCH_URI = 'http://localhost:9200'

    """
    Uploads settings.
    8 Megabytes by default.
    """
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    """
    2 Megabytes by default
    """
    IMAGE_UPLOAD_MAX_SIZE = 2 * 1024 * 1024
    IMAGE_UPLOAD_ALLOWED_EXTENSIONS = ['jpg', 'gif', 'png']

    """
    Is new user registration enabled
    """
    SIGNUP_ENABLED = True

    """
    Supported languages
    """
    LANGUAGES = {
        'ru': 'Русский',
        'en': 'English'
    }


class DevelopmentConfig(ProductionConfig):
    """
    An example of standard development config.
    It bases on production config and overwrite some settings.
    """

    DEBUG = True
    STATIC_BUNDLE_REWRITE = True
    STATIC_BUNDLE_ENV = "development"
    MEDIA_REWRITE = True
    CSRF_ENABLED = False
    HOST = '127.0.0.1'
