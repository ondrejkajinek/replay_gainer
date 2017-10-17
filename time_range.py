# coding: utf8


class TimeRange(object):

    def __init__(self, lower, upper):
        self._lower = lower
        self._upper = upper

    def __contains__(self, item):
        return item > self._lower and item <= self._upper
