# coding: utf-8
"""Contains methods to generate a random password."""

import crypt
import random
import re
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


def hash_password(password):
    """
    Hash (if not already done) a string valid for use with PAAS/IAAS password

    WARNING: Using a hash password will make impossible for the API to
             check/validate the password strength so you should check it
             before.

    :param password: The string to hash
    :type  password: ``str``

    :rtype: ``str``
    """

    # crypt SHA-512
    if re.match('^\$6\$[a-zA-Z0-9\./]{16}\$[a-zA-Z0-9\./]{86}$', password):
        return password

    salt = mkpassword(length=16,
                      chars=string.ascii_letters + string.digits + './')
    return crypt.crypt(password, '$6$%s$' % (salt, ))
