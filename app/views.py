from flask_restful import Api, Resource, fields, marshal, reqparse
from flask_httpauth import HTTPTokenAuth
from flask import Flask, request
from datetime import datetime
from flask import g, Blueprint

from app import db 
from app.models import User, Bucketlist, Item

auth = HTTPTokenAuth(scheme='Token')

@auth.verify_token
def verify_token(token):

    # authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

# By default, all fields in out return iterable will be rendered as-is.
# Flask-RESTful provides the fields module and the marshal to help us solve this
# while working with objects


# Field Marshal for Bucketlist
bucketlist_field = { 'id': fields.Integer,
                      'name': fields.String,
                      'date_created': fields.DateTime(dt_format='rfc822'),
                      'date_modified': fields.DateTime(dt_format='rfc822'),
                    #   'items': fields.Nested(bucketlist_item_field),
                      'created_by': fields.String,
                      'uri':fields.Url('bucket_list.bucketlist'),
                    }


bucketlist_blueprint = Blueprint('bucket_list', __name__)
api_bucketlist = Api(bucketlist_blueprint)

class BucketlistAPI(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name', type=str,
            required=True,
            help='Please provide a bucketlist name',
            location='json'
        )

    def post(self):
        args = self.reqparse.parse_args()
        bucketlist = Bucketlist.query.filter_by(name=args['name'], created_by=g.user.id).first()
        if not bucketlist:
            try:
                new_bucketlist = Bucketlist(
                    name=args['name'],
                    created_by=g.user.id
                )

                db.session.add(new_bucketlist)
                db.session.commit()

                return marshal(bucketlist, bucketlist_field), 200
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


            
        
        





api_bucketlist.add_resource(BucketlistAPI, '/bucketlist', endpoint='bucketlist')
