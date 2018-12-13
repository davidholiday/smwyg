# flask app configuration values
# copyright (c) 2018 wildduck.io


import os

from app_src.admin.app_roles import *


class Config(object):

    # set host to something that hooks into docker nicely
    HOST = "0.0.0.0"

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # for signing cookies
    SECRET_KEY = 'a501412c-b278-43f6-a5e6-5c120e7a030f'

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for signing the data.
    CSRF_SESSION_KEY = '2da17496-d3e8-42ab-bd77-c8e83bf7a4ec'

    # don't need to track anything at this time. see https://stackoverflow.com/a/33790196 for insight
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # adds a little someth'n someth'n to the password hashing
    SECURITY_PASSWORD_SALT = "08357c20-b607-4cc9-9990-11ecaa3d98bf"

    # Specifies if users are required to confirm their email address when registering a new account.
    SECURITY_CONFIRMABLE = True

    # Specifies if Flask-Security should create a user registration endpoint.
    SECURITY_REGISTERABLE = True

    # Specifies if Flask-Security should create a password reset/recover endpoint.
    SECURITY_RECOVERABLE = True

    # Specifies if Flask-Security should track basic user login statistics.
    SECURITY_TRACKABLE = True

    # Specifies if Flask-Security should enable the change password endpoint.
    SECURITY_CHANGEABLE = True

    # mail settings
    #
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SECURITY_EMAIL_SENDER = 'no-reply@showmewhatyougot.io'
    MAIL_USERNAME = 'no-reply@showmewhatyougot.io'
    MAIL_PASSWORD = '86755635-fdfd-4903-b4ee-d830fa87d258'
    BYPASS_SECURITY_EMAIL = False


class DevConfig(Config):

    # Statement for enabling the development environment
    DEBUG = True

    # URI of the db
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@wd_alpha_postgres/db1'

    # test users - one for each role
    USERS_DICT = [

        {
            'EMAIL': 'a@a.com',
            'PASSWORD': 'password',
            'FIRST_NAME': 'first',
            'LAST_NAME': 'name',
            'ROLES': [ROLE_ADMIN]
        },
        {
            'EMAIL': 'r@r.com',
            'PASSWORD': 'password',
            'FIRST_NAME': 'first',
            'LAST_NAME': 'name',
            'ROLES': [ROLE_RECRUITER]
        },
        {
            'EMAIL': 't@t.com',
            'PASSWORD': 'password',
            'FIRST_NAME': 'first',
            'LAST_NAME': 'name',
            'ROLES': [ROLE_TALENT]
        }

    ]

    # tells init_db() it's ok to auto-confirm users it creates
    BYPASS_SECURITY_EMAIL = True



class ProdConfig(Config):

    # Statement for enabling the development environment
    DEBUG = False

    # FIXME see https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
    # FIXME the AWS db is set up to deny public access
    # URI of the db
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://wildduck1138:G}GJ;cWoaM%2xy`j@wd-alpha-rds.cgemtimccgvb.us-west-2.rds.amazonaws.com/db1'

    # only an admin role for prod
    USERS_DICT = [

        {
            'EMAIL': 'david@wildduck.io',
            'PASSWORD': '779207dc-780e-414a-951a-e12ba11bd689',
            'FIRST_NAME': 'David',
            'LAST_NAME': 'Holiday',
            'ROLES': [ROLE_ADMIN]
        }

    ]

