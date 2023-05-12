import logging
import os
import sys

from posthog import Posthog
from flask import Flask
from flask.logging import default_handler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logtail import LogtailHandler

from src.logging_helpers import (log_after_request,
                                 save_logging_context_before_request)

logtail_handler = None
if os.getenv("LOGTAIL_TOKEN") is not None:
    logtail_handler = LogtailHandler(
        source_token=os.getenv("LOGTAIL_TOKEN"), level=logging.DEBUG
    )

db = SQLAlchemy()
migrate = Migrate()
posthog = Posthog(
    project_api_key=os.getenv("POSTHOG_API_KEY", None),
    host=os.getenv("POSTHOG_HOST", None),
)

def create_app():
    """
    It creates a Flask app, sets up the session, and registers the blueprints
    :return: A Flask app object
    """
    app: Flask = Flask(__name__)

   
    app.secret_key = b"\x18\xc4\xd0&\xfd\xf3\xd2\xa1\x11\x88p\xb8\xe6\x0f'\xbf"
    app.posthog = posthog

    initialize_logging(app)
    register_blueprints(app)
    register_decorators(app)

    return app


def register_decorators(app):
    app.before_request(save_logging_context_before_request)
    app.after_request(log_after_request)


def initialize_logging(app: Flask):
    """
    It initializes the logging
    :param app: A Flask app object
    :return: None
    """

    app.logger.level = logging.DEBUG
    app.logger.removeHandler(default_handler)
    if logtail_handler is not None:
        app.logger.addHandler(logtail_handler)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))

    app.logger.log(logging.INFO, "Logging initialized")

def register_blueprints(app):
    """
    It registers the blueprints
    :param app: A Flask app object
    :return: None
    """
    from src.api import bp as api_bp 

    app.register_blueprint(api_bp, url_prefix="/api")

