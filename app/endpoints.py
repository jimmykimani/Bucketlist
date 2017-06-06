from flask_restful import Api, Resource, fields, marshal, reqparse
from flask_httpauth import HTTPTokenAuth
from flask import request, g, Blueprint
from datetime import datetime


from app import db
from app.models import User, Bucketlist, Item
from app import errors

auth = HTTPTokenAuth(scheme='Token')
# Use HTTP authentication scheme to protect route '/' with a token
# The scheme name(Token) is given as an argument in the constructor.


@auth.verify_token
def verify_token(token):
    """
    The verify_token callback receives the
    authentication credentials provided by
    the client on the Authorization header
    """
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

# By default, all fields in out return iterable will be rendered as-is.
# Flask-RESTful provides the fields module and the marshal to help us solve this
# while working with objects


# Field Marshal for Bucketlist item
bucketlist_item_field = {'item_id': fields.Integer,
                         'name': fields.String,
                         'bucketlist_id': fields.Integer,
                         'date_created': fields.DateTime,
                         'date_modified': fields.DateTime,
                         'done': fields.String
                         }


# Field Marshal for Bucketlist
bucketlist_field = {'id': fields.Integer,
                    'name': fields.String,
                    'date_created': fields.DateTime,
                    'date_modified': fields.DateTime,
                    'created_by': fields.String,
                    'items': fields.Nested(bucketlist_item_field),
                    'uri': fields.Url('bucket_list.bucketlists'),
                    }

bucketlist_blueprint = Blueprint('bucket_list', __name__)
api_bucketlist = Api(bucketlist_blueprint)

# ======================================================
# CREATE Bucketlist Resource
# ------------------------------------------------------


class BucketlistAPI(Resource):
    """
    This class retrieves all the bucket lists
    that a user has created

    The class uses reqparse to validate data
    where it creates an instance of it

    """
    decorators = [auth.login_required]
    # This callback function will be called when authentication is succesful

    def __init__(self):
        """
        Define the bucketlist parameters

        """
        # Use reqparse for request data validation
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name', type=str,
            required=True,
            help='Please provide a bucketlist name',
            location='json'
        )

    def get(self, id=None):
        """
        The [GET] is used to return all bucktlists
        or a spcefic bucteklist if search parameters
        are provided

        Args:
            id :the bucketlist identifier
            q : returns specfic bucketlist based on the name
            limit:specify the number of results
        Returns:
            BucketList query
        """
        if id:
            bucket = Bucketlist.query.filter_by(
                id=id, created_by=g.user.id).first()
            if bucket:
                return marshal(bucket, bucketlist_field), 200
            return errors.not_found('Bucketlist not found')
        else:
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument(
                'page', type=int, location='args',
                default=1
            )
            self.reqparse.add_argument(
                'limit',
                type=int,
                default=20,
                location='args'
            )
            self.reqparse.add_argument(
                'q', type=str,
                location='args'
            )
            args = self.reqparse.parse_args()
            q = args['q']
            page = args['page']
            limit = args['limit']
        # if search or query parameters are given

        # Paginates the result of passed in functions and returns as JSON(Marshal)
        # courtesy - Miguel Grinberg (blog.miguelgrinberg.com)

        if q:
            bucketlist = Bucketlist.query.filter(Bucketlist.created_by == g.user.id,
                                                 Bucketlist.name.like('%' + q + '%'))\
                .paginate(page, limit, False)
        else:
            bucketlist = Bucketlist.query.filter_by(created_by=g.user.id).\
                paginate(page, limit, False)
        if not bucketlist:
            return errors.not_found('Bucketlist not available')

        if bucketlist.has_next:
            next_page = request.url + '?page=' + \
                str(page + 1) + '&limit=' + str(limit)
        else:
            next_page = 'Null'
        if bucketlist.has_prev:
            prev_page = request.url + '?page=' + \
                str(page - 1) + '&limit=' + str(limit)
        else:
            prev_page = 'Null'
        return {'meta': {'next_page': next_page,
                         'prev_page': prev_page,
                         'total_pages': bucketlist.pages
                         },
                'bucketlist': marshal(bucketlist.items,
                                      bucketlist_field
                                      )}, 200

    def post(self):
        """
        Creates a bucketlist and saves it to the database """
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

        return ({'message': 'New bucketlist created successfully',
                 'bucketlist': marshal(
                     new_bucketlist,
                     bucketlist_field
                 )}, 201)

    def put(self, id):
        """
        Edit the name of a bucketlist [PUT]

        Args:
            id :the bucketlist identiier
        Returns:
            a dictionary of the bucketlist updated
        """
        args = self.reqparse.parse_args()
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        name = args['name']

        if not bucketlist:
            return ({'message': 'bucketlist does not exist.'}, 404)
        else:
            if name == bucketlist.name:
                return ({'message': 'Cannot update with same name.'}, 409)
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
        """
        Delete a single bucketlist [DELETE]

        Args:
            id :the bucketlist identifier
        Returns:
            Response of the result status
        """
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

    # ======================================================
    # CREATE Bucketlist Item Resource
    # ------------------------------------------------------

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

    def get(self, bucketlist_id, item_id=None):
        """
        Returns a bucketlist item

        Args:
            bucketlist_id -- the bucketlist identifier
            item_id :the bucketlist item identifier
        Returns:
            BucketList item query
        """
        if item_id:
            user_id = g.user.id
            bucket_item = Item.query.filter_by(
                bucketlist_id=bucketlist_id, item_id=item_id).first()
            if not bucket_item:
                return errors.not_found("No items found")
            return marshal(bucket_item, bucketlist_item_field), 200
        elif bucketlist_id:
            bucket_item = Item.query.filter_by(
                bucketlist_id=bucketlist_id).all()
            if not bucket_item:
                return errors.not_found("No items found for this bucketlist")
            return marshal(bucket_item, bucketlist_item_field), 200
        else:
            item = Item.query.filter().all()
            if item:
                return marshal(item, bucketlist_item_field), 200
            return errors.not_found('No items created')

    def post(self, bucketlist_id):
        """
        Creates items to a specific bucketlist
        """

        args = self.reqparse.parse_args()
        name = args['name']
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, created_by=g.user.id).first()

        if not bucketlist:
            return errors.not_found('Sorry couldnt find bucketlist that matches id {}'
                                    .format(bucketlist_id))

        existent_item = (Item.query.filter_by(
            bucketlist_id=bucketlist_id, name=name)).first()
        if existent_item:
            return errors.Conflict('item already exists')
        last_existent_item = (Item.query.filter_by(bucketlist_id=bucketlist_id)
                              .order_by(db.desc(Item.item_id)))
        try:
            prev_item_id = last_existent_item[0].item_id
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
        if not args['name']:
            return errors.bad_request('Please provide an item name')

    def put(self, bucketlist_id, item_id):
        """
        Edit the name of a bucketlist itrem

        Args:
            id :the bucketlist item  identiier
        Returns:
            a dictionary of the bucketlist  item updated
        """
        args = self.reqparse.parse_args()
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, created_by=g.user.id).first()
        bucketlist_item = Item.query.filter_by(item_id=item_id).first()
        name = args['name']
        done = args['done']

        if not bucketlist:
            return errors.not_found('Invalid bucketlist id')
        if not bucketlist_item:
            return errors.not_found('Invalid item id')

        elif bucketlist_item:
            if done in [True, False]:
                bucketlist_item.done = done
            if name == bucketlist_item.name:
                return ({'message': 'Cannot update with same name.'}, 409)
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
        bucketlist_item = Item.query.filter_by(
            bucketlist_id=bucketlist_id, item_id=item_id).first()

        if not bucketlist:
            return errors.not_found('Invalid bucketlist id')
        if not bucketlist_item:
            return errors.not_found('Invalid bucketlist id')
        if bucketlist.created_by != g.user.id:
            return errors.forbidden('Your not authorized to perfome deletion')

        db.session.delete(bucketlist_item)
        db.session.commit()
        return ({'message': 'bucketlist with id {} has been deleted'.format(item_id)}, 200)

# =================================================
# DEFINE API RESOURCE FOR BUCKETLIST AND ITEMS


api_bucketlist.add_resource(
    BucketlistAPI, '/api/v1/bucketlists/<int:id>/', '/api/v1/bucketlists/', endpoint='bucketlists')
api_bucketlist.add_resource(
    BucketlistItemAPI,
    '/api/v1/bucketlists/<int:bucketlist_id>/items/',
    '/api/v1/bucketlists/<int:bucketlist_id>/items/<int:item_id>', endpoint='items'
)
# =================================================
# EOF
# --------------------------------------------------
