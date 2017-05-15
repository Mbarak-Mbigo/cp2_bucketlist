# api/__init__.py
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()

def add_cors_headers(response, ):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    # print("Response: ", )
    return response

def create_app(config_name):
    """Application factory function for app instance creation."""
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    
    # from api.resources import api
    # api.init_app(app)
    from api.resources.api_auth_v1 import auth_bp
    from api.resources import api_v1
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    return app
