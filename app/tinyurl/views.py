from flask import (
    g, current_app, jsonify, redirect, render_template, request, url_for)
from werkzeug.exceptions import BadRequest, NotFound

from app.tinyurl import common, blueprint
from app.tinyurl.forms import MakeForm, SearchForm
from core.parsers import encode_url


@blueprint.route('/', methods=['GET', 'POST'])
def make_form():
    form = MakeForm()
    long_url = request.form.get('url')
    if form.validate_on_submit():
        return common.make_short(long_url, is_html=True)
    return render_template('tinyurl/make.html', form=form)


@blueprint.route('/search', methods=['GET', 'POST'])
def search_form():
    form = SearchForm()
    short_id = request.form.get('short_id') or None
    long_url = request.form.get('long_url') or None
    if form.validate_on_submit():
        get_info_endpoint = url_for(
            'tinyurl.get_info', url=long_url, id=short_id, html=True)
        return redirect(get_info_endpoint, code=303)
    return render_template('tinyurl/search.html', form=form)


@blueprint.route('/api', methods=['GET'])
def get_info():
    is_html = request.args.get('html', False)
    if 'url' in request.args and 'id' not in request.args:
        current_app.logger.debug('Found long url in request args')
        long_url = request.args.get('url')
        return _get_info_from_long_url(long_url=long_url, is_html=is_html)
    elif 'url' not in request.args and 'id' in request.args:
        short_id = request.args.get('id')
        return _get_info_from_short_id(short_id=short_id, is_html=is_html)
    else:
        raise BadRequest(
            'Only one of url or id parameters can be set in the query')


def _get_short_qr_from_short_url(short_url):
    return (
        'https://chart.googleapis.com/chart'
        '?cht=qr&chs=100x100&choe=UTF-8&chl={short_url}'.format(
            short_url=encode_url(short_url)))


def _get_info_from_long_url(long_url, is_html):
    # Sanitize user input
    current_app.logger.info('Request to GET shorten url {long_url}'.format(
        long_url=(long_url or 'empty')))
    common.validate_long_url(long_url)
    # Determine short id
    short_id = g.tinyurl.get_short_id(long_url)
    if short_id is None:
        raise NotFound('TinyURL does not exist')
    else:
        short_url = common.get_short_url_from_short_id(short_id)
        short_qr = _get_short_qr_from_short_url(short_url)
        payload = dict(
            long_url=long_url,
            short_id=short_id, short_url=short_url, short_qr=short_qr)
        if is_html:
            return render_template('tinyurl/get.html', **payload)
        else:
            return jsonify(payload), 200


def _get_info_from_short_id(short_id, is_html):
    # Sanitize user input
    current_app.logger.info('Request to GET long url from {short_id}'.format(
        short_id=(short_id or 'empty')))
    common.validate_short_id(short_id)
    # Determine long url
    long_url = g.tinyurl.get_long_url(short_id)
    if long_url is None:
        raise NotFound('TinyURL does not exist')
    else:
        short_url = common.get_short_url_from_short_id(short_id)
        short_qr = _get_short_qr_from_short_url(short_url)
        payload = dict(
            long_url=long_url,
            short_id=short_id, short_url=short_url, short_qr=short_qr)
        if is_html:
            return render_template('tinyurl/get.html', **payload)
        else:
            return jsonify(payload), 200


@blueprint.route('/api', methods=['POST'])
def make_short():
    # Sanitize user input
    if not request.is_json:
        raise BadRequest('Request body is not json')
    body = request.get_json()
    long_url = body.get('url')
    # ...
    return common.make_short(long_url=long_url)


@blueprint.route('/<string:short_id>', methods=['GET'])
def redirect_to_long(short_id):
    # Sanitize user input
    current_app.logger.info(
        'Request to redirect using short id {short_id}'.format(
            short_id=short_id))
    long_url = g.tinyurl.get_long_url(short_id)
    if long_url is None:
        raise NotFound('TinyURL does not exist')
    else:
        # TODO:
        # - show an advertisement
        # - track usage
        return redirect(long_url, code=302)
