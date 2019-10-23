import os

from flask import g
from redis import Redis
from fakeredis import FakeRedis

from core.logger import root_logger as logger

_CLIENT = None


def _get_client():
    global _CLIENT
    if _CLIENT is None:
        redis_configs = dict(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            # Only socket.connect
            socket_connect_timeout=1.0,
            # Both socket.send/socket.recv and socket.connect
            socket_timeout=5.0)
        logger.info(
            'Creating new Redis() instance for host {host}, '
            'port {port} and db {db}'.format(**redis_configs))
        _CLIENT = Redis(**redis_configs)
    return _CLIENT


_TEST_CLIENT = None


def _get_test_client():
    global _TEST_CLIENT
    if _TEST_CLIENT is None:
        logger.info('Creating new FakeRedis() instance')
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
