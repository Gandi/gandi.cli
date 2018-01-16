# coding: utf-8
"""Contains methods to generate a random password."""

import random
import string

# remove backslash from generated password to avoid
# general escape issues while transmitting it
PUNCTUATION = string.punctuation.replace(chr(0x5c), '')


def mkpassword(length=16, chars=None, punctuation=None):
    """Generates a random ascii string - useful to generate authinfos

    :param length: string wanted length
    :type length: ``int``

    :param chars: character population,
                  defaults to alphabet (lower & upper) + numbers
    :type chars: ``str``, ``list``, ``set`` (sequence)

    :param punctuation: number of punctuation signs to include in string
    :type punctuation: ``int``

    :rtype: ``str``
    """
    if chars is None:
        chars = string.ascii_letters + string.digits

    # Generate string from population
    data = [random.choice(chars) for _ in range(length)]

    # If punctuation:
    # - remove n chars from string
    # - add random punctuation
    # - shuffle chars :)
    if punctuation:
        data = data[:-punctuation]

        for _ in range(punctuation):
            data.append(random.choice(PUNCTUATION))
        random.shuffle(data)

    return ''.join(data)
