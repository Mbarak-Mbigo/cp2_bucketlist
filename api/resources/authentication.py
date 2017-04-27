# api/resources/authentication.py
from flask import Blueprint

from flask_restful import Api, Resource

auth_bp = Blueprint('auth_bp', __name__)
api = Api(auth_bp)


class Authentication(Resource):
    def get(self):
        pass
    
    def post(self):
        pass
    
    def put(self):
        pass
    
    
api.add_resource(Authentication, '/login', endpoint='auth')
api.add_resource(Authentication, '/register', endpoint='auth_register')
api.add_resource(Authentication, '/token', endpoint='auth_token')
