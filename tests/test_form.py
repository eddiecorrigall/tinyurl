import pytest

from flask import url_for


class TestIntegrationTinyURLForm(object):
    def test_make_form_get(self, app):
        with app.app_context():
            with app.test_client() as client:
                response = client.get(
                    url_for('tinyurl.make_form'))
                body = response.data.decode()
                assert 'name="url"' in body
                assert 'name="submit"' in body

    @pytest.mark.parametrize(
        ['long_url', 'status_code', 'is_redirected', 'body_substring'],
        [
            ('http://youtube.com', 303, True, None),
            ('http://example.com', 303, True, None),
            ('http://youtube.com', 200, False, 'URL is already a TinyURL'),
            ('localhost', 200, False, 'URL is invalid'),
        ]
    )
    def test_make_form_post(
            self, app,
            long_url, status_code, is_redirected, body_substring):
        with app.app_context():
            with app.test_client() as client:
                response = client.post(
                    url_for('tinyurl.make_form'),
                    data={'url': long_url})
                assert status_code == response.status_code
                if is_redirected:
                    location = response.headers.get('Location')
                    assert location is not None
                    assert location.endswith(
                        url_for('tinyurl.get_short', url=long_url, html=True))
                if body_substring is not None:
                    body = response.data.decode()
                    assert body_substring in body
