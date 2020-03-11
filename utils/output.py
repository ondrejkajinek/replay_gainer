# coding: utf8

import sys


ENDC = "\033[0m"
FAIL = "\033[91m"
INFO = "\033[34m"


def error(message, *args):
    """prints error message to stderr, in red color"""
    sys.stderr.write(_single_line("%s%s%s\n" % (FAIL, message % args, ENDC)))


def info(message, *args):
    """prints info message to stdout, in blue color"""
    sys.stdout.write(_single_line("%s%s%s\n" % (INFO, message % args, ENDC)))


def _single_line(text):
    return text.rstrip("\n") + "\n"
