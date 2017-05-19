from app import db
from datetime import datetime

class User(db.Model):
    """
    This class represents User table
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True)
    password = db.Column(db.String(100))


    def __repr__(self):
        return '<User %r>' % self.username

class Bucketlist(db.Model):
    """
    This class reprewsents Bucketlist tables
    """

    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    # owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref='Bucketlist',
                            cascade='all, delete', lazy='dynamic')

    def __init__(self, name):
        """initialize with name."""
    # self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
        return '<Item %s>' %(self.name)
        