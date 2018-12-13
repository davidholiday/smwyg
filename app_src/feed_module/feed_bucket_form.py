# form definition for the content feed slide bucket modal
# copyright (c) 2018 wildduck.io


from flask_wtf import FlaskForm


class FeedBucketForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(FeedBucketForm, self).__init__()
