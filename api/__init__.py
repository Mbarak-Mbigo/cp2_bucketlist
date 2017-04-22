from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    """Application factory function for app instance creation."""
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    
    # from api.resources import api
    # api.init_app(app)

    from api.resources import api_v1
    # app.register_blueprint(api_v1, url_prefix='/')
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    return app

