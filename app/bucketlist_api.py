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