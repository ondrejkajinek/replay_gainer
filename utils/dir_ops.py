# coding: utf8

from os import listdir, path


def escape(directory):
    # TODO: something functional and nice :)
    escaped = " ()'"
    fixed = directory
    for char in escaped:
        fixed = fixed.replace(char, "\\" + char)

    return fixed


def files(directory):
    return _dir_iterator(directory, path.isfile)


def directories(directory):
    return _dir_iterator(directory, path.isdir)


def _dir_iterator(directory, condition):
    return (
        path.join(directory, item)
        for item
        in listdir(directory)
        if condition(path.join(directory, item))
    )
