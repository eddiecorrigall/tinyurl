import urllib.parse
import validators

from collections import namedtuple

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
    url_obj = urllib.parse.urlparse(url)
    return URL(
        scheme=url_obj.scheme or None,
        path=url_obj.path or None,
        query=url_obj.query or None,
        fragment=url_obj.fragment or None,
        username=url_obj.username or None,
        password=url_obj.password or None,
        hostname=url_obj.hostname or None,
        port=url_obj.port or None)


def url_encode(string):
    """Retrun a string that is url encoded.

    Arguments:
    string -- Thes string to url encode.
    """
    return urllib.parse.quote(string, safe='')


def qr_encode(string):
    """Return an image url to the encoded string.

    Arguments:
    string -- The string encoded in the QR code.
    """
    return (
        'https://chart.googleapis.com/chart'
        '?cht=qr'
        '&choe=UTF-8'
        '&chs={width}x{height}'
        '&chl={string_encoded}').format(
            width=101, height=101, string_encoded=url_encode(string))
