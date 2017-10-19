# coding: utf8

from sys import stdout, stderr


ENDC = "\033[0m"
FAIL = "\033[91m"
INFO = "\033[34m"


def error(message, *args):
    stderr.write(_single_line("%s%s%s\n" % (FAIL, message % args, ENDC)))


def info(message, *args):
    stdout.write(_single_line("%s%s%s\n" % (INFO, message % args, ENDC)))


def _single_line(text):
    return text.rstrip("\n") + "\n"
