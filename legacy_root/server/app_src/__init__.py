# assembles the flask app_src and db objects
# copyright (c) 2018 wildduck.io

from flask import Flask, url_for

from flask_admin import Admin
from flask_admin import helpers as admin_helpers

from flask_bootstrap import Bootstrap

from flask_security import Security

from flask_mail import Mail

# needs to happen before the models import
from app_src.helpers.datastore_helpers import init_db, user_datastore

from app_src.gateway_module.controllers import gateway_blueprint

from app_src.gateway_module.models import *

from app_src.admin.admin_model_views import *


# create gateway_module object with configuration
app = Flask(__name__)
app.config.from_object('config.DevConfig')


# for flask bootstrap integration
Bootstrap(app)


# enables email capability
mail = Mail(app)


# initializes SQLAlchemy
db.init_app(app)


# initializes Flask Security
security = Security(app, user_datastore)


# register blueprints
app.register_blueprint(gateway_blueprint)


# creates the admin panel
admin = Admin(app, name='SMWYG ALPHA', template_mode='bootstrap3')

user_modelview_with_roles = UserView(User, db.session)
admin.add_view(user_modelview_with_roles)

role_modelview = AppRoleView(Role, db.session)
admin.add_view(role_modelview)


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
