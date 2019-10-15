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
    try:
        validators.url(string)
        return True
    except validators.ValidationFailure:
        return False


def parse_url(url):
    """Return a tuple given a string,
    first item is an URL, second item indicates parse error.

    Arguments:
    url -- The url string to parse.
    """
    try:
        url_obj = urlparse(url)
        return URL(
            scheme=url_obj.scheme,
            path=url_obj.path,
            query=url_obj.query,
            fragment=url_obj.fragment,
            username=url_obj.username,
            password=url_obj.password,
            hostname=url_obj.hostname,
            port=url_obj.port), False
    except ValueError:
        pass
    return URL(), True
