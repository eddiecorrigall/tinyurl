import wtforms

from flask import g, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from app.tinyurl import common
from core.parsers import BASE62, in_alphabet, is_url


class MakeForm(FlaskForm):
    url = StringField('Long URL', validators=[DataRequired()])
    submit = SubmitField('Make!')

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


class SearchForm(FlaskForm):
    long_url = StringField('Long URL')
    short_id = StringField('OR, Short ID')
    submit = SubmitField('Search!')

    def validate_long_url(self, field):
        long_url = field.data
        if long_url is None or len(long_url) == 0:
            current_app.logger.debug('Long url is None or empty')
            return
        current_app.logger.debug(
            'Long url: {long_url}'.format(long_url=long_url))
        if not is_url(long_url):
            raise wtforms.ValidationError('Long URL is invalid')
        short_id = g.tinyurl.get_short_id(long_url=long_url)
        if short_id is None:
            raise wtforms.ValidationError(
                'TinyURL does not yet exist for this Long URL')

    def validate_short_id(self, field):
        short_id = field.data
        if short_id is None or len(short_id) == 0:
            current_app.logger.debug('Short id is None or empty')
            return
        current_app.logger.debug(
            'Short id: {short_id}'.format(short_id=short_id))
        if not in_alphabet(short_id, BASE62):
            raise wtforms.ValidationError('Short ID is invalid')
        long_url = g.tinyurl.get_long_url(short_id)
        if long_url is None:
            raise wtforms.ValidationError(
                'TinyURL does not yet exist for this Short ID')
