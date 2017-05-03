# common/authentication.py
import json

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask import g, request, jsonify
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from api.models import User, UserSchema, db

userschema = UserSchema()

auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@auth.verify_password
def verify_user_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@token_auth.verify_token
def verify_token(token):
    user = User.decode_auth_token(token)
    if type(user) is int:
        g.user = User.query.filter_by(id=user).first()
        return True
    response = {
        'Error': user
    }
    print(response)
    return False
        

class AuthRequiredResource(Resource):
    method_decorators = [token_auth.login_required]


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
                    "status": "User {} registered Successfully.".format(user.username),
                    "token": auth_token.decode()
                }
                return response_data, 201
            else:
                response = {
                    'Error': 'User {} already exists!'.format(user.username)
                }
                return response, 409
        except SQLAlchemyError as error:
            db.session.rollback()
            response = jsonify({'error': str(error)})
            return response, 401


class LoginUser(Resource):
    # Login a user
    def post(self):
        request_data = request.get_json()
        if not request_data:
            response = {'user': 'No input data provided'}
            return response, 400
        
        if 'username' and 'password' not in request_data.keys():
            response = {'Error': 'password and username required'}
            return response, 400
        else:
            if verify_user_password(request_data['username'], request_data['password']):
                user = User.query.filter_by(username=request_data['username']).first()
                auth_token = user.encode_auth_token(user.id)
                response = {
                    'status': 'Login successful.',
                    'token': auth_token.decode()
                }
                return response, 200
            else:
                response = {
                    'Error': 'Invalid username or password'
                }
                return response, 401
