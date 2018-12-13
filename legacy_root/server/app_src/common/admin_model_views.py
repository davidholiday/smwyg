# custom views for the admin pages that ensure the mapping between user and role is represented
# copyright (c) 2018 wildduck.io


from flask import current_app

from flask_login import current_user

from flask_admin.contrib.sqla import ModelView

from app_src.admin.app_roles import *


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


    # define the view
    #
    can_view_details = True

    column_list = [
        'first_name',
        'last_name',
        'email',
        'password',
        'roles',
        'active',
        'confirmed_at',
        'last_login_at',
        'current_login_at',
        'last_login_ip',
        'current_login_ip',
        'login_count',
    ]

    column_default_sort = ('last_name', False)

    column_filters = [
        'first_name',
        'last_name',
        'email',
        'password',
        'active',
        'roles.name',
        'confirmed_at',
        'last_login_at',
        'current_login_at',
        'last_login_ip',
        'current_login_ip',
        'login_count',
    ]

    column_details_list = [
        'first_name',
        'last_name',
        'email',
        'password',
        'active',
        'roles',
        'confirmed_at',
        'last_login_at',
        'current_login_at',
        'last_login_ip',
        'current_login_ip',
        'login_count',
    ]

    form_columns = [
        'first_name',
        'last_name',
        'email',
        'password',
        'active',
        'roles',
        'confirmed_at',
        'last_login_at',
        'current_login_at',
        'last_login_ip',
        'current_login_ip',
        'login_count',
    ]


class RoleView(ModelView, __AdminViewMixin):
    """
        Parrots the Role table model and adds a request intercept to prevent unauthorized access

    """

    # override base accessibility methods with ones from the mixin
    #
    def is_accessible(self):
        return self.base_is_accessible()


    # define the view
    #
    column_list = ['name', 'description']
    form_columns = ['name', 'description']
