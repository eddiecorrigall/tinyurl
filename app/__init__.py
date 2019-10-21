import os

from flask import Flask

from app import tinyurl
from core import logger, redis


def create_app(testing=False):
    app = Flask(__name__)
    app.config['TESTING'] = testing
    app.config['SECRET_KEY'] = (
        os.getenv('SECRET_KEY', 'superman'))
    app.config['WTF_CSRF_SECRET_KEY'] = (
        os.getenv('WTF_CSRF_SECRET_KEY', 'batman'))

    logger.init_app(app)
    redis.init_app(app)
    tinyurl.init_app(app)

    from app.errors import blueprint as errors_blueprint
    app.register_blueprint(errors_blueprint)

    from app.tinyurl import blueprint as tinyurl_blueprint
    app.register_blueprint(tinyurl_blueprint)

    return app
