import redis
import logging

from abc import ABC, abstractmethod

from core.common import sleep_jitter
from core.parsers import BASE62, encode
from services.exceptions import ServiceException


class TinyURLServiceException(ServiceException):
    def __init__(self, *args, **kwargs):
        super.__init__('TinyURL Service Exception', *args, **kwargs)


class TinyURLService(ABC):
    @abstractmethod
    def get_short_id(self, long_url):
        """Get a short id associated with the long url.

        Returns the short id associated with the long url, or None.

        Arguments:
        long_url -- A str value used to lookup the short id.
        """
        pass

    @abstractmethod
    def get_or_create_short_id(self, long_url):
        """Get or create a short id given a long url.

        Return a short id str that has historically been associated with the
        long url, or create a new mapping to the long url and return the new
        short id.

        Arguments:
        long_url -- A str value to be, or already associated with a short id.
        """
        pass

    @abstractmethod
    def get_long_url(self, short_id):
        """Get long url given a short id.

        Return a long url str associated with the short id, otherwise None.

        Arguments:
        short_id -- A str value used to lookup long_url.
        """
        pass

    @abstractmethod
    def update_long_url(self, short_id, long_url):
        """Update the long url associatd with the short id.

        Return True if the persistence layer was modified, otherwise False.

        Arguments:
        short_id -- A str value used to lookup long_url
        long_url -- A str value used to redirect given short_id
        """
        pass


class TinyURLServiceRedis(TinyURLService):

    REDIS_MAX_ATTEMPTS = 100
    REDIS_NAME_PREFIX = 'tinyurl'
    REDIS_NAME_SHORT = '{prefix}:short'.format(prefix=REDIS_NAME_PREFIX)
    REDIS_NAME_LONG = '{prefix}:long'.format(prefix=REDIS_NAME_PREFIX)

    def __init__(self, logging_handler, get_redis_client):
        self.logger = logging.getLogger()
        self.logger.addHandler(logging_handler)
        self.get_redis_client = get_redis_client

    def get_short_id(self, long_url):
        current_short_id = self.get_redis_client().hget(
            name=self.REDIS_NAME_SHORT, key=long_url)
        if current_short_id is not None:
            return current_short_id.decode()  # Return as str

    def get_or_create_short_id(self, long_url):
        """Given a long url, assign and return a non-negative integer encoded
        in base 62 as str value.

        This is an example of a Bijective function.

        Returns a short id str, or raises a TinyURLServiceException.

        Arguments:
        long_url -- A str value to translate into a short id.
        """
        with self.get_redis_client().pipeline() as pipe:
            for attempt in range(1, self.REDIS_MAX_ATTEMPTS + 1):
                self.logger.info(
                    'Attempt {attempt} to get or create id from {url}'.format(
                        attempt=attempt, url=long_url))
                try:
                    # Return if exists
                    current_id = self.get_short_id(long_url)
                    if current_id is not None:
                        return current_id
                    # WATCH on the key that holds sequence number.
                    pipe.watch(self.REDIS_NAME_SHORT)
                    # The pipeline is now in immediate execution mode until
                    # commands are buffered again.
                    # Determine the next id.
                    length = pipe.hlen(name=self.REDIS_NAME_SHORT)
                    next_id = encode(length, BASE62)
                    # With MULTI, the pipeline is now in buffered mode.
                    pipe.multi()
                    # If key exists do nothing,
                    # otherwise assign value to next id.
                    pipe.hsetnx(
                        name=self.REDIS_NAME_SHORT,
                        key=long_url, value=next_id)
                    pipe.execute()
                except redis.exceptions.WatchError:
                    self.logger.info(
                        'An asynchronous event modified the watched name '
                        '{name} before it could be modified.'.format(
                            name=self.REDIS_NAME_SHORT))
                    # Add jitter for each loop to spread out async attempts
                    sleep_jitter(5, 50)
        raise TinyURLServiceException('Failed to get or create id for long')

    def get_long_url(self, short_id):
        long_url = self.get_redis_client().hget(
            name=self.REDIS_NAME_LONG, key=short_id)
        if long_url is not None:
            return long_url.decode()  # Return as str

    def update_long_url(self, short_id, long_url):
        if self.get_redis_client().hsetnx(
                name=self.REDIS_NAME_LONG, key=short_id, value=long_url):
            return True  # Modified
        else:
            return False  # Not modified
