import os

from flask import g
from redis import Redis


def get_client():
    return Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0)))


def init_app(app):

    @app.before_request
    def redis_before_request():
        if 'redis' not in g:
            g.redis = get_client()

    @app.teardown_appcontext
    def redis_teardown_appcontext(error):
        redis = g.pop('redis', None)
        if redis is not None:
            redis.connection_pool.disconnect()
