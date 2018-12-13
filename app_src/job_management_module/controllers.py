# handles job management view
# copyright (c) 2018 wildduck.io


import logging, operator

from flask import Blueprint, render_template, current_app, request, flash, jsonify

from flask_security import roles_accepted, current_user, login_required

from app_src.offering_attributes.models import *
from app_src.admin.app_roles import *

from app_src.job_management_module.add_job_form import AddJobForm

from app_src.job_management_module.models import *

from app_src.helpers.template_helpers import *

from app_src.offering_attributes.offering_sentiments import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

job_management_blueprint = Blueprint('job_management_blueprint', __name__)


@job_management_blueprint.route('/api/jobs/data', methods=['GET'])
@roles_accepted(ROLE_RECRUITER, ROLE_ADMIN)
@login_required
def get_job_data():
    """ grabs current_users' offerings and returns to caller a json object containing an offering-centric view
    of what they have and who has interacted with it

    Returns:

    """
    # FIXME you definitely should not have made everything a many2many relation...
    # FIXME this should be handled by querying the db differently...


    # first get a list of jobs owned by the current user
    #
    caller_jobs_db_obj = \
        Jobs.query.filter(
            Jobs.submitted_by.contains(current_user),
        ).all()


    # pull out the salient data from each job rec owned by the current user
    #
    jobs_view_dict = {}
    for caller_job_db_obj in caller_jobs_db_obj:
        jobs_view_dict[caller_job_db_obj.id] = {}
        jobs_view_dict[caller_job_db_obj.id]['id'] = caller_job_db_obj.id
        jobs_view_dict[caller_job_db_obj.id]['job_role'] = caller_job_db_obj.job_role[0].name
        jobs_view_dict[caller_job_db_obj.id]['job_level'] = caller_job_db_obj.job_level[0].name
        jobs_view_dict[caller_job_db_obj.id]['job_location'] = caller_job_db_obj.job_location[0].name

        jobs_view_dict[caller_job_db_obj.id]['submitted_at'] = \
            caller_job_db_obj.submitted_at.strftime('%b %d %Y %I:%M%p GMT')

        jobs_view_dict[caller_job_db_obj.id]['job_sheet'] = caller_job_db_obj.job_rec_name
        jobs_view_dict[caller_job_db_obj.id]['views'] = len(caller_job_db_obj.offering_views.all())


        # figure out what the most popular sentiment is for this rec
        #
        sentiment_dict = {}
        for offering_sentiments in caller_job_db_obj.offering_sentiments.all():
            for sentiment in offering_sentiments.sentiment:
                if sentiment_dict.get(sentiment.name) is None:
                    sentiment_dict[sentiment.name] = 1
                else:
                    sentiment_dict[sentiment.name] += 1

        if len(sentiment_dict) > 0:
            # ty so https://stackoverflow.com/a/613218/2234770
            # returns [ {k:v},... ]
            sorted_sentiment_list = sorted(sentiment_dict.items(), key=operator.itemgetter(1))
            jobs_view_dict[caller_job_db_obj.id]['overall_sentiment'] = sorted_sentiment_list[0][0]
        else:
            jobs_view_dict[caller_job_db_obj.id]['overall_sentiment'] = MEH


        # enumerate through the viewed_by list and create a detail view
        #
        jobs_view_dict[caller_job_db_obj.id]['interaction_detail'] = []

        for offering_view in caller_job_db_obj.offering_views:
            for viewed_by in offering_view.viewed_by:

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

                first_name = viewed_by.first_name
                last_name = viewed_by.last_name
                email = viewed_by.email
                last_login = viewed_by.last_login_at.strftime('%b %d %Y %I:%M%p GMT'),


                sentiment = \
                    MEH \
                        if len(offering_sentiments_list[0].sentiment) is 0 \
                        else offering_sentiments_list[0].sentiment[0].name

                comment = offering_comments_list[0].comment if len(offering_comments_list) > 0 else ""

                jobs_view_dict[caller_job_db_obj.id]['interaction_detail'].append(
                    {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'last_login': last_login,
                        'sentiment': sentiment,
                        'comment': comment
                    }
                )

    # FIXME this whole function is inelegant - aggregating this way is not necessary
    data = [jobs_view_dict[id] for id in jobs_view_dict.keys()]
    return_dict = { 'data': data, }
    return jsonify(return_dict)


@job_management_blueprint.route('/jobs', methods=['GET', 'POST'])
@roles_accepted(ROLE_RECRUITER, ROLE_ADMIN)
@login_required
def jobs():
    """
    returns the job management page

    Returns:

    """
    form = AddJobForm(request.form)

    # validate_on_submit() is a shortcut for is_submitted() and validate()
    if request.method == "POST" and form.validate_on_submit():
        job_level = [value for id, value in form.job_level_list.choices if id == form.job_level_list.data][0]
        job_role = [value for id, value in form.job_role_list.choices if id == form.job_role_list.data][0]
        job_location = [value for id, value in form.job_location_list.choices if id == form.job_location_list.data][0]
        job_rec = form.job_rec.data

        # fields that are FK holders and hold M2M relationships need to be set as the db object, not value
        #
        # see
        # https://stackoverflow.com/a/19777181
        # https://stackoverflow.com/a/33083837
        new_job_db_entry = Jobs(
            job_level=OfferingLevel.query.filter_by(name=job_level).all(),
            job_role=OfferingRole.query.filter_by(name=job_role).all(),
            job_location=OfferingLocation.query.filter_by(name=job_location).all(),
            job_rec_name=job_rec.filename,
            job_rec_file=job_rec.stream.read(),
            submitted_by=[current_user]
        )

        # TODO surrouind this in a try/except to capture+report errors to caller
        db.session.add(new_job_db_entry)
        db.session.commit()
        flash('job rec submitted!', 'success')

        # # FIXME don't leave this here
        # offering = Jobs.query.filter_by(job_rec_name=job_rec.filename).first()
        # test_offering_view_db_entry = OfferingViews(
        #     viewed_by=[current_user],
        #     offering=[offering],
        # )
        # db.session.add(test_offering_view_db_entry)
        # db.session.commit()
        # flash('you need to disable this b4 prod!', 'warning')

    # 'errors' is a dict that has a list of errors as values
    # http://wtforms.readthedocs.io/en/latest/forms.html#wtforms.form.Form.errors
    elif form.is_submitted() and not form.validate():
        for error_list in form.errors.values():
            flash('Something went wrong submitting the job rec!', 'danger')
            for error in error_list:
                current_app.logger.info('form errors: {}'.format(error))
                message_text = 'FORM ERROR: {}'.format(error)
                message_category = 'danger'
                flash(message_text, message_category)

    template = 'job_management.html'

    user_role_list = [current_user_role.name for current_user_role in current_user.roles]
    hamburger_menu_items = get_hamburger_menu_items_by_role(user_role_list)

    return render_template(template,
                           form=form,
                           provider_id=current_user.id,
                           hamburger_menu_items=hamburger_menu_items)


