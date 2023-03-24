import logging
import os
import sys

from flask import Flask
from flask.logging import default_handler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logtail import LogtailHandler

from src.logging_helpers import (log_after_request,
                                 save_logging_context_before_request)

logtail_handler = LogtailHandler(
    source_token=os.getenv("LOGTAIL_TOKEN"), level=logging.DEBUG
)

db = SQLAlchemy()
migrate = Migrate()
# dictConfig(
#     {
#         "version": 1,
#         "formatters": {
#             "default": {
#                 "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
#             }
#         },
#         "handlers": {
#             "console": {
#                 "class": "logging.StreamHandler",
#                 "stream": "ext://sys.stdout",
#                 "formatter": "default",
#             },
#             "logtail": {
#                 "class": "logtail.LogtailHandler",
#                 "source_token": os.getenv("LOGTAIL_TOKEN"),
#                 "formatter": "default",
#             },
#         },
#         "root": {"level": "DEBUG", "handlers": ["console", "logtail"]},
#     }
# )


def create_app():
    """
    It creates a Flask app, sets up the session, and registers the blueprints
    :return: A Flask app object
    """
    app: Flask = Flask(__name__)

   
    app.secret_key = b"\x18\xc4\xd0&\xfd\xf3\xd2\xa1\x11\x88p\xb8\xe6\x0f'\xbf"

    DB_URL = f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PW")}@{os.getenv("POSTGRES_URL")}/{os.getenv("POSTGRES_DB")}'
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    initialize_logging(app)
    initialize_extensions(app)
    register_blueprints(app)
    register_decorators(app)

    return app


def register_decorators(app):
    app.before_request(save_logging_context_before_request)
    app.after_request(log_after_request)


def initialize_extensions(app):
    """
    It initializes the extensions
    :param app: A Flask app object
    :return: None
    """
    db.init_app(app)
    migrate.init_app(app, db)


def initialize_logging(app: Flask):
    """
    It initializes the logging
    :param app: A Flask app object
    :return: None
    """

    app.logger.level = logging.DEBUG
    app.logger.removeHandler(default_handler)
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

