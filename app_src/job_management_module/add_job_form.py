# form definition for the add job modal
# copyright (c) 2018 wildduck.io


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import SelectField

from app_src.offering_attributes.models import OfferingRole, OfferingLevel, OfferingLocation


class AddJobForm(FlaskForm):

    job_level_list = SelectField(u'Level', coerce=int)
    job_role_list = SelectField(u'Role', coerce=int)
    job_location_list = SelectField(u'Location', coerce=int)

    job_rec = FileField('Job Rec', validators=[
        FileRequired(),
        FileAllowed(['docx'], 'Word docs only please!')
    ])

    # to ensure SelectFields gets populated when object is constructed. after init -- remember the db is always source
    # of truth to the app (source of truth to the db are the constants objects)
    #
    # t/y SO --v
    # https://stackoverflow.com/a/753657
    # https://stackoverflow.com/a/25663409
    def __init__(self, *args, **kwargs):

        super(AddJobForm, self).__init__()

        self.job_level_list.choices = [(obj.id, obj.name) for obj in OfferingLevel.query.order_by('name')]
        self.job_role_list.choices = [(obj.id, obj.name) for obj in OfferingRole.query.order_by('name')]
        self.job_location_list.choices = [(obj.id, obj.name) for obj in OfferingLocation.query.order_by('name')]

