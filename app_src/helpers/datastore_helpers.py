# creates populates the db tables with roles and users
# copyright (c) 2018 wildduck.io


# TODO a lot of this should be replaced with some kind of db seed and migration mechanism...


import os

from pytz import utc

from flask import current_app

from flask_security import utils

from flask_security import SQLAlchemyUserDatastore

from sqlalchemy_utils import create_database, drop_database

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # this has to precede the model import.
                   # in this file because I don't love it in the __init__ file

from app_src.gateway_module.models import *

from app_src.job_management_module.models import *

from app_src.offering_attributes.models import *

from app_src.admin import app_roles

from app_src.offering_attributes.offering_roles import *
from app_src.offering_attributes.offering_levels import *
from app_src.offering_attributes.offering_locations import *
from app_src.offering_attributes.offering_sentiments import *


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def init_db():
    """
    ensures db tables are created and populated in the correct order

    Returns:

    """
    __create_db_tables()

    __populate_offering_roles_table()
    __populate_offering_levels_table()
    __populate_offering_locations_table()
    __populate_offering_sentiment_table()

    __populate_roles_table()

    __populate_users_table()


def __create_db_tables():
    """
    creates any db tables that are missing from the db. this is a non-destructive operation if in any mode but DEV

    Returns:

    """

    # can't create or drop databases in prod (and don't want to cycle the db every time we bring up the app unless we're
    # in dev mode anyway...)
    # if os.environ['APP_MODE'] == 'DEV':
        # drop_database(current_app.config['SQLALCHEMY_DATABASE_URI'])
        # create_database(current_app.config['SQLALCHEMY_DATABASE_URI'])

    db.create_all()


def __populate_roles_table():
    """
    populates the roles table with the contents of app_src.common.app_roles

    Returns:

    """
    for app_role_tuple in app_roles.get_app_role_tuples():
        user_datastore.find_or_create_role(name=app_role_tuple[0], description=app_role_tuple[1])
        user_datastore.commit()


def __populate_users_table():
    """
    creates users and assigns roles to them based on config values

    Returns:

    """

    # first check to ensure the roles table has been populated - this won't work if it isn't
    role_table_contents = Role.query.all()
    if len(role_table_contents) == 0:
        raise Exception("roles table must be populated before adding users")

    users_dict_list = current_app.config['USERS_DICT']
    for user_dict in users_dict_list:
        current_app.logger.info('user_dict is: {}'.format(user_dict))
        user_email = user_dict['EMAIL']

        if not user_datastore.get_user(user_email):
            plaintext_password = user_dict['PASSWORD']
            encrypted_password = utils.hash_password(plaintext_password)

            first_name = user_dict['FIRST_NAME']
            last_name = user_dict['LAST_NAME']

            user_roles = user_dict['ROLES']

            user_datastore.create_user(email=user_email,
                                       password=encrypted_password,
                                       first_name=first_name,
                                       last_name=last_name)

            for user_role in user_roles:
                user_datastore.add_role_to_user(user_email, user_role)

            user_datastore.commit()

            user_obj = User.query.filter_by(email=user_email).first()
            user_obj.confirmed_at = datetime.now().astimezone(utc)
            db.session.commit()


def __populate_offering_roles_table():

    for offering_role in get_offering_role_names():

        __add_create_to_db_session_if_not_present(db.session,
                                                  OfferingRole,
                                                  name=offering_role)

    db.session.commit()


def __populate_offering_levels_table():

    for offering_level in get_offering_level_names():

        __add_create_to_db_session_if_not_present(db.session,
                                                  OfferingLevel,
                                                  name=offering_level)

    db.session.commit()


def __populate_offering_locations_table():

    for offering_location in get_offering_locations_names():

        __add_create_to_db_session_if_not_present(db.session,
                                                  OfferingLocation,
                                                  name=offering_location)

    db.session.commit()


def __populate_offering_sentiment_table():

    for offering_sentiment in get_offering_sentiment_names():

        __add_create_to_db_session_if_not_present(db.session,
                                                  OfferingSentiment,
                                                  name=offering_sentiment)

    db.session.commit()


def __get_or_create(session, model, **kwargs):
    """

    Args:
        session:
        model:
        **kwargs:

    Notes:
        https://stackoverflow.com/a/6078058

    Returns:

    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def __add_create_to_db_session_if_not_present(session, model, commit=False, **kwargs):
    """

    Args:
        session: sqlalchemy db session

        model: table model class you want to create if not present

        commit: defaults to False - will commit the new creates to the db if True

        **kwargs:

    Notes:
        https://stackoverflow.com/a/6078058

    Returns:
        True if not present, else False
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return False
    else:
        instance = model(**kwargs)
        session.add(instance)

        if commit:
            session.commit()

        return True
