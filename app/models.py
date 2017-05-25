import os
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


class User(db.Model):
    """
    This class represents User table
    """

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True)
    password = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expiration=36000):

        s = Serializer(os.getenv('SECRET_KEY'), expires_in=expiration)
        return s.dumps({'user_id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(os.getenv('SECRET'))
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['user_id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username


class Bucketlist(db.Model):
    """
    This class reprewsents Bucketlist tables
    """

    __tablename__ = 'bucketlists'
    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                           nullable=False)
    items = db.relationship('Item', backref='Bucketlist',
                            cascade='all, delete', lazy='dynamic')

    def __repr__(self):
        return '<BucketList %s>' % (self.name)


class Item(db.Model):
    """
    This class represents Items inthe buckelets table
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        return '<Item %s>' % (self.name)
