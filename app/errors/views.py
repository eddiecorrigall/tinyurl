from flask import current_app, jsonify
from werkzeug.exceptions import HTTPException

from app.errors import blueprint


def _handle_error(message, status_code, exception=None):
    if 500 <= status_code < 600:
        current_app.logger.error(message)
        if exception:
            current_app.logger.error(exception)
    else:
        current_app.logger.info(message)
        if exception:
            current_app.logger.debug(exception)
    response = jsonify(dict(message=message))
    response.status_code = status_code
    return response


@blueprint.app_errorhandler(HTTPException)
def handle_bad_request(http_error):
    return _handle_error(
        message=http_error.description,
        status_code=http_error.code,
        exception=http_error)
