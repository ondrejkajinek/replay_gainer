# coding: utf8

from sys import stdout, stderr


def error(message, *args):
    stderr.write(_single_line(message) % args)


def info(message, *args):
    stdout.write(_single_line(message) % args)


def _single_line(text):
    return text.rstrip("\n") + "\n"
