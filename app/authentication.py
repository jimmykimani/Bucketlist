from flask import Flask, Blueprint, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api
from app import db

from app.models import User


auth_blueprint = Blueprint('auth', __name__)

api_auth = Api(auth_blueprint)


class RegisterAPI(Resource):

    """
    User Registration Resource
    """

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'username', type=str,
            help="No username provided!",
            required=True
        )
        self.parser.add_argument(
            'password', type=str,
            help='Invalid password'
        )

    def post(self):
        args = self.parser.parse_args()
        if username is None or password is None:
            abort(400)
        user = User.query.filter_by(username=args['username']).first()
        if user is None:
            try:
                user = Users(
                    username=args['username'],
                    password=args['password'],
                )
                user.hash_password(args['password'])
                db.session.add(user)
                db.session.commit()

                auth_token = user.generate_auth_token()
                r = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(r)), 201
            except Exception as e:
                r = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(r)), 401
        else:
            r = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(r)), 202


class LoginAPI(Resource):
    """
    User Login Resource
    """

    def post(self):
        # fetch the post data
        args = self.parser.parse_args()
        try:
            # fetch the user data
            user = User.query.filter_by(username=args['username']).first()
            if user and user.verify_password(args['password']):
                auth_token = user.generate_auth_token(user.id)
                if auth_token:
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response)), 404
        except Exception as e:
            print(e)
            response = {
                'status': 'fail',
                'message': 'Try again'
            }

            return make_response(jsonify(response)), 500


api_auth.add_resource(RegisterAPI, '/auth/register', endpoint='register')
api_auth.add_resource(LoginAPI, '/auth/login', endpoint='login')
