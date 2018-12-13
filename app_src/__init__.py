# assembles the flask app_src and db objects
# copyright (c) 2018 wildduck.io


import os
import logging

from werkzeug.exceptions import HTTPException

from flask import Flask, url_for, render_template, make_response

from flask_sslify import SSLify

from flask_admin import Admin
from flask_admin import helpers as admin_helpers

from flask_bootstrap import Bootstrap

from flask_security import Security
from flask_security.forms import RegisterForm

from wtforms.fields.core import StringField
from wtforms.validators import DataRequired

from flask_wtf.csrf import CSRFProtect

from flask_mail import Mail

# needs to happen before the models import
from app_src.helpers.datastore_helpers import init_db, user_datastore
from app_src.helpers.template_helpers import *

from app_src.gateway_module.controllers import gateway_blueprint
from app_src.gateway_module.models import *

from app_src.job_management_module.models import *
from app_src.job_management_module.controllers import job_management_blueprint

from app_src.talent_management_module.controllers import talent_management_blueprint


from app_src.admin.admin_model_views import *

from app_src.offering_attributes.models import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# FIXME this file has gotten ridiculous -- after MVP this needs to be restructured

# create and configure flask app object
app = Flask(__name__)

if 'APP_MODE' in os.environ.keys():
    if os.environ['APP_MODE'] == 'PROD':
        app.config.from_object('config.ProdConfig')
    elif os.environ['APP_MODE'] == 'DEV':
        app.config.from_object('config.DevConfig')
else:
    os.environ['APP_MODE'] = 'DEV'
    app.config.from_object('config.DevConfig')


# forces SSL if app is running on Heroku
if 'DYNO' in os.environ:
    sslify = SSLify(app)


# not sure if I love having this here but it's ok for now. this is to replace the default error page with the larry one
@app.errorhandler(Exception)
@app.errorhandler(404)
def handle_error(e):
    error_code = 500
    error_text = str(e)
    message_bg = 'bg-danger'
    hamburger_menu = get_hamburger_menu_items_by_role([])

    if isinstance(e, HTTPException):
        error_code = e.code

    logger.exception(e)

    return make_response(
        render_template(
            'error.html',
            error_text=error_text,
            error_code=error_code,
            message_bg=message_bg,
            hamburger_menu=hamburger_menu
        ),
        error_code
    )


# applies CSRF protection to non FlaskForms
# https://flask-wtf.readthedocs.io/en/stable/csrf.html
csrf = CSRFProtect(app)


# for flask bootstrap integration
Bootstrap(app)


# enables email capability
mail = Mail(app)


# initializes SQLAlchemy
db.init_app(app)


# initializes Flask Security

# FIXME don't like this form here
class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])

security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)


# register blueprints
app.register_blueprint(gateway_blueprint)
app.register_blueprint(job_management_blueprint)
app.register_blueprint(talent_management_blueprint)

# FIXME don't leave this in this state -- here because I want to temporarily disable something in feeds controller...
from app_src.feed_module.controllers import feed_blueprint
app.register_blueprint(feed_blueprint)


# creates the admin panel
# FIXME build this elsewhere...
admin = Admin(app, name='SHOW ME WHAT YOU GOT! v0.0.1-ALPHA', template_mode='bootstrap3', url="/peekaboo")

user_modelview_with_roles = UserView(User, db.session)
admin.add_view(user_modelview_with_roles)

app_role_modelview = AppRoleView(Role, db.session)
admin.add_view(app_role_modelview)

job_role_modelview = JobRoleView(OfferingRole, db.session)
admin.add_view(job_role_modelview)

job_level_modelview = JobLevelView(OfferingLevel, db.session)
admin.add_view(job_level_modelview)

job_locations_modelview = JobLocationsView(OfferingLocation, db.session)
admin.add_view(job_locations_modelview)

job_sentiments_modelview = JobSentimentView(OfferingSentiment, db.session)
admin.add_view(job_sentiments_modelview)

jobs_modelview = JobsView(Jobs, db.session)
admin.add_view(jobs_modelview)

offering_views_modelview = OfferingViewsView(OfferingViews, db.session)
admin.add_view(offering_views_modelview)

offering_comments_modelview = OfferingCommentsView(OfferingComments, db.session)
admin.add_view(offering_comments_modelview)

offering_sentiments_modelview = OfferingSentimentsView(OfferingSentiments, db.session)
admin.add_view(offering_sentiments_modelview)


# ensures the db tables are created and seeded prior to accepting requests
@app.before_first_request
def before_first_request():
    init_db()


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
)
