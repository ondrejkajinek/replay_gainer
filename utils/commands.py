# coding: utf8

from os import devnull
from subprocess import check_call
from subprocess import CalledProcessError


def has_command(command):
    try:
        _run(["which", command])
        has = True
    except CalledProcessError:
        has = False

    return has


def shell_run(command):
    return _run(command, shell=True)


def _run(command, **kwargs):
    with open(devnull, "w") as dn:
        return check_call(command, stdout=dn, **kwargs)
