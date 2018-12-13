# creates populates the db tables with roles and users
# copyright (c) 2018 wildduck.io


from pytz import utc

from datetime import datetime

from flask import current_app

from flask_security import utils

from flask_security import SQLAlchemyUserDatastore

from sqlalchemy_utils import database_exists, create_database

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()  # this has to precede the model import.
                   # in this file because I don't love it in the __init__ file

from app_src.gateway_module.models import *

from app_src.admin import app_roles


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def init_db():
    """
    ensures db tables are created and populated in the correct order

    Returns:

    """
    __create_db_tables()
    __populate_roles_table()
    __populate_users_table()


def __create_db_tables():
    """
    non-destructively creates any db tables that are missing from the db

    Returns:

    """
    if not database_exists(current_app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(current_app.config['SQLALCHEMY_DATABASE_URI'])

    db.create_all()


def __populate_roles_table():
    """
    populates the roles table with the contents of app_src.roles

    Returns:

    """
    for role_tuple in app_roles.get_app_role_tuples():
        user_datastore.find_or_create_role(name=role_tuple[0], description=role_tuple[1])
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

            # this to bypass the requirement for a confirmation email
            if current_app.config['BYPASS_SECURITY_EMAIL']:
                user_obj = User.query.filter_by(email=user_email).first()
                user_obj.confirmed_at = datetime.now().astimezone(utc)
                db.session.commit()
