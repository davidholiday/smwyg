# form definition for the content feed slide notes modal
# copyright (c) 2018 wildduck.io


from flask_wtf import FlaskForm


class FeedNotesForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(FeedNotesForm, self).__init__()
