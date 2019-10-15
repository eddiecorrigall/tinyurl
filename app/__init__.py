import os

from flask import Flask, g
from flask.logging import default_handler

from app import redis
from services.tinyurl import TinyURLServiceRedis


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'superman-batman')

    redis.init_app(app)

    @app.before_request
    def before_request():
        if 'tinyurl' not in g:
            g.tinyurl = TinyURLServiceRedis(
                logging_handler=default_handler,
                get_redis_client=redis.get_client)

    from app.errors import blueprint as errors_blueprint
    app.register_blueprint(errors_blueprint)

    from app.tinyurl import blueprint as tinyurl_blueprint
    app.register_blueprint(tinyurl_blueprint)

    return app
