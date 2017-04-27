"""Application configuration module.

configuration definitions and options
config.py
"""
# standard imports
import os

# third party imports
# local imports

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Common configurations across all environments."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'id9v<3%$i01p9BE@'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    PAGINATION_PAGE_SIZE = 20
    PAGINATION_PAGE_ARGUMENT_NAME = 'page'


class DevelopmentConfig(Config):
    """Development environment configurations."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="db_admin",
                                                                                             DB_PASS="",
                                                                                             DB_ADDR="127.0.0.1",
                                                                                             DB_NAME="bucketlist_dev")


class TestingConfig(Config):
    """Testing environment configurations."""

    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="db_admin",
                                                                                             DB_PASS="",
                                                                                             DB_ADDR="127.0.0.1",
                                                                                             DB_NAME="bucketlist_test")


class ProductionConfig(Config):
    """Production environment configurations."""

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="db_user01",
                                                                                             DB_PASS="64fks6wH&",
                                                                                             DB_ADDR="0.0.0.0",
                                                                                             DB_NAME="bucketlist_data")


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
