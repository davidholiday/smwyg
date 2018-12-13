# custom views for the admin pages that ensure the mapping between user and role is represented
# copyright (c) 2018 wildduck.io


from flask import current_app

from flask_login import current_user

from flask_admin.contrib.sqla import ModelView

from app_src.admin.app_roles import *


# FIXME you need to settle on whether or not these are 'jobs' or 'offerings'

# FIXME I think you can make only one class for all these single k/v tables...


class __AdminViewMixin(object):
    """
        security intercept that prevents access to admin view to only users with ADMIN role

    """

    admin_role = ROLE_ADMIN


    def base_is_accessible(self):
        """
        rejects all users who aren't active, authenticated, and has the ADMIN role

        Returns:

        """

        return_val = False

        if current_user.is_active \
                and current_user.is_authenticated \
                and current_user.has_role(self.admin_role):

            return_val = True

        return return_val


class UserView(ModelView, __AdminViewMixin):
    """
        Parrots the User table model and adds a request intercept to prevent unauthorized access

    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()

    # prevents Type Error can't convert str to bin --> basically we're telling the admin view not to
    # dork with the LargeBinary column in the db
    column_exclude_list = ['resume']
    form_excluded_columns = ['resume']


class AppRoleView(ModelView, __AdminViewMixin):
    """
        Parrots the Role table model and adds a request intercept to prevent unauthorized access

    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()


class JobRoleView(ModelView, __AdminViewMixin):
    """
        Parrots the JobRole table model and adds a request intercept to prevent unauthorized access

    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()


class JobLevelView(ModelView, __AdminViewMixin):
    """
        Parrots the JobLevel table model and adds a request intercept to prevent unauthorized access

    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()


class JobLocationsView(ModelView, __AdminViewMixin):
    """
        Parrots the JobLocations table model and adds a request intercept to prevent unauthorized access

    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()


class JobSentimentView(ModelView, __AdminViewMixin):
    """
        Parrots the JobsSentiment table model and adds a request intercept to prevent unauthorized access

    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()


class JobsView(ModelView, __AdminViewMixin):
    """
        Parrots the Jobs table model and adds a request intercept to prevent unauthorized access

    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()

    # prevents Type Error can't convert str to bin --> basically we're telling the admin view not to
    # dork with the LargeBinary column in the db
    column_exclude_list = ['job_rec_file']
    form_excluded_columns = ['job_rec_file']



class OfferingViewsView(ModelView, __AdminViewMixin):
    """
    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()


class OfferingCommentsView(ModelView, __AdminViewMixin):
    """
    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()


class OfferingSentimentsView(ModelView, __AdminViewMixin):
    """
    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()
