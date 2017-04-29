# api/resources/authentication.py
import json
from  flask import Blueprint, request, make_response, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Api, Resource

from api.models import User, UserSchema, db

auth_bp = Blueprint('auth_bp', __name__)
api = Api(auth_bp)

userschema = UserSchema()


class RegisterUser(Resource):
    # Register a user
    def post(self):
        request_data = request.get_json()
        if not request_data:
            response = {'user': 'No input data provided'}
            return response, 400
        errors = userschema.validate(request_data)
        if errors:
            return errors, 403
        try:
            username = request_data['username']
            user = User.query.filter_by(username=username).first()
            if not user:
                # create user
                user = User()
                user.username = request_data['username']
                user.password = request_data['password']
                user.email = request_data['email']
                user.add(user)
                # generate token
                auth_token = user.encode_auth_token(user.id)
                response_data = {
                    "status": "User {} created successfully.".format(user.username),
                    "token": auth_token.decode('ascii')
                }

                return response_data, 201
            else:
                response = {'Error': 'User {} already exists!'.format(user.username)}
                return response, 409
        except SQLAlchemyError as error:
            db.session.rollback()
            response = jsonify({'error': str(error)})
            return response, 401
            
  
class LoginUser(Resource):
    # Login a user
    def post(self):
        request_data = request.get_json()
        return request_data, 200

    
api.add_resource(RegisterUser, '/register', endpoint='auth_register')
api.add_resource(LoginUser, '/login', endpoint='auth')
