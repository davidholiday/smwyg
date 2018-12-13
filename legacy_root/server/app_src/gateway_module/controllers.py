# handles entry into the app and role-based routing
# copyright (c) 2018 wildduck.io


from flask import Blueprint, request, render_template

from flask_security import login_required, current_user

from app_src.admin.app_roles import *


# TODO don't forget you can use the blueprint constructor to define a prefix for the constituent urls
gateway_blueprint = Blueprint('gateway', __name__)


@gateway_blueprint.route('/', methods=['GET'])
@login_required
def root():
    """
    routes the user to the correct landing page based on their ROLE

    Returns:

    """

    # TODO here remind me later how to do this
    # current_user_role_objects = current_user.roles
    current_user_role_names = [role.name for role in current_user.roles]

    template = 'job_management.html' \
        if ROLE_RECRUITER[0] in current_user_role_names \
        else 'feed_management.html'

    message_bg = 'bg-info'
    message = 'user is: {} {}'.format(current_user, current_user_role_names)
    return render_template(template, message_bg=message_bg, message=message)
