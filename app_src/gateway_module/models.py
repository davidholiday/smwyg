# users and roles table
# copyright (c) 2018 wildduck.io


from flask_security import UserMixin, RoleMixin

from app_src.helpers.datastore_helpers import db

from app_src.admin.app_roles import *


app_role_to_users = db.Table('app_role_to_users',
                             db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                             db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    confirmed_at = db.Column(db.DateTime(timezone=True))
    current_login_at = db.Column(db.DateTime(timezone=True))
    last_login_at = db.Column(db.DateTime(timezone=True))
    login_count = db.Column(db.Integer(), default=1)
    current_login_ip = db.Column(db.String(42))
    last_login_ip = db.Column(db.String(42))
    resume = db.Column(db.LargeBinary)

    # see below for relationship argument api
    # http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#relationships-api
    roles = db.relationship('Role',
                            secondary=app_role_to_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return '<User id=%s email=%s>' % (self.id, self.email)


# TODO this should be called something else but in order to make that happen you need to
# TODO override and refactor some of the datastore code. not worth doing right now...
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __str__(self):
        return '%s' % (self.name)
