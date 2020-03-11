import functools
import os


def escape(directory):
    """Escapes characters for bash"""
    return functools.reduce(
        lambda value, char: value.replace(char, "\\" + char),
        " ()'&[]",
        directory
    )


def files(directory):
    """Returns iterator over files in directory"""
    return _dir_iterator(directory, os.path.isfile)


def directories(directory):
    """Returns iterator over subdirectories in directory"""
    return _dir_iterator(directory, os.path.isdir)


def _dir_iterator(directory, condition):
    return (
        os.path.join(directory, item)
        for item
        in os.listdir(directory)
        if condition(os.path.join(directory, item))
    )
