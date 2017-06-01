from flask_restful import Api, Resource, fields, marshal, reqparse
from flask_httpauth import HTTPTokenAuth
from flask import Flask, request, g
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
                    'items': fields.Nested(bucketlist_item_field),
                    'created_by': fields.String,
                    'uri': fields.Url('bucket_list.bucketlist'),
                    }

bucketlist_blueprint = Blueprint('bucket_list', __name__)
api_bucketlist = Api(bucketlist_blueprint)