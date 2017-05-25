from flask import Flask, Blueprint, make_response, jsonify
from flask_restful import reqparse, Resource, Api, inputs
from app import db

from app.models import User


auth_blueprint = Blueprint('auth', __name__)

api_auth = Api(auth_blueprint)


class RegisterAPI(Resource):

    """
    User Registration Resource
    """

    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type=str,
            required=True,
            help='Invalid Username!',
            location='json'
        )
        self.reqparse.add_argument(
            'password', type=str,
            required=True,
            help='Please provid a password',
            location='json'
        )
        

    def post(self):
        """ lets one register to the API """

        args = self.reqparse.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if not user:
            try:
                user = User(
                    username=args['username'],
                    password_hash=args['password']
                )

                # insert the user
                user.hash_password(args['password'])
                db.session.add(user)
                db.session.commit()

                # generate the auth token
                # auth_token = user.generate_auth_token()
                response = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    # 'auth_token': auth_token.decode()
                }

                return (response, 201)
            except Exception as e:
                response = {
                    'status': 'fail' + str(e),
                    'message': 'Some error occurred. Please try again.'
                }
                return (response, 500)
        else:
            response = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return (response, 202)


class LoginAPI(Resource):
    """Login Resource"""

    def __init__(self):
        """
        constructor for  LoginAPI
        """

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type=str,
            required=True,
            help='Invalid Username!',
            location='json'
        )
        self.reqparse.add_argument(
            'password', type=str,
            required=True,
            help='Please provid a password',
            location='json'
        )

    def post(self):
        """"
         fxn to allow Login into the API
        """

        args = self.reqparse.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        try:
            if user:
                # verifies user and password
                if user.verify_password(args['password']):
                    auth_token = user.generate_auth_token()
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        # 'auth_token': auth_token.decode()
                    }
                    return response, 200
                else:
                    response = {
                        'status': 'fail',
                        'message': 'Invalid user or Password mismatch.'
                    }
                    return response, 404
        except:

            response = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response, 500

api_auth.add_resource(RegisterAPI, '/auth/register', endpoint='register')
api_auth.add_resource(LoginAPI, '/auth/login', endpoint='login')
