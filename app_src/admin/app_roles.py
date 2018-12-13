# flask app user roles
# copyright (c) 2018 wildduck.io


ROLE_ADMIN = "ADMIN"
ROLE_ADMIN_DESCRIPTION = "role that has full access to the app"

ROLE_RECRUITER = "RECRUITER"
ROLE_RECRUITER_DESCRIPTION = "recruiters can create feeds, add talent users"

ROLE_TALENT = "TALENT"
ROLE_TALENT_DESCRIPTION = "talent can consume feeds"


def get_app_role_tuples():
    """

    Returns((str, str)): ((ROLE NAME, ROLE DESCRIPTION), (...), ...)

    """
    return (
        (ROLE_ADMIN, ROLE_ADMIN_DESCRIPTION),
        (ROLE_RECRUITER, ROLE_RECRUITER_DESCRIPTION),
        (ROLE_TALENT, ROLE_TALENT_DESCRIPTION)
    )


def get_app_role_names():
    """

    Returns(str): (ROLE NAME, ...)

    """
    return (
        ROLE_ADMIN,
        ROLE_RECRUITER,
        ROLE_TALENT
    )
