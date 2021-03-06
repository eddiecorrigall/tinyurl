import os

from flask import Flask
from flask_bootstrap import Bootstrap

import core.logger
import core.redis
import core.tinyurl


def create_app(testing=False):
    app = Flask(__name__)
    app.config['TESTING'] = testing
    app.config['SECRET_KEY'] = os.environ['TINYURL_SECRET_KEY']

    core.logger.init_app(app)
    core.redis.init_app(app)
    core.tinyurl.init_app(app)

    Bootstrap(app)

    from app.errors import blueprint as errors_blueprint
    app.register_blueprint(errors_blueprint)

    from app.tinyurl import blueprint as tinyurl_blueprint
    app.register_blueprint(tinyurl_blueprint)

    return app
