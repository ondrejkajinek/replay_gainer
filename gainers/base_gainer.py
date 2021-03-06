import os

from utils import convert_gain, convert_peak
from utils import escape, files
from utils import info
from utils import has_command, shell_run
from .utils import contained_suffixes


class BaseGainer():

    REPLAYGAIN_TAGS = (
        ("replaygain_album_gain", convert_gain),
        ("replaygain_album_peak", convert_peak),
        ("replaygain_track_gain", convert_gain),
        ("replaygain_track_peak", convert_peak),
    )

    gain_program = None
    gain_add = None
    gain_remove = None

    supported_suffixes = set()

    def __init__(self, debug):
        self._check_environment()
        self._debug = debug

    def __str__(self):
        return self.__class__.__name__

    def add(self, directory, force=False):
        if self._needs_add(directory, force):
            info(
                "Adding replay gain tags in directory '%s' with %r" % (
                    directory, self.__class__.__name__
                )
            )
            if not self._debug:
                shell_run(self._add_command(directory))

    def remove(self, directory, force=False):
        if self._needs_remove(directory):
            info(
                "Removing replay gain tags in directory '%s' with %r" % (
                    directory, self.__class__.__name__
                )
            )
            if not self._debug:
                shell_run(self._remove_command(directory))

    def _add_command(self, directory):
        return self.gain_add % (
            " ".join(
                os.path.join(escape(directory), "*{}".format(suffix))
                for suffix
                in contained_suffixes(self.supported_suffixes, directory)
            )
        )

    def _check_environment(self):
        if None in (self.gain_program, self.gain_add, self.gain_remove):
            raise RuntimeError(
                "replay-gain util not properly configured configured for class %r" % str(self)
            )

        if not has_command(self.gain_program):
            raise RuntimeError(
                "Program %r is not available" % self.gain_program
            )

        if not self.supported_suffixes:
            raise RuntimeError(
                "Gainer %r does not support any file suffix!" % str(self)
            )

    def _has_tags(self, track):
        tags = self._load_tags(track)
        for tag_name in self._replay_gain_tag_names():
            if tag_name not in tags:
                success = False
                break
        else:
            success = True

        return success

    def _load_tags(self, track):
        raise NotImplementedError()

    def _needs_add(self, directory, force):
        return any(
            (
                os.path.splitext(item)[1] in self.supported_suffixes and
                (not self._has_tags(item) or force)
            )
            for item
            in files(directory)
        )

    def _needs_remove(self, directory):
        return any(
            (
                os.path.splitext(item)[1] in self.supported_suffixes and
                self._has_tags(item)
            )
            for item
            in files(directory)
        )

    def _remove_command(self, directory):
        return self.gain_remove % (
            " ".join(
                os.path.join(escape(directory), "*{}".format(suffix))
                for suffix
                in contained_suffixes(self.supported_suffixes, directory)
            )
        )

    def _replay_gain_tag_names(self):
        for tag in self.REPLAYGAIN_TAGS:
            yield tag[0]
