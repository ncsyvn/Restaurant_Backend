import os
os_env = os.environ


class Config(object):
    SECRET_KEY = '3nF3Rn0'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

class DevConfig(Config):
    """Development configuration."""
    # a config
    ENV = 'development'
    DEBUG = True
    DEBUG_TB_ENABLED = True  # Disable Debug toolbar
    HOST = '0.0.0.0'
    TEMPLATES_AUTO_RELOAD = True
    # msql
    SQLALCHEMY_DATABASE_URI = 'mysql://ncsyvn:123456@127.0.0.1:3306/restaurant'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
