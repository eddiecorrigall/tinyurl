import validators

from collections import namedtuple
from urllib.parse import urlparse


URL = namedtuple(
    typename='URL',
    field_names=[
        'scheme', 'path', 'query', 'fragment', 'username', 'password',
        'hostname', 'port'],
    defaults=(None,) * 8)


def is_url(string):
    """Return True if valid url otherwise False.

    Arguments:
    string -- The string to test.
    """
    return validators.url(string) is True


def parse_url(url):
    """Return a tuple given a string,
    first item is an URL, second item indicates parse error.

    Exceptions:
    ValueError, TypeError

    Arguments:
    url -- The url string to parse.
    """
    if not is_url(url):
        raise ValueError('Invalid url')
    url_obj = urlparse(url)
    return URL(
        scheme=url_obj.scheme or None,
        path=url_obj.path or None,
        query=url_obj.query or None,
        fragment=url_obj.fragment or None,
        username=url_obj.username or None,
        password=url_obj.password or None,
        hostname=url_obj.hostname or None,
        port=url_obj.port or None)
