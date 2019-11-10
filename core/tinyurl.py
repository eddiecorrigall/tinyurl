from flask import g
from flask.logging import default_handler

from core import redis
from core.logger import root_logger as logger
from services.tinyurl import TinyURLServiceRedis


_SERVICE = None


def _get_service():
    global _SERVICE
    if _SERVICE is None:
        logger.info('Creating TinyURLServiceRedis() instance')
        _SERVICE = TinyURLServiceRedis(
            logging_handler=default_handler,
            get_redis_client=redis.get_instance(testing=False))
    return _SERVICE


_TEST_SERVICE = None


def _get_test_service():
    global _TEST_SERVICE
    if _TEST_SERVICE is None:
        logger.info('Creating TinyURLServiceRedis() test instance')
        _TEST_SERVICE = TinyURLServiceRedis(
            logging_handler=default_handler,
            get_redis_client=redis.get_instance(testing=True))
    return _TEST_SERVICE


def get_instance(testing):
    if testing:
        return _get_test_service
    else:
        return _get_service


def init_app(app):
    testing = app.config['TESTING']

    @app.before_request
    def tinyurl_before_request():
        if 'tinyurl' not in g:
            g.tinyurl = get_instance(testing)()

    @app.teardown_appcontext
    def redis_teardown_appcontext(error):
        g.pop('tinyurl', None)
