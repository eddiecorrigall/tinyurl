import pytest

from app import create_app


@pytest.fixture(scope='class')
def app():
    app = create_app(testing=True)
    app.config['SERVER_NAME'] = 'localhost.localdomain:5000'
    app.config['WTF_CSRF_ENABLED'] = False
    return app
