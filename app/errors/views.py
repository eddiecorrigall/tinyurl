from flask import current_app, jsonify
from redis.exceptions import RedisError
from werkzeug.exceptions import HTTPException

from app.errors import blueprint
from services.exceptions import ServiceException


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


@blueprint.app_errorhandler(ServiceException)
def handle_service_exception(service_exception):
    return _handle_error(
        message='Internal Server Error: Service Exception',
        status_code=500,
        exception=service_exception)


@blueprint.app_errorhandler(RedisError)
def handle_redis_error(redis_error):
    return _handle_error(
        message='Internal Server Error: Database Failure',
        status_code=500,
        exception=redis_error)


@blueprint.app_errorhandler(Exception)
def handle_generic_exception(exception):
    return _handle_error(
        message='Internal Server Error',
        status_code=500,
        exception=exception)
