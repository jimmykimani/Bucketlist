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
                         'name': fields.String,
                         'bucketlist_id': fields.Integer,
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
            bucket = Bucketlist.query.filter_by(
                id=id, created_by=g.user.id).first()
            if bucket:
                return marshal(bucket, bucketlist_field), 200
        else:
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument(
                'page', type=int,location='args',
                deafult=1
            )
            self.reqparse.add_argument(
                'limit',
                type=int,
                default=20,
                location='args'
            )
            self.reqparse.add_argument(
                'q',type=str,
                location='args'
            )

    def post(self):
        args = self.reqparse.parse_args()
        new_bucketlist = Bucketlist(name=args['name'],
                                    created_by=g.user.id)

        if Bucketlist.query.filter_by(name=args['name'],
                                      created_by=g.user.id).first():
            return errors.Conflict('Bucket list {} already exists'
                                   .format(args['name']))
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
            return ({'message': 'bucketlist with id {} has been updated'
                     .format(id)}, 200)
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
                return ({'message': 'bucketlist with id {} has been deleted'
                         .format(id)}, 200)
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

    def post(self, bucketlist_id):
        """
        Creates items to a specific bucketlist
        """

        args = self.reqparse.parse_args()
        name = args['name']
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, created_by=g.user.id).first()

        if not bucketlist:
            return errors.not_found('Sorry couldnt find bucketlist that matches id {}'.format(bucketlist_id))

        existent_item = (Item.query.filter_by(
            bucketlist_id=bucketlist_id, name=name)).first()
        if existent_item:
            return errors.Conflict('item already exists')
        last_existent_item = (Item.query.filter_by(bucketlist_id=bucketlist_id)
                              .order_by(db.desc(Item.id)))
        try:
            prev_item_id = last_existent_item[0].id
        except IndexError:
            prev_item_id = 0

        if bucketlist.created_by == g.user.id:
            new_item = Item(name=name,
                            item_id=prev_item_id + 1,
                            bucketlist_id=bucketlist_id)
            db.session.add(new_item)
            db.session.commit()
            return (
                {
                    'message': 'New bucketlist item created successfully',
                    'bucketlist': marshal(
                        new_item,
                        bucketlist_item_field)
                }, 201
            )
        else:
            return errors.unauthorized('Your not authorised to access this item!')
        if Item.query.filter_by(name=args['item_name']).first():
            return errors.Conflict('Item already exists')
        if not args['item_name']:
            return errors.bad_request('Please provide an item name')

    def put(self, bucketlist_id, item_id):
        """
        Updates a specific bucketlist item
        """
        args = self.reqparse.parse_args()
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, created_by=g.user.id).first()
        bucketlist_item = Item.query.filter_by(item_id=item_id).first()
        name = args['item_name']
        done = args['done']

        if not bucketlist:
            return errors.not_found('Invalid bucketlist id')
        if not bucketlist_item:
            return errors.not_found('Invalid item id')

        elif bucketlist_item:
            if done in ['True', 'False']:
                bucketlist_item.done = done
            if name:
                bucketlist_item.name = name

            db.session.commit()
            return marshal(bucketlist_item, bucketlist_item_field), 200

    def delete(self, bucketlist_id, item_id):
        """
        Delete an item in a Bucketlist
        """
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, created_by=g.user.id).first()
        bucketlist_item = Item.query.filter_by(item_id=item_id).first()

        if not bucketlist or bucketlist_item:
            return errors.not_found('Invalid bucketlist id')
        if bucketlist.created_by != g.user.id:
            return errors.forbidden('Your not authorized to perfome deletion')

        db.session.delete(bucketlist_item)
        db.session.commit()
        return ({'message': 'bucketlist with id {} has been deleted'.format(item_id)}, 200)


# define the API resource
api_bucketlist.add_resource(
    BucketlistAPI, '/api/v1/bucketlists/<int:id>/', '/api/v1/bucketlists/', endpoint='bucketlists')
api_bucketlist.add_resource(
    BucketlistItemAPI,
    '/api/v1/bucketlists/<int:bucketlist_id>/items/',
    '/api/v1/bucketlists/<int:bucketlist_id>/items/<int:item_id>', endpoint='items'
)
