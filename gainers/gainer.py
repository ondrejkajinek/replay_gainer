# coding: utf8

from utils import convert_gain, convert_peak, files, has_command, shell_run
from utils import TimeRange

from os import path


class Gainer(object):

    REPLAYGAIN_TAGS = (
        ("mp3gain_album_minmax", None),
        ("mp3gain_minmax", None),
        ("replaygain_album_gain", convert_gain),
        ("replaygain_album_peak", convert_peak),
        ("replaygain_track_gain", convert_gain),
        ("replaygain_track_peak", convert_peak),
    )

    gain_program = None

    supported_suffixes = set()

    def __init__(self, debug):
        self._check_environment()
        self._debug = debug

    def __str__(self):
        return self.__class__.__name__

    def add(self, directory, start_time, force=False):
        if self._needs_add(directory, start_time, force):
            print(
                "Adding replay gain tags in directory '%s' with %r" % (
                    directory, self.__class__.__name__
                )
            )
            if not self._debug:
                shell_run(
                    self._add_command(self._fix_directory(directory))
                )
                self._create_time_mark(directory)

    def remove(self, directory, start_time, force=False):
        if self._needs_remove(directory):
            print(
                "Removing replay gain tags in directory '%s' with %r" % (
                    directory, self.__class__.__name__
                )
            )
            if not self._debug:
                shell_run(
                    self._remove_command(self._fix_directory(directory))
                )

    def _create_time_mark(self, directory):
        with open(self._mark_file(directory), "w"):
            pass

    def _check_environment(self):
        if self.gain_program is None:
            raise RuntimeError(
                "No replay-gain util configured for class %r" % str(self)
            )

        if not has_command(self.gain_program):
            raise RuntimeError(
                "Program %r is not available" % self.gain_program
            )

        if not self.supported_suffixes:
            raise RuntimeError(
                "Gainer %r does not support any file suffix!" % str(self)
            )

    def _fix_directory(self, directory):
        # TODO: something functional and nice :)
        escaped = " ()'"
        fixed = directory
        for char in escaped:
            fixed = fixed.replace(char, "\\" + char)

        return fixed

    def _get_min_time(self, directory):
        try:
            return path.getmtime(self._mark_file(directory))
        except OSError:
            return 0

    def _mark_file(self, directory):
        return path.join(
            directory, ".%s.timestamp" % self.gain_program.lower()
        )

    def _needs_add(self, directory, start_time, force):
        time_range = TimeRange(
            0 if force else self._get_min_time(directory),
            start_time
        )
        return any(
            (
                path.splitext(item)[1] in self.supported_suffixes and
                path.getmtime(item) in time_range
            )
            for item
            in files(directory)
        )

    def _needs_remove(self, directory):
        return any(
            path.splitext(item)[1] in self.supported_suffixes
            for item
            in files(directory)
        )
