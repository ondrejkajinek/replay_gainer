# coding: utf8

from .gainer import Gainer


class VorbisGainer(Gainer):

    # gain_programm = ""

    supported_suffixes = (".ogg", )

    def _add_command(self, directory):
        pass
        # TODO
        # return """%s --add-replay-gain %s""" % (
        #     self.gain_programm, path.join(directory, "*.flac")
        # )

    def _remove_command(self, directory):
        pass
        # TODO
        # return """%s --remove-replay-gain %s""" % (
        #     self.gain_programm, path.join(directory, "*.flac")
        # )
