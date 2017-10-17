# coding: utf8

from os import devnull
from subprocess import check_call


def has_command(command):
    return run(["which", command]) == 0


def run(command, **kwargs):
    with open(devnull, "w") as dn:
        return check_call(command, stdout=dn, **kwargs)
