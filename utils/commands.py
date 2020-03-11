# coding: utf8

import os
from subprocess import check_call, check_output
from subprocess import CalledProcessError


def has_command(command):
    """
    Checks if specified command exists in current environment

    'which' command is used for this purpose
    """
    try:
        with open(os.devnull, "w") as dev_null:
            check_call(("which", command), stdout=dev_null)

        has = True
    except CalledProcessError:
        has = False

    return has


def shell_run(command):
    return check_output(command, shell=True)
