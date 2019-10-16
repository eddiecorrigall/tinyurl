from flask import g, current_app, redirect, render_template, request, url_for
from werkzeug.exceptions import BadRequest, NotFound

from core.parsers import is_url, parse_url


from app.tinyurl import blueprint
from app.tinyurl.forms import MakeForm


@blueprint.route('/', methods=['GET', 'POST'])
def make_form():
    form = MakeForm()
    if form.validate_on_submit():
        long_url = request.form.get('url')
        return _make_short(long_url)
    return render_template('tinyurl/make.html', form=form)


def validate_long_url(long_url):
    # Sanitize user input
    if not long_url:
        raise BadRequest('Request url is empty or not defined')
    if not is_url(long_url):
        raise BadRequest('Request url is invalid')
    # Check if request is self-referencing
    url_obj, _ = parse_url(long_url)
    app_url_obj, _ = parse_url(request.base_url)
    if url_obj.hostname == app_url_obj.hostname:
        if url_obj.port == app_url_obj.port:
            raise BadRequest('Request url is self-referencing')


@blueprint.route('/tinyurl', methods=['GET'])
def get_short():
    # Sanitize user input
    long_url = request.args.get('url')
    current_app.logger.info('Request to GET shorten url {long_url}'.format(
        long_url=(long_url or 'empty')))
    validate_long_url(long_url)
    # Determine short id
    short_id = g.tinyurl.get_short_id(long_url)
    if short_id is None:
        raise NotFound('TinyURL does not exist')
    else:
        return short_id, 200


def _make_short(long_url):
    # Sanitize user input
    validate_long_url(long_url)
    # Determine the short id
    short_id = g.tinyurl.get_or_create_short_id(long_url)
    current_app.logger.info(
        'Request url {long_url} has short id {short_id}'.format(
            long_url=long_url, short_id=short_id))
    # Update entry only if necessary
    get_short_url = url_for('tinyurl.get_short', url=long_url)
    if g.tinyurl.update_long_url(short_id, long_url):
        current_app.logger.info(
            'Saved url {long_url} as shortened string {short_id}'.format(
                long_url=long_url, short_id=short_id))
        return redirect(get_short_url, code=303)  # See other
    else:
        return redirect(get_short_url, code=304)  # Not modified


@blueprint.route('/tinyurl', methods=['POST'])
def make_short():
    # Sanitize user input
    if not request.is_json:
        raise BadRequest('Request body is not json')
    body = request.get_json()
    long_url = body.get('url')
    # ...
    return _make_short(long_url)


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
