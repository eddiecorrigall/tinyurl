from flask import g, current_app, redirect, render_template, request
from werkzeug.exceptions import BadRequest, NotFound


from app.tinyurl import blueprint

from app.tinyurl import common
from app.tinyurl.forms import MakeForm


@blueprint.route('/', methods=['GET', 'POST'])
def make_form():
    form = MakeForm()
    long_url = request.form.get('url')
    if form.validate_on_submit():
        return common.make_short(long_url, is_html=True)
    return render_template('tinyurl/make.html', form=form)


@blueprint.route('/tinyurl', methods=['GET'])
def get_short():
    # Sanitize user input
    long_url = request.args.get('url')
    current_app.logger.info('Request to GET shorten url {long_url}'.format(
        long_url=(long_url or 'empty')))
    common.validate_long_url(long_url)
    # Determine short id
    short_id = g.tinyurl.get_short_id(long_url)
    if short_id is None:
        raise NotFound('TinyURL does not exist')
    else:
        short_url = common.get_short_url_from_short_id(short_id)
        is_html = request.args.get('html', False)
        if is_html:
            return render_template(
                'tinyurl/get.html',
                long_url=long_url, short_id=short_id, short_url=short_url)
        else:
            return short_url, 200


@blueprint.route('/tinyurl', methods=['POST'])
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
