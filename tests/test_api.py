import pytest

from flask import current_app, url_for


class TestFlaskApp(object):
    def test_app_configured_for_testing(self, app):
        """ Test that the application set TESTING config to True """
        with app.app_context():
            assert app.config['TESTING']

    def test_app_context_is_current_app(self, app):
        """ Test that current_app is the same instance as app """
        with app.app_context():
            assert current_app.name == app.name


class TestIntegration_TinyURL(object):
    @pytest.mark.parametrize(
        ['long_url', 'status_code'],
        [
            ('https://en.wikipedia.org/wiki/TinyURL', 303),
            ('https://www.google.ca/maps', 303),
            ('https://en.wikipedia.org/wiki/TinyURL', 304),
        ]
    )
    def test_make_short(
            self, app,
            long_url, status_code):
        with app.app_context():
            with app.test_client() as client:
                response = client.post(
                    url_for('tinyurl.make_short'),
                    headers={'Content-Type': 'application/json'},
                    json={'url': long_url},
                    follow_redirects=False)
                assert response.status_code == status_code
                location = response.headers.get('Location')
                assert location is not None
                assert location.endswith(url_for(
                    'tinyurl.get_short', url=long_url))

    @pytest.mark.parametrize(
        ['long_url', 'status_code'],
        [
            ('https://en.wikipedia.org/wiki/TinyURL', 200),
            ('https://www.google.ca/maps', 200),
            ('http://example.com', 404),
        ]
    )
    def test_get_short(
            self, app,
            long_url, status_code):
        with app.app_context():
            with app.test_client() as client:
                response = client.get(
                    url_for('tinyurl.get_short', url=long_url))
                assert response.status_code == status_code

    @pytest.mark.parametrize(
        ['long_url', 'short_id', 'status_code'],
        [
            ('https://en.wikipedia.org/wiki/TinyURL', 'a', 302),
            ('https://www.google.ca/maps', 'b', 302),
            (None, 'c', 404),
        ]
    )
    def test_redirect_to_long(
            self, app,
            long_url, short_id, status_code):
        with app.app_context():
            with app.test_client() as client:
                response = client.get(
                    url_for('tinyurl.redirect_to_long', short_id=short_id))
                assert response.status_code == status_code
                location = response.headers.get('Location')
                if long_url is not None:
                    assert location is not None
                    assert location == long_url
