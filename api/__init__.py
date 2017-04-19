from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    """Application factory function for app instance creation."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)

    return app

