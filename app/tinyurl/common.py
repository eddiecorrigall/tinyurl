from urllib.parse import urljoin

from flask import current_app, g, url_for, redirect, request
from werkzeug.exceptions import BadRequest, InternalServerError

from core.parsers import BASE62, in_alphabet, parse_url


def validate_long_url(long_url):
    # Sanitize user input
    if not long_url:
        raise BadRequest('Request url is empty or not defined')
    # Check if request is self-referencing
    try:
        url_obj = parse_url(long_url)
    except ValueError:
        raise BadRequest('Request url failed to parse')
    try:
        app_url_obj = parse_url(request.base_url)
    except ValueError:
        raise InternalServerError('Request base url failed to parse')
    if url_obj.hostname == app_url_obj.hostname:
        if url_obj.port == app_url_obj.port:
            raise BadRequest('Request url is self-referencing')


def validate_short_id(short_id):
    # Sanitize user input
    if not short_id:
        raise BadRequest('Request id is empty or not defined')
    # Check if characters are base-62
    if not in_alphabet(short_id, BASE62):
        raise BadRequest('Request id contains invalid characters')


def get_short_url_from_short_id(short_id):
    return urljoin(
        request.base_url,
        url_for('tinyurl.redirect_to_long', short_id=short_id))


def get_short_url_from_long_url(long_url):
    validate_long_url(long_url)
    short_id = g.tinyurl.get_short_id(long_url)
    if short_id is not None:
        return get_short_url_from_short_id(short_id)


def make_short(long_url, is_html=None):
    # Sanitize user input
    validate_long_url(long_url)
    # Determine the short id
    short_id = g.tinyurl.get_or_create_short_id(long_url)
    current_app.logger.info(
        'Request url {long_url} has short id {short_id}'.format(
            long_url=long_url, short_id=short_id))
    # Update entry only if necessary
    get_short_endpoint = url_for(
        'tinyurl.get_info', url=long_url, html=is_html)
    if g.tinyurl.update_long_url(short_id, long_url):
        current_app.logger.info(
            'Saved url {long_url} as shortened string {short_id}'.format(
                long_url=long_url, short_id=short_id))
        return redirect(get_short_endpoint, code=303)  # Modified: see other
    else:
        return redirect(get_short_endpoint, code=304)  # Not modified
