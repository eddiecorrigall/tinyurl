import pytest

from core.parsers import BASE62, encode, decode
from core.parsers import URL, is_url, in_alphabet, parse_url


class TestParsersBaseConversion(object):
    @pytest.mark.parametrize(
        ['alphabet', 'number', 'result', 'raises_exception'],
        [
            (666, 0, 'alphabet must be of type str', TypeError),
            ('', 0, 'alphabet must have at least 2 characters', ValueError),
            ('1', 0, 'alphabet must have at least 2 characters', ValueError),
            ('01', '2', 'number must be of type int', TypeError),
            ('01', 2, '10', None),
            ('01', 5, '101', None),
            (BASE62, 0, 'a', None),
            (BASE62, 125, 'cb', None),
            (BASE62, 1763, 'CB', None),
            (BASE62, 2572058570175124615, 'deadBEEF123', None),
            (BASE62, -1, 'number must be a non-negative integer', ValueError),
        ]
    )
    def test_encode(self, alphabet, number, result, raises_exception):
        def test():
            assert encode(number, alphabet) == result

        if raises_exception:
            with pytest.raises(raises_exception):
                test()
        else:
            test()

    @pytest.mark.parametrize(
        ['alphabet', 'string', 'result', 'raises_exception'],
        [
            (666, '1', 'alphabet must be of type str', TypeError),
            ('', '1', 'alphabet must have at least 2 characters', ValueError),
            ('1', '1', 'alphabet must have at least 2 characters', ValueError),
            ('01', '', 'string must have at least 1 character', ValueError),
            ('01', 10, 'string must be of type str', TypeError),
            ('101', '10', 'alphabet has duplicate characters', ValueError),
            ('01', '-10', 'string has character not in alphabet', ValueError),
            ('01', '10', 2, None),
            ('01', '101', 5, None),
            (BASE62, 'a', 0, None),
            (BASE62, 'cb', 125, None),
            (BASE62, 'CB', 1763, None),
            (BASE62, 'deadBEEF123', 2572058570175124615, None),
        ]
    )
    def test_decode(self, alphabet, string, result, raises_exception):
        def test():
            assert decode(string, alphabet) == result

        if raises_exception:
            with pytest.raises(raises_exception):
                test()
        else:
            test()

    @pytest.mark.parametrize(
        ['alphabet', 'string', 'result', 'raises_exception'],
        [
            (666, '1', 'invalid alphabet', TypeError),
            (['a', 'b', 'c'], 'a', True, None),
            ('abc', 'a', True, None),
            ('abc', 'aa', True, None),
            ('abc', 'abbc', True, None),
            ('abc', '1', False, None),
            ('abc', '', True, None),
            ('abc', 'abcd', False, None),
        ]
    )
    def test_in_alphabet(self, alphabet, string, result, raises_exception):
        def test():
            assert in_alphabet(string, alphabet) == result

        if raises_exception:
            with pytest.raises(raises_exception):
                test()
        else:
            test()


class TestParsersUrl(object):
    @pytest.mark.parametrize(
        ['url', 'result', 'raises_exception'],
        [
            (None, 'url must be of type str', TypeError),
            ('localhost', False, None),
            ('http://localhost', True, None),
            ('ftp://foobar.dk', True, None),
            ('ftp://myuser:@foobar.dk', True, None),
            ('http://foobar.d', False, None),
            ('http://127.0.0.1', True, None),
            ('http://10.0.0.1', True, None),
            ('https://www.youtube.com/watch?v=dQw4w9WgXcQ', True, None),
            ('jdbc:mydialect://mypostgres:9999/mypath', False, None),
        ]
    )
    def test_is_url(self, url, result, raises_exception):
        def test():
            assert is_url(url) == result

        if raises_exception:
            with pytest.raises(raises_exception):
                test()
        else:
            test()

    @pytest.mark.parametrize(
        ['url', 'result', 'raises_exception'],
        [
            # (None, 'url must be of type str', TypeError),
            ('localhost', 'invalid url', ValueError),
            ('http://localhost', URL(
                scheme='http', hostname='localhost'), None),
            ('ftp://foobar.dk', URL(
                scheme='ftp', hostname='foobar.dk'), None),
            ('ftp://myuser:mypassword@foobar.dk', URL(
                scheme='ftp', username='myuser', password='mypassword',
                hostname='foobar.dk'), None),
            ('http://foobar.d', 'invalid url', ValueError),
            ('http://127.0.0.1', URL(
                scheme='http', hostname='127.0.0.1'), None),
            ('http://10.0.0.1', URL(
                scheme='http', hostname='10.0.0.1'), None),
            ('https://www.youtube.com/watch?v=dQw4w9WgXcQ', URL(
                scheme='https', hostname='www.youtube.com', path='/watch',
                query='v=dQw4w9WgXcQ'), None),
            ('jdbc:mydialect://mypostgres:9999/mypath', 'invalid url',
                ValueError),
            ('https://en.wikipedia.org/wiki/TinyURL#Similar_services', URL(
                scheme='https', hostname='en.wikipedia.org',
                path='/wiki/TinyURL', fragment='Similar_services'), None)
        ]
    )
    def test_parse_url(self, url, result, raises_exception):
        def test():
            assert parse_url(url) == result

        if raises_exception:
            with pytest.raises(raises_exception):
                test()
        else:
            test()
