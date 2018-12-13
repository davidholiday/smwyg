# handles talent management view
# copyright (c) 2018 wildduck.io


import logging

from flask import Blueprint, render_template, make_response, current_app, request, flash, jsonify

from flask_security import roles_accepted, current_user, login_required

from app_src.offering_attributes.models import *

from app_src.job_management_module.models import *

from app_src.helpers.template_helpers import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


talent_management_blueprint = Blueprint('talent_management_blueprint', __name__)


@talent_management_blueprint.route('/api/talent/interactions', methods=['GET'])
@roles_accepted(ROLE_RECRUITER, ROLE_ADMIN)
@login_required
def get_talent_views():
    """ for a given content provider this grabs both a summary and detail view of who has viewed their content and
    what the interactions were

    Returns:

    """
    # FIXME you definitely should not have made everything a many2many relation...

    # FIXME this should be handled by querying the db differently...

    # first get a list of jobs owned by the current user
    caller_jobs_db_obj = \
        Jobs.query.filter(
            Jobs.submitted_by.contains(current_user),
        ).all()

    # TODO this is from rhys
    # Start with the jobs that are owned by the current (recruiter) user,
    # then for each job object, get the viewed_by object
    # and derive comments and sentiments from that
    # '''
    # caller_jobs_db_obj = \
    #     Jobs.query.filter(
    #         Jobs.submitted_by.contains(current_user),
    #     )\
    #     .join(OfferingViews, OfferingViews.offering == Jobs.id)\
    #     .join(User, User.id == OfferingViews.viewed_by)\
    #     .join(OfferingComments, OfferingComments.submitted_by == User.id)\
    #     .join(OfferingSentiments, OfferingSentiments.submitted_by == User.id)\
    #     .join(OfferingSentiment, OfferingSentiment.id == OfferingSentiments.sentiment)\
    #     .all()

    # now for each jobrec update talent_view_dict with who has seen it
    talent_view_dict = {}
    for caller_job_db_obj in caller_jobs_db_obj:
        for offering_view in caller_job_db_obj.offering_views:
            for viewed_by in offering_view.viewed_by:

                if viewed_by.id == current_user.id:
                    continue

                # DON'T FORGET YOU ARE DEALING WITH A SQLALCHEMY BASE QUERY OBJECT IN THESE CROSS REFERENCE TABLES
                # ALSO -- even though all of this is coming out as lists -- for comments and sentiments, because we're
                # querying based on the viewed_by User object we know there's only ever going to be one comment or
                # sentiment per job rec for any given user
                offering_sentiments_list = \
                    viewed_by.offering_sentiments.filter(
                        OfferingSentiments.offering.contains(caller_job_db_obj)
                    ).all()

                offering_comments_list = \
                    viewed_by.offering_comments.filter(
                        OfferingComments.offering.contains(caller_job_db_obj),
                    ).all()

                if talent_view_dict.get(viewed_by.id) is None:
                    talent_view_dict[viewed_by.id] = {}
                    talent_view_dict[viewed_by.id]['user_data'] = None
                    talent_view_dict[viewed_by.id]['interaction_detail'] = []

                if talent_view_dict[viewed_by.id]['user_data'] is None:
                    talent_view_dict[viewed_by.id]['user_data'] = {
                        'user_id': viewed_by.id,
                        'first_name': viewed_by.first_name,
                        'last_name': viewed_by.last_name,
                        'email': viewed_by.email,
                        'last_login': viewed_by.last_login_at.strftime('%b %d %Y %I:%M%p GMT'),
                    }

                talent_view_dict[viewed_by.id]['interaction_detail'].append(
                    {
                        'job_role': caller_job_db_obj.job_role[0].name,
                        'job_level': caller_job_db_obj.job_level[0].name,
                        'job_location': caller_job_db_obj.job_location[0].name,
                        'job_rec_name': caller_job_db_obj.job_rec_name,
                        'sentiment': offering_sentiments_list[0].sentiment[0].name,
                        'comment': offering_comments_list[0].comment if len(offering_comments_list) > 0 else ""
                    }
                )

    # aggregate
    for key in talent_view_dict.keys():
        number_jobs_viewed = len(talent_view_dict[key]['interaction_detail'])
        talent_view_dict[key]['user_data']['interactions'] = number_jobs_viewed
        talent_view_dict[key]['user_data']['interaction_detail'] = talent_view_dict[key]['interaction_detail']

    # put into a form the jquery datatable can easily deal with
    data = [talent_view_dict[id]['user_data'] for id in talent_view_dict.keys()]

    return_dict = {
        'status': 'success',
        'data': data,
    }

    return jsonify(return_dict)


@talent_management_blueprint.route('/talent', methods=['GET', 'POST'])
@roles_accepted(ROLE_RECRUITER, ROLE_ADMIN)
@login_required
def talent():
    """
    returns the talent management page

    Returns:

    """

    template = 'talent_management.html'
    user_role_list = [current_user_role.name for current_user_role in current_user.roles]
    hamburger_menu_items = get_hamburger_menu_items_by_role(user_role_list)

    return render_template(template, hamburger_menu_items=hamburger_menu_items)


