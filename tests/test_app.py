from flask import current_app


class TestFlaskApp(object):
    def test_app_configured_for_testing(self, app):
        """ Test that the application set TESTING config to True """
        with app.app_context():
            assert app.config['TESTING'] is True

    def test_app_context_is_current_app(self, app):
        """ Test that current_app is the same instance as app """
        with app.app_context():
            assert current_app.name == app.name
