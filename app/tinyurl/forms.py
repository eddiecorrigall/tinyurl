import wtforms

from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from app.tinyurl import common
from core.parsers import is_url


class MakeForm(FlaskForm):
    url = StringField('Long URL', validators=[DataRequired()])
    submit = SubmitField('Make TinyURL!')

    def validate_url(self, field):
        long_url = field.data
        if not is_url(long_url):
            raise wtforms.ValidationError('URL is invalid')
        short_id = g.tinyurl.get_short_id(long_url=long_url)
        if short_id is not None:
            short_url = common.get_short_url_from_short_id(short_id=short_id)
            raise wtforms.ValidationError(
                'URL is already a TinyURL ({short_url}).'.format(
                    short_url=short_url))
