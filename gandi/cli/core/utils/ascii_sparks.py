# coding: utf-8

parts = u' ▁▂▃▄▅▆▇▉'

def sparks(nums):
    fraction = max(nums) / float(len(parts) - 1)
    return ''.join(parts[int(round(x/fraction))] for x in nums)
