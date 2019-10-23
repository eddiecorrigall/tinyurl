import random

from time import sleep


def sleep_jitter(min_milliseconds, max_milliseconds):
    """
    Sleep/block for a random amount of time given a millisecond integer range.

    Arguments:
    min_milliseconds -- non-negative, inclusive lower-bound
    max_milliseconds -- non-negative, exclusive upper-bound
    """
    jitter_milliseconds = random.randrange(min_milliseconds, max_milliseconds)
    sleep(jitter_milliseconds / 1000.0)
