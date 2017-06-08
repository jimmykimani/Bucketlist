import os
import datetime
from app import db

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    """
    This class represents thr user model of the
    APi who canbe  created and allowed to login

    Once a login is sucesfull the user is generatd
    an auth token
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(250), nullable=False)
    bucketlist = db.relationship('Bucketlist', backref='user')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=36000):
        """
        To verify the auth_token, we use the same
        SECRET KEY used to encode a token
        """
        s = Serializer(os.getenv('SECRET') or 'super-secret', expires_in=expiration)
        # If the auth_token is valid, we get the
        # user id from the sub index of the payload.
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(os.getenv('SECRET'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token but already expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username


class Bucketlist(db.Model):
    """
    This class reprewsents Bucketlist tables
    """

    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_modified = db.Column(db.DateTime,
                              default=datetime.datetime.now,
                              onupdate=datetime.datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'),
                           nullable=False)
    items = db.relationship('Item', backref='bucketlist',
                            cascade='all, delete', lazy='dynamic')

    # def __repr__(self):
    #     return '<BucketList %s>' % (self.name)


class Item(db.Model):
    """
    This class represents Items inthe buckelets table
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        'bucketlist.id', ondelete='CASCADE'),nullable=False)
    item_id = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_modified = db.Column(db.DateTime,
                              default=datetime.datetime.now,
                              onupdate=datetime.datetime.now)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Item %s>' % (self.name)
