# coding: utf8

from mutagen.flac import FLAC
from mutagen.flac import error as flac_error

from .gainer import Gainer
from utils import convert_gain, info


class FlacGainer(Gainer):

    gain_program = "metaflac"
    gain_add = "metaflac --add-replay-gain %s"
    gain_remove = "metaflac --remove-replay-gain %s"

    supported_suffixes = (".flac", )

    REPLAYGAIN_TAGS = Gainer.REPLAYGAIN_TAGS + (
        ('replaygain_reference_loudness', convert_gain),
    )

    def _load_tags(self, track):
        try:
            flac = FLAC(track)
        except flac_error:
            info("No FLAC tag found in '%s', creating one", track)
            flac = FLAC()

        return flac
