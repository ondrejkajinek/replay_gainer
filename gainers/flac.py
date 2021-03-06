from mutagen.flac import FLAC
from mutagen.flac import error as flac_error

from utils import convert_gain, info
from .base_gainer import BaseGainer


class FlacGainer(BaseGainer):

    gain_program = "metaflac"
    gain_add = "metaflac --add-replay-gain %s"
    gain_remove = "metaflac --remove-replay-gain %s"

    supported_suffixes = (".flac", )

    REPLAYGAIN_TAGS = BaseGainer.REPLAYGAIN_TAGS + (
        ('replaygain_reference_loudness', convert_gain),
    )

    def _load_tags(self, track):
        try:
            flac = FLAC(track)
        except flac_error:
            info("No FLAC tag found in '%s', creating one", track)
            flac = FLAC()

        return flac
