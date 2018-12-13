# jobs table(s)
# copyright (c) 2018 wildduck.io


from datetime import datetime

from app_src.helpers.datastore_helpers import db


job_roles = db.Table('job_roles',
                     db.Column('jobs_id', db.Integer(), db.ForeignKey('jobs.id')),
                     db.Column('offering_role_id', db.Integer(), db.ForeignKey('offering_role.id')))

job_levels = db.Table('job_levels',
                      db.Column('jobs_id', db.Integer(), db.ForeignKey('jobs.id')),
                      db.Column('offering_level_id', db.Integer(), db.ForeignKey('offering_level.id')))

job_locations = db.Table('job_locations',
                         db.Column('jobs_id', db.Integer(), db.ForeignKey('jobs.id')),
                         db.Column('offering_location_id', db.Integer(), db.ForeignKey('offering_location.id')))

job_submitted_by = db.Table('job_submitted_by',
                            db.Column('jobs_id', db.Integer(), db.ForeignKey('jobs.id')),
                            db.Column('user_id', db.Integer(), db.ForeignKey('user.id')))


class Jobs(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    # comments
    # views
    # overall_sentiment

    # see below for relationship argument api
    # http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#relationships-api
    job_role = db.relationship('OfferingRole',
                               secondary=job_roles,
                               backref=db.backref('jobs', lazy='dynamic'))

    job_level = db.relationship('OfferingLevel',
                                secondary=job_levels,
                                backref=db.backref('jobs', lazy='dynamic'))

    job_location = db.relationship('OfferingLocation',
                                   secondary=job_locations,
                                   backref=db.backref('jobs', lazy='dynamic'))

    submitted_by = db.relationship('User',
                                   secondary=job_submitted_by,
                                   backref=db.backref('jobs', lazy='dynamic'))

    submitted_at = db.Column(db.DateTime(timezone=True), default=datetime.now())

    active = db.Column(db.Boolean(), default=False)

    job_rec_name = db.Column(db.String(255), nullable=False)

    # TODO this is only okay for MVP purposes -- if this becomes a thing we'll have to put job recs somewhere else.
    # TODO not putting this in s3 because I want these files local for rapid xport to user
    job_rec_file = db.Column(db.LargeBinary(), nullable=False)

    def __str__(self):
        return '<Job id=%s>' % (self.id)

    # ty so https://stackoverflow.com/a/11884806
    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c
            in self.__table__.columns
            if
                c.name != '_sa_instance_state' and
                c.name != 'submitted_at' and
                c.name != 'active'
        }


