# handles both feed management and feed api endpoints
# copyright (c) 2018 wildduck.io


from urllib.request import urlopen

import os

import logging

from io import BytesIO

from werkzeug.exceptions import Forbidden, InternalServerError

from flask import Blueprint, render_template, current_app, redirect, url_for, request, jsonify, send_file, flash

from flask_security import login_required, current_user

from flask_login import current_user

from sqlalchemy.sql import not_

from app_src import csrf

from app_src.job_management_module.models import *

from app_src.offering_attributes.models import *
from app_src.offering_attributes.offering_sentiments import *

from app_src.gateway_module.models import *

from app_src.helpers.template_helpers import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

feed_blueprint = Blueprint('feed_blueprint', __name__)


@feed_blueprint.route('/feed/done', methods=['GET'])
@login_required
def done():
    """
    TODO this needs to pull from a table of funky stuff

    Returns:

    """
    current_user_role_names = [app_role.name for app_role in current_user.roles]
    hamburger_menu_items = get_hamburger_menu_items_by_role(current_user_role_names)
    return render_template('all_done.html', hamburger_menu_items=hamburger_menu_items)




@feed_blueprint.route('/feed/next/<feed_provider_id>/<offering_level_id>/<offering_role_id>/<offering_location_id>',
                      methods=['GET', 'POST'])
@csrf.exempt # FIXME don't leave this enabled in prod!
@login_required
def feed_iterator(feed_provider_id, offering_level_id, offering_role_id, offering_location_id):
    """
    [GET] --> method will return the first jobsheet the user hasn't already seen that matches the filter criteria

    [POST] --> method will receive and validate caller supplied metadata on provided job rec and the method will first
    mark that rec as 'viewed', then return a fresh one if available. if one is unavailable the caller will be routed to
    a 'good job here's your cookie' page.
    
    Note that we're not paginating because every time the user pollinates an offering that needs to be posted to the db

    *! this is a lot of db round trips - in future it's probably going to make sense to pass a set of things to the
    client app (hopefully an SPA at that point) and refactor this endpoint so it only has to update the pollination
    tables... !*

    """

    # if POST update the db with what was viewed and respond with status code
    if request.method == 'POST':
        payload_dict = request.json

        # update job record with who has just viewed it
        #
        viewed_job = Jobs.query.filter_by(id=payload_dict['job_id'])[0]
        new_offering_view = OfferingViews(viewed_by=[current_user], offering=[viewed_job])
        db.session.add(new_offering_view)

        # update job record with user comment if present
        #
        if payload_dict['user_comment'] != "":
            new_user_comment = OfferingComments(
                submitted_by=[current_user],
                offering=[viewed_job],
                comment=payload_dict['user_comment']
            )
            db.session.add(new_user_comment)

        # update job record with user sentiment
        #
        user_sentiment = payload_dict['user_sentiment']
        if user_sentiment not in get_offering_sentiment_names():
            raise ValueError(
                'user sentiment {} not a member of valid sentiment list {}!'
                    .format(user_sentiment, get_offering_sentiment_names())
            )

        offering_sentiment_db_obj = OfferingSentiment.query.filter_by(name=user_sentiment)[0]

        new_offering_sentiment = OfferingSentiments(
            submitted_by=[current_user],
            offering=[viewed_job],
            sentiment=[offering_sentiment_db_obj]
        )
        db.session.add(new_offering_sentiment)

        # commit and we're out
        #
        try:
            db.session.commit()
        except Exception as e:
            logger.error(e)
            raise InternalServerError

        return jsonify(success=True)

    # else, if we're here we're dealing with a GET request
    # grab the next offering the caller hasn't seen yet. if none route them to the 'no more' page.
    template = "feed_slide.html"
    current_user_role_names = [app_role.name for app_role in current_user.roles]
    hamburger_menu_items = get_hamburger_menu_items_by_role(current_user_role_names)

    next_offering = __get_next_offering(current_user,
                                        feed_provider_id,
                                        offering_level_id,
                                        offering_role_id,
                                        offering_location_id)


    # FIXME
    # FIXME
    # TODO this needs to throw you into an 'all done' slide
    if next_offering is None:
        redirect_url = 'feed_blueprint.done'
        return redirect(url_for(redirect_url))
        # return render_template("index.html",
        #                        message="no more recs for you!",
        #                        message_bg="bg-warning",
        #                        hamburger_menu_items=hamburger_menu_items)
    else:
        doc_url = request.host_url + 'api/jobrec/' + str(next_offering.id) + '/' + next_offering.job_rec_name

        number_comments = len([comment for comment in next_offering.offering_comments])
        number_sentiments = len([sentiment for sentiment in next_offering.offering_sentiments])

        help_text = ""
        help_text_file_path = os.path.join( os.path.dirname(__file__), '../static/help.md')
        logger.info(os.path.join( os.path.dirname(__file__), '../static/help.md') )

        with open(help_text_file_path, 'r') as help_desk_file:
            help_text = help_desk_file.read()

        if os.environ['APP_MODE'] == 'DEV':
            flash(next_offering.job_rec_name, "info")

        # set sentiment, comment, and doc_id template variables so it'll be easy to post them back later
        return render_template(
            template,
            feed_url=request.url,
            offering_sentiments=get_offering_sentiment_names(),
            number_comments=number_comments,
            number_sentiments=number_sentiments,
            user_sentiment=MEH, # FIXME
            user_comment="", # FIXME
            help_text=help_text,
            doc_url=doc_url,
            job_id=next_offering.id,
            hamburger_menu_items=hamburger_menu_items,
        )


def __get_next_offering(current_user, feed_provider_id, offering_level_id, offering_role_id, offering_location_id):
    """

    Args:
        current_user:
        feed_provider_id:
        offering_level_id:
        offering_role_id:
        offering_location_id:

    Returns:

    """

    # ty so
    #
    #
    # the cross reference tables have to be filtered differently because the cell value is a reference to
    # another table. here, again, you probably should revisit whether or not it was a good idea to make all your
    # table relations m2m...
    #
    # the not business was more painful than it probably should be due I suspect to a difference between
    # sql-alchemy and flask-sql-alchemy
    #
    # ty so
    # https://stackoverflow.com/questions/5018694/how-to-pass-a-not-like-operator-in-a-sqlalchemy-orm-query
    # https://stackoverflow.com/questions/26182027/how-to-use-not-in-clause-in-sqlalchemy-orm-query
    # https://stackoverflow.com/a/26050043
    #
    # RTFM
    # http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.ColumnProperty.Comparator.any
    next_offering = Jobs.query \
        .filter(
            db.not_(Jobs.offering_views.any(OfferingViews.viewed_by.contains(current_user))),
            Jobs.submitted_by.any(User.id == feed_provider_id),
            Jobs.job_level.any(OfferingLevel.id == offering_level_id),
            Jobs.job_role.any(OfferingRole.id == offering_role_id),
            Jobs.job_location.any(OfferingLocation.id == offering_location_id)
        ) \
        .first()

    return next_offering


@feed_blueprint.route('/api/jobrec/<job_rec_id>/<job_rec_name>', methods=['GET'])
def get_file(job_rec_id, job_rec_name):
    """
    retrieves a given job_rec iff the caller is the rendering engine or has the ADMIN role

    Args:
        job_rec_id(str): record id in the jobs table from which to grab the job rec

        job_rec_name(str): name of the file - this is required to force callers to ask for something specific

    Returns:
        job_rec file data

    """
    # the filename filter is a layer of security to ensure the caller has to ask for a specific filename
    response_record = Jobs.query.filter_by(
        id=job_rec_id,
        job_rec_name=job_rec_name
    ).first()

    job_rec_file_data = response_record.job_rec_file
    return send_file(BytesIO(job_rec_file_data), attachment_filename=job_rec_name, as_attachment=False)


