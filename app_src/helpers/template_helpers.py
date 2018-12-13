# getters for common blocks of template code
# copyright (c) 2018 wildduck.io


from app_src.admin.app_roles import *


def get_hamburger_menu_items_by_role(user_role_list):

    hamburger_menu_items = ""

    if ROLE_ADMIN in user_role_list:
        hamburger_menu_items = __get_admin_hamburger_menu_items()
    elif ROLE_RECRUITER in user_role_list:
        hamburger_menu_items = __get_recruiter_hamburger_menu_items()
    else:
        hamburger_menu_items = __get_talent_hamburger_menu_items()

    return hamburger_menu_items


def __get_admin_hamburger_menu_items():
    """
    allows multiple templates to pull the same menu list items from one source of truth

    Returns(str): html5 list elements for the hamburger menu

    """

    return \
        "<li><a href='/peekaboo'><span class='glyphicon glyphicon-king'></span> &nbsp; Admin</a></li>" + \
        "<li><a href='/jobs'><span class='glyphicon glyphicon-briefcase'></span> &nbsp; Jobs</a></li>" + \
        "<li><a href='/talent'><span class='glyphicon glyphicon-user'></span> &nbsp; Talent</a></li>" + \
        "<li role='separator' class='divider'></li>" + \
        "<li><a href='/logout'><span class='glyphicon glyphicon-log-out'></span> &nbsp; Logout </a></li>"


def __get_recruiter_hamburger_menu_items():
    """
    allows multiple templates to pull the same menu list items from one source of truth

    Returns(str): html5 list elements for the hamburger menu

    """

    return \
        "<li><a href='/jobs'><span class='glyphicon glyphicon-briefcase'></span> &nbsp; Jobs</a></li>" + \
        "<li><a href='/talent'><span class='glyphicon glyphicon-user'></span> &nbsp; Talent</a></li>" + \
        "<li role='separator' class='divider'></li>" + \
        "<li><a href='/logout'><span class='glyphicon glyphicon-log-out'></span> &nbsp; Logout </a></li>"


def __get_talent_hamburger_menu_items():
    """
    allows multiple templates to pull the same menu list items from one source of truth

    Returns(str): html5 list elements for the hamburger menu

    """

    return \
        "<li><a href='/'><span class='glyphicon glyphicon-home'></span> &nbsp; Home</a></li>" + \
        "<li role='separator' class='divider'></li>" + \
        "<li><a href='/logout'><span class='glyphicon glyphicon-log-out'></span> &nbsp; Logout </a></li>"


