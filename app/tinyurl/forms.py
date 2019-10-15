import wtforms

from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL


class MakeForm(FlaskForm):
    url = StringField('Long URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Make TinyURL!')

    def validate_url(self, field):
        short_id = g.tinyurl.get_short_id(field.data)
        if short_id is not None:
            raise wtforms.ValidationError(
                'URL is already a TinyURL ({short_id}).'.format(
                    short_id=short_id))
