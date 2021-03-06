# api/resources/authentication.py

from flask import Blueprint
from flask_restful import Api

from api import add_cors_headers
from common.authentication import RegisterUser, LoginUser

auth_bp = Blueprint('auth_bp', __name__)
auth_bp.after_request(add_cors_headers)
api = Api(auth_bp)

api.add_resource(RegisterUser, '/register', endpoint='auth_register')
api.add_resource(LoginUser, '/login', endpoint='auth')
