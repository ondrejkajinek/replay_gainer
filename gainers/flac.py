# coding: utf8

from os import path

from .gainer import Gainer


class FlacGainer(Gainer):

    gain_programm = "metaflac"

    supported_suffixes = (".flac", )

    def _add_command(self, directory):
        return """%s --add-replay-gain %s""" % (
            self.gain_programm, path.join(directory, "*.flac")
        )

    def _remove_command(self, directory):
        return """%s --remove-replay-gain %s""" % (
            self.gain_programm, path.join(directory, "*.flac")
        )
