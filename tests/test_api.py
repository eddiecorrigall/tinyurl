import pytest

from flask import url_for


class TestIntegrationTinyURLAPI(object):
    @pytest.mark.parametrize(
        ['long_url', 'status_code', 'is_redirected', 'body_substring'],
        [
            ('https://en.wikipedia.org/wiki/TinyURL', 303, True, None),
            ('https://www.google.ca/maps', 303, True, None),
            ('https://en.wikipedia.org/wiki/TinyURL', 304, True, None),
            ('', 400, False, 'Request url is empty or not defined'),
            ('invalid url', 400, False, 'Request url failed to parse'),
            ('http://localhost.localdomain:5000', 400, False,
                'Request url is self-referencing'),
        ]
    )
    def test_make_short(
            self, app,
            long_url, status_code, is_redirected, body_substring):
        with app.app_context():
            with app.test_client() as client:
                response = client.post(
                    url_for('tinyurl.make_short'),
                    headers={'Content-Type': 'application/json'},
                    json={'url': long_url},
                    follow_redirects=False)
                assert response.status_code == status_code
                if is_redirected:
                    location = response.headers.get('Location')
                    assert location is not None
                    assert location.endswith(url_for(
                        'tinyurl.get_short', url=long_url))
                if body_substring is not None:
                    body = response.data.decode()
                    assert body_substring in body

    def test_make_short_with_invalid_content_type(self, app):
        with app.app_context():
            with app.test_client() as client:
                response = client.post(
                    url_for('tinyurl.make_short'),
                    headers={'Content-Type': 'application/xml'},
                    json={'url': 'http://google.ca'},
                    follow_redirects=False)
                body = response.data.decode()
                assert 'Request body is not json' in body

    def test_make_short_with_invalid_json(self, app):
        with app.app_context():
            with app.test_client() as client:
                response = client.post(
                    url_for('tinyurl.make_short'),
                    headers={'Content-Type': 'application/json'},
                    data={'url': 'http://google.com'},
                    follow_redirects=False)
                body = response.data.decode()
                assert 'Failed to decode JSON object' in body

    @pytest.mark.parametrize(
        ['long_url', 'status_code'],
        [
            ('https://en.wikipedia.org/wiki/TinyURL', 200),
            ('https://www.google.ca/maps', 200),
            ('http://example.com', 404),
            ('', 400),
            ('invalid url', 400),
            ('http://localhost.localdomain:5000', 400),
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
        [
            'long_url', 'short_id', 'status_code', 'is_redirected',
            'body_substring'
        ], [
            ('https://en.wikipedia.org/wiki/TinyURL', 'a', 302, True, None),
            ('https://www.google.ca/maps', 'b', 302, True, None),
            (None, 'c', 404, False, 'TinyURL does not exist'),
        ]
    )
    def test_redirect_to_long(
            self, app,
            long_url, short_id, status_code, is_redirected, body_substring):
        with app.app_context():
            with app.test_client() as client:
                response = client.get(
                    url_for('tinyurl.redirect_to_long', short_id=short_id))
                assert response.status_code == status_code
                if is_redirected:
                    location = response.headers.get('Location')
                    assert location is not None
                    assert location == long_url
                if body_substring is not None:
                    body = response.data.decode()
                    assert body_substring in body
