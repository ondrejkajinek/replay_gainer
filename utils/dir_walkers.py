# coding: utf8

from os import listdir, path


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
