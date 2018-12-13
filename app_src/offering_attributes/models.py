# table models for offering attributes
# copyright (c) 2018 wildduck.io


from datetime import datetime

from app_src.helpers.datastore_helpers import db


# FIXME clean up your naming conventions - jobs or offerings?

# TODO at some point you're going to need to evaluate these relationships - do they all need to be many 2 many?


"""
-------------------
STATIC VALUE MODELS
-------------------
"""


class OfferingRole(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __str__(self):
        return '<id=%s name=%s' % (self.id, self.name)


class OfferingLevel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __str__(self):
        return '<id=%s name=%s' % (self.id, self.name)


class OfferingLocation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __str__(self):
        return '<id=%s name=%s' % (self.id, self.name)


class OfferingSentiment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __str__(self):
        return '<id=%s name=%s' % (self.id, self.name)


"""
----------------------
CROSS REFERENCE TABLES
----------------------
"""

# views cross ref
#
offering_views_viewed_by = \
    db.Table('offering_views_viewed_by',
             db.Column('offering_views_id', db.Integer(), db.ForeignKey('offering_views.id')),
             db.Column('user_id', db.Integer(), db.ForeignKey('user.id')))

offering_views_offering = \
    db.Table('offering_views_offering',
             db.Column('offering_views_id', db.Integer(), db.ForeignKey('offering_views.id')),
             db.Column('jobs_id', db.Integer(), db.ForeignKey('jobs.id')))


# comments cross ref
#
offering_comments_submitted_by = \
    db.Table('offering_comments_submitted_by',
             db.Column('offering_comments_id', db.Integer(), db.ForeignKey('offering_comments.id')),
             db.Column('user_id', db.Integer(), db.ForeignKey('user.id')))

offering_comments_offering = \
    db.Table('offering_comments_offering',
             db.Column('offering_comments_id', db.Integer(), db.ForeignKey('offering_comments.id')),
             db.Column('jobs_id', db.Integer(), db.ForeignKey('jobs.id')))


# sentiments cross ref
#
offering_sentiments_sentiment = \
    db.Table('offering_sentiments_sentiment',
             db.Column('offering_sentiments_id', db.Integer(), db.ForeignKey('offering_sentiments.id')),
             db.Column('offering_sentiment_id', db.Integer(), db.ForeignKey('offering_sentiment.id')))

offering_sentiments_submitted_by = \
    db.Table('offering_sentiments_submitted_by',
             db.Column('offering_sentiments_id', db.Integer(), db.ForeignKey('offering_sentiments.id')),
             db.Column('user_id', db.Integer(), db.ForeignKey('user.id')))

offering_sentiments_offering = \
    db.Table('offering_sentiments_offering',
             db.Column('offering_sentiments_id', db.Integer(), db.ForeignKey('offering_sentiments.id')),
             db.Column('jobs_id', db.Integer(), db.ForeignKey('jobs.id')))


"""
----------------------
CROSS REFERENCE MODELS
----------------------
"""

class OfferingViews(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    viewed_by = db.relationship('User',
                                secondary=offering_views_viewed_by,
                                backref=db.backref('offering_views', lazy='dynamic'))

    offering = db.relationship('Jobs',
                               secondary=offering_views_offering,
                               backref=db.backref('offering_views', lazy='dynamic'))

    submitted_at = db.Column(db.DateTime(timezone=True), default=datetime.now())

    def __str__(self):
        return '<id=%s viewed_by=%s offering=%s' % (self.id, self.viewed_by, self.offering)


class OfferingComments(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String(420), nullable=False)

    submitted_by = db.relationship('User',
                                   secondary=offering_comments_submitted_by,
                                   backref=db.backref('offering_comments', lazy='dynamic'))

    offering = db.relationship('Jobs',
                               secondary=offering_comments_offering,
                               backref=db.backref('offering_comments', lazy='dynamic'))

    submitted_at = db.Column(db.DateTime(timezone=True), default=datetime.now())


class OfferingSentiments(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    sentiment = db.relationship('OfferingSentiment',
                                secondary=offering_sentiments_sentiment,
                                backref=db.backref('offering_sentiments', lazy='dynamic'))

    submitted_by = db.relationship('User',
                                   secondary=offering_sentiments_submitted_by,
                                   backref=db.backref('offering_sentiments', lazy='dynamic'))

    offering = db.relationship('Jobs',
                               secondary=offering_sentiments_offering,
                               backref=db.backref('offering_sentiments', lazy='dynamic'))

    submitted_at = db.Column(db.DateTime(timezone=True), default=datetime.now())

