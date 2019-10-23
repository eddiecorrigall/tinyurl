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
                        url_for('tinyurl.get_info', url=long_url, html=True))
                if body_substring is not None:
                    body = response.data.decode()
                    assert body_substring in body

    def test_search_form_get(self, app):
        with app.app_context():
            with app.test_client() as client:
                response = client.get(
                    url_for('tinyurl.search_form'))
                body = response.data.decode()
                assert 'name="long_url"' in body
                assert 'name="short_id"' in body
                assert 'name="submit"' in body

    @pytest.mark.parametrize(
        [
            'long_url', 'status_code', 'is_redirected',
            'body_substring'
        ], [
            ('http://youtube.com', 303, True, None),
            ('http://not-a-long-url.com', 200, False,
                'TinyURL does not yet exist for this Long URL'),
            ('invalid url', 200, False, 'Long URL is invalid'),
        ]
    )
    def test_search_form_post_long_url(
            self, app,
            long_url, status_code, is_redirected, body_substring):
        with app.app_context():
            with app.test_client() as client:
                response = client.post(
                    url_for('tinyurl.search_form'),
                    data={'long_url': long_url})
                assert status_code == response.status_code
                if is_redirected:
                    location = response.headers.get('Location')
                    assert location is not None
                    assert location.endswith(url_for(
                        'tinyurl.get_info', url=long_url, html=True))
                if body_substring is not None:
                    body = response.data.decode()
                    assert body_substring in body

    @pytest.mark.parametrize(
        ['short_id', 'status_code', 'is_redirected', 'body_substring'],
        [
            ('a', 303, True, None),
            ('xyz', 200, False,
                'TinyURL does not yet exist for this Short ID'),
            ('Qwerty!@#', 200, False, 'Short ID is invalid'),
        ]
    )
    def test_search_form_post_short_id(
            self, app,
            short_id, status_code, is_redirected, body_substring):
        with app.app_context():
            with app.test_client() as client:
                response = client.post(
                    url_for('tinyurl.search_form'),
                    data={'short_id': short_id})
                assert status_code == response.status_code
                if is_redirected:
                    location = response.headers.get('Location')
                    assert location is not None
                    assert location.endswith(url_for(
                        'tinyurl.get_info', id=short_id, html=True))
                if body_substring is not None:
                    body = response.data.decode()
                    assert body_substring in body
