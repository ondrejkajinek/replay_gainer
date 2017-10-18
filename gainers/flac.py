# coding: utf8

from mutagen.flac import FLAC
from mutagen.flac import error as flac_error
from os import path

from .gainer import Gainer
from utils import convert_gain, info


class FlacGainer(Gainer):

    gain_program = "metaflac"

    supported_suffixes = (".flac", )

    REPLAYGAIN_TAGS = Gainer.REPLAYGAIN_TAGS + (
        ('replaygain_reference_loudness', convert_gain),
    )

    def _add_command(self, directory):
        return """%s --add-replay-gain %s""" % (
            self.gain_program, path.join(directory, "*.flac")
        )

    def _load_tags(self, track):
        try:
            flac = FLAC(track)
        except flac_error:
            info("No FLAC tag found in '%s', creating one", track)
            flac = FLAC()

        return flac

    def _remove_command(self, directory):
        return """%s --remove-replay-gain %s""" % (
            self.gain_program, path.join(directory, "*.flac")
        )
