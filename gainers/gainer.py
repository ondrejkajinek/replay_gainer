# coding: utf8

from utils import convert_gain, convert_peak, has_command, run


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

    def __init__(self):
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

    def __str__(self):
        return self.__class__.__name__

    def add(self, directory):
        run(self._add_command(self._fix_directory(directory)), shell=True)

    def remove(self, directory):
        run(self._remove_command(self._fix_directory(directory)), shell=True)

    def _fix_directory(self, directory):
        # TODO: something functional and nice :)
        escaped = " ()'"
        fixed = directory
        for char in escaped:
            fixed = fixed.replace(char, "\\" + char)

        return fixed
