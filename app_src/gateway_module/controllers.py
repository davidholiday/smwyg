# handles entry into the app and role-based routing
# copyright (c) 2018 wildduck.io


import logging

from flask import Blueprint, render_template, current_app, redirect, url_for, request

from flask_security import login_required, current_user

from flask_login import current_user

from app_src.admin.app_roles import *

from app_src.helpers.template_helpers import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# TODO don't forget you can use the blueprint constructor to define a prefix for the constituent urls
gateway_blueprint = Blueprint('gateway_blueprint', __name__)


@gateway_blueprint.route('/', methods=['GET'])
@login_required
def root():
    """
    routes the user to the correct landing page based on their ROLE

    Returns:

    """
    current_user_role_names = [app_role.name for app_role in current_user.roles]

    if ROLE_ADMIN in current_user_role_names:
        redirect_url = 'admin.index'
    elif ROLE_RECRUITER in current_user_role_names:
        redirect_url = 'job_management_blueprint.jobs'
    else:
        redirect_url = 'gateway_blueprint.base'

    return redirect(url_for(redirect_url))


@gateway_blueprint.route('/base', methods=['GET'])
@login_required
def base():
    """
    default endpoint for root() to use as a catch all

    Returns:

    """
    current_user_role_names = [app_role.name for app_role in current_user.roles]
    hamburger_menu_items = get_hamburger_menu_items_by_role(current_user_role_names)

    message_bg = 'bg-info'

    message = "if you are seeing this it is probably because you're not a recruiter or admin user. " \
              "this first version of the app doesn't yet have the capability to allow talent (that's you!) to seek " \
              "out job recs on your own (it will soon, I promise!)." \
              "in the mean time enjoy the lovely gif and have a rad day!"

    return render_template(
        'index.html',
        message_bg=message_bg,
        message=message,
        hamburger_menu_items=hamburger_menu_items
    )


@gateway_blueprint.route('/error', methods=['GET'])
@login_required
def error():
    """
    enables failed ajax requests to post on fail which will trigger the error view

    Returns:

    """
    return render_template(
        'error.html',
        message_bg="bg-danger",
        error_code="500",
        error_text="template reported error (probably an ajax call)"
    )

