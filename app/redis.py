import os

from flask import g
from redis import Redis

from fakeredis import FakeRedis

_CLIENT = None


def _get_client():
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)))
    return _CLIENT


_TEST_CLIENT = None


def _get_test_client():
    global _TEST_CLIENT
    if _TEST_CLIENT is None:
        _TEST_CLIENT = FakeRedis()
    return _TEST_CLIENT


def get_instance(testing):
    if testing:
        return _get_test_client
    else:
        return _get_client


def init_app(app):

    testing = app.config['TESTING']

    @app.before_request
    def redis_before_request():
        if 'redis' not in g:
            g.redis = get_instance(testing)()

    @app.teardown_appcontext
    def redis_teardown_appcontext(error):
        redis = g.pop('redis', None)
        if redis is not None:
            redis.connection_pool.disconnect()
