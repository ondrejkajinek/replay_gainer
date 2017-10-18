# coding: utf8

from os import listdir, path
from sys import exc_info

from mutagen.apev2 import APEv2
from mutagen.apev2 import error as apev2_error
from mutagen.id3 import ID3, TXXX
from mutagen.id3 import error as id3_error
from mutagen.id3 import Encoding as Id3Encoding

from .gainer import Gainer
from utils import error, info


class Mp3Gainer(Gainer):

    gain_program = "mp3gain"

    supported_suffixes = (".mp3", )

    REPLAYGAIN_TAGS = Gainer.REPLAYGAIN_TAGS + (
        ("mp3gain_album_minmax", None),
        ("mp3gain_minmax", None)
    )

    def add(self, directory, force=False):
        super(Mp3Gainer, self).add(directory, force)
        for track in self._list_tracks(directory):
            try:
                self._apev2_to_id3(track)
            except:
                pass

    def remove(self, directory, force=False):
        super(Mp3Gainer, self).remove(directory, force)
        if self._needs_remove(directory):
            for track in self._list_tracks(directory):
                try:
                    self._remove_id3_replaygain(track)
                except:
                    pass

    def _add_command(self, directory):
        return """%s -s a %s""" % (
            self.gain_program, path.join(directory, "*.mp3")
        )

    def _apev2_to_id3(self, track):
        ape = self._load_ape(track)
        id3 = self._load_tags(track)
        saving = False
        for tag_name, converter in self.REPLAYGAIN_TAGS:
            if tag_name in ape:
                try:
                    self._copy_replaygain_tag(ape, id3, tag_name, converter)
                except ValueError as e:
                    error("Error when copying replay gain tag: %r", e)
                else:
                    saving = True

        if saving:
            id3.save(track)
            info("Track '%s': APEv2 copied to ID3", track)
        else:
            info("No changes made in file '%s', not saving", track)

    def _copy_replaygain_tag(self, ape, id3, tag_name, converter):
        if callable(converter):
            try:
                value = converter(str(ape[tag_name]))
            except ValueError:
                raise
        else:
            value = str(ape[tag_name])

        id3.add(TXXX(encoding=Id3Encoding.UTF8, desc=tag_name, text=value))

    def _load_ape(self, track):
        try:
            ape = APEv2(track)
        except apev2_error:
            info("No APEv2 on file '%s', skipping", track)
            raise
        except:
            error("Error: %s", exc_info()[1])
            raise
        else:
            return ape

    def _load_tags(self, track):
        try:
            id3 = ID3(track)
        except id3_error:
            info("No ID3 tag found in '%s', creating one", track)
            id3 = ID3()

        return id3

    def _list_tracks(self, directory):
        for file_ in listdir(directory):
            if path.splitext(file_)[1].lower() == ".mp3":
                yield path.join(directory, file_)

    def _remove_id3_replaygain(self, track):
        id3 = self._load_tags(track)
        for tag in self._replay_gain_tag_names():
            id3.pop(tag, None)

        id3.save(track)

    def _remove_command(self, directory):
        return """%s -s d %s""" % (
            self.gain_program, path.join(directory, "*.mp3")
        )

    def _replay_gain_tag_names(self):
        for tag in self.REPLAYGAIN_TAGS:
            yield "TXXX:%s" % tag[0]
