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

    def add(self, directory, start_time, force=False):
        super(Mp3Gainer, self).add(directory, start_time, force)
        for track in self._list_tracks(directory):
            try:
                self._apev2_to_id3(track)
            except:
                pass

    def remove(self, directory, start_time, force=False):
        super(Mp3Gainer, self).remove(directory, start_time, force)
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
        id3 = self._load_id3(track)
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

    def _load_id3(self, track):
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
        id3 = self._load_id3(track)
        for tag_name, tag_value in id3:
            info("%s -> %s", tag_name, tag_value)
            # TODO: remove those TXXX tags that are from REPLAYGAIN_TAGS

    def _remove_command(self, directory):
        return """%s -s d %s""" % (
            self.gain_program, path.join(directory, "*.mp3")
        )
