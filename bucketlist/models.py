from bucketlist import db
from datetime import datetime

class User(db.Model):
    """
    This class represents User table
    """

    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True)
    password = db.Column(db.String(100))


    def __repr__(self):
        return '<User %r>' % self.username

class Bucketlist(db.Model):
    """
    This class reprewsents Bucketlist tables
    """

    __tablename__ = 'Bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey('Users.id'))
    items = db.relationship('Item', backref='Bucketlist',
                            cascade='all, delete', lazy='dynamic')
    
    def __repr__(self):
        return '<BucketList %s>' % (self.name)

class Items(db.Models):
    """
    This class represents Items inthe buckelets table
    """
    __tablename__ = 'Items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        return '<Items %s>' %(self.name)