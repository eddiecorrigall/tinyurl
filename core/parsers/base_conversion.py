BASE62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def encode(number, alphabet):
    """Encode a non-negative integer number into a string using alphabet.

    Arguments:
    number -- The non-negative integer to encode into alphabet.
    alphabet -- The string of unique characters to help encode the number.
    """
    if not isinstance(alphabet, str):
        raise TypeError('Alphabet must be of type str')
    if not len(alphabet) >= 2:
        raise ValueError('Alphabet must have at least two items')
    if not isinstance(number, int):
        raise TypeError('Number must be of type int')
    if number < 0:
        raise ValueError('Number must be non-negative')
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
    if not isinstance(alphabet, str):
        raise TypeError('Alphabet must be of type str')
    if not len(alphabet) >= 2:
        raise ValueError('Alphabet must have at least two items')
    if not isinstance(string, str):
        raise TypeError('String must be of type str')
    if len(string) == 0:
        raise ValueError('String must be non-empty')
    base = len(alphabet)
    number = 0
    char_value = dict([(x, i) for i, x in enumerate(alphabet)])
    if len(char_value) != len(alphabet):
        raise ValueError('Alphabet contains duplicate characters')
    for index, char in enumerate(string):
        power = len(string) - index - 1
        if char in char_value:
            number += char_value[char] * (base ** power)
        else:
            raise ValueError(
                'String input contains a character that is not in alphabet')
    return number
