from flask_restful import Api, Resource, fields, marshal, reqparse
from flask_httpauth import HTTPTokenAuth
from flask import Flask, request, g, jsonify
from datetime import datetime
from flask import g, Blueprint


from app import db
from app.models import User, Bucketlist, Item
from app import errors

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    """To validate the token sent by the user."""
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

# By default, all fields in out return iterable will be rendered as-is.
# Flask-RESTful provides the fields module and the marshal to help us solve this
# while working with objects


bucketlist_item_field = {'item_id': fields.Integer,
                         'item_name': fields.String,
                         'date_created': fields.DateTime,
                         'date_modified': fields.DateTime(dt_format='rfc822'),
                         'done': fields.String
                         }


# Field Marshal for Bucketlist
bucketlist_field = {'id': fields.Integer,
                    'name': fields.String,
                    'date_created': fields.DateTime,
                    'date_modified': fields.DateTime,
                    # 'items': fields.Nested(bucketlist_item_field),
                    'created_by': fields.String,
                    'uri': fields.Url('bucket_list.bucketlists'),
                    }

bucketlist_blueprint = Blueprint('bucket_list', __name__)
api_bucketlist = Api(bucketlist_blueprint)


class BucketlistAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        """
        Define the bucketlist parameters

        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name', type=str,
            required=True,
            help='Please provide a bucketlist name',
            location='json'
        )

    def get(self, id=None):
        if id:
            if g.user.id:
                bucket = Bucketlist.query.filter_by(
                    id=id, created_by=g.user.id).first()
                print ('passs............')
                if bucket:
                    return marshal(bucket, bucketlist_field), 200

    def post(self):
        args = self.reqparse.parse_args()
        new_bucketlist = Bucketlist(name=args['name'], created_by=g.user.id)

        if Bucketlist.query.filter_by(name=args['name'], created_by=g.user.id).first():
            return errors.Conflict('Bucket list {} already exists'.format(args['name']))
        if new_bucketlist:

            db.session.add(new_bucketlist)
            db.session.commit()

            return marshal(new_bucketlist, bucketlist_field), 201

    def put(self, id):
        args = self.reqparse.parse_args()
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        name = args['name']

        if not bucketlist:
            return ({'message': 'bucketlist with id {} has been updated'.format(id)}, 200)
        if name:
            if bucketlist.created_by == g.user.id:

                bucketlist.name = name
                db.session.add(bucketlist)
                db.session.commit()
                return (
                    {
                        'message': 'Update was successfull',
                        'bucketlist': marshal(
                            bucketlist,
                            bucketlist_field
                        )
                    }, 200
                )

            else:
                return errors.bad_request(' Unauthorised')
        else:
            return errors.bad_request('No value provided!')

    def delete(self, id):
    
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()

        if bucketlist:
            if bucketlist.created_by == g.user.id:
                db.session.delete(bucketlist)
                db.session.commit()
                return ({'message': 'bucketlist with id {} has been deleted'.format(id)}, 200)
            else:
                return errors.bad_request(' Unauthorised')
        else:
            return errors.not_found('Bucketlist does not exist!')

class BucketlistItemAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name', type=str,
            required=True,
            help='Please provide an item name',
            location='json'
        )
        self.reqparse.add_argument(
            'done', default=False,
            type=bool,
            location='json'
        )

    def get(self, bucketlist_id):
        pass
# define the API resource
api_bucketlist.add_resource(
    BucketlistAPI, '/api/v1/bucketlists/<int:id>/', '/api/v1/bucketlists/', endpoint='bucketlists')
