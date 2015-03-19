# coding: utf-8

# Author: Rory McCann
# https://pypi.python.org/pypi/ascii_sparks/0.0.3
# License: Unknown

parts = u' ▁▂▃▄▅▆▇▉'


def sparks(nums):
    fraction = max(nums) / float(len(parts) - 1)
    return ''.join([parts[int(round(x / fraction))] for x in nums])
