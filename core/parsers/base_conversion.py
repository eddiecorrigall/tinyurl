BASE62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def encode(number, alphabet):
    """Encode a non-negative integer number into a string using alphabet.

    Arguments:
    number -- The non-negative integer to encode into alphabet.
    alphabet -- The string of unique characters to help encode the number.
    """
    if number == 0:
        return alphabet[0]
    base = len(alphabet)
    buf = []
    while number:
        number, remainder = divmod(number, base)
        buf.append(alphabet[remainder])
    buf.reverse()
    return ''.join(buf)


def decode(string, alphabet):
    """Decode an alphabet encoded string into a non-negative integer.

    Arguments:
    string -- The encoded string.
    alphabet -- The alphabet to used to encode the string.
    """
    base = len(alphabet)
    number = 0
    char_value = dict([(x, i) for i, x in enumerate(alphabet)])
    for index, char in enumerate(string):
        power = len(string) - index - 1
        number += char_value[char] * (base ** power)
    return number
