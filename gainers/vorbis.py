from .gainer import Gainer


class VorbisGainer(Gainer):

    # gain_program = ""
    # gain_add = ""
    # gain_remove = ""

    supported_suffixes = (".ogg", )

    def _load_tags(self, track):
        raise NotImplementedError()

    def _replay_gain_tag_names(self):
        raise NotImplementedError()
