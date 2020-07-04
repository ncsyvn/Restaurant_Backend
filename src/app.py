from flask import Flask
from src.extensions import db, ma
from src.settings import DevConfig
from src.api.v1 import product, bill, bill_detail, statistic


def create_app(config_object=DevConfig):
    """Init App Register Application extensions and API prefix

    Args:
        config_object: We will use Prod Config when the environment variable has FLASK_DEBUG=1.
        You can run export FLASK_DEBUG=1 in order to run in application dev mode.
        You can see config_object in the settings.py file
    """
    app = Flask(__name__, static_url_path="", static_folder="./files", template_folder="./template")
    app.config.from_object(config_object)
    register_extensions(app, config_object)
    register_blueprints(app)
    return app


def register_extensions(app, config_object):
    """Init extension. You can see list extension in the extensions.py

    Args:
        app: Flask handler application
        config_object: settings of the application
    """
    # Order matters: Initialize SQLAlchemy before Marshmallow
    # create log folder
    db.app = app
    db.init_app(app)
    ma.init_app(app)


def register_blueprints(app):
    """Init blueprint for api url

    :param app: Flask application
    """
    app.register_blueprint(product.api, url_prefix='/api/v1/products')
    app.register_blueprint(bill.api, url_prefix='/api/v1/bills')
    app.register_blueprint(bill_detail.api, url_prefix='/api/v1/bill_detail')
    app.register_blueprint(statistic.api, url_prefix='/api/v1/statistic')
