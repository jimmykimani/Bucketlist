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




