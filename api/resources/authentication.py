
from flask import Blueprint

from flask_restful import Api, Resource


auth = Blueprint('auth', __name__)
api = Api(auth)


class Authentication(Resource):
    def get(self):
        pass
    
    def post(self):
        pass
    
    def put(self):
        pass
    
    
api.add_resource(Authentication, '/login', endpoint='auth')
api.add_resource(Authentication, '/register', endpoint='auth_register')
