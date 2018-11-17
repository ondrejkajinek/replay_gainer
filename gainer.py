# coding: utf8

from os import path

from utils import directories
from utils import error, info

MUSIC_DIRECTORY_KEY = "music_directory"


class Gainer(object):

    TIME_MARK_FILE = path.expanduser("~/.config/mpd_gainer/.time_mark")

    def __init__(self, options):
        self._directory = options.directory or self._get_mpd_dir()
        self._force = options.force
        self._gainers = []
        self._method = "add" if options.add_replay_gain else "remove"
        self._load_gainers(options)
        if options.debug:
            info("Running in debug mode, processed dirs will be printed.")

    def process(self):
        for directory in self._walk_mpd_dirs():
            for gainer in self._gainers:
                try:
                    getattr(gainer, self._method)(directory, self._force)
                except Exception as exc:
                    error(
                        "Gainer '%s' failed to process directory '%s': %s" % (
                            gainer.__class__.__name__, directory, exc
                        )
                    )

    def _get_mpd_dir(self):

        def check(line):
            return line.lstrip().startswith(MUSIC_DIRECTORY_KEY)

        def get_dir(line):
            return (
                line.lstrip()[len(MUSIC_DIRECTORY_KEY):]
                .strip().strip("\"").strip("'")
            )

        try:
            with open("/etc/mpd.conf", "r") as conf_in:
                return next(get_dir(line) for line in conf_in if check(line))
        except StopIteration:
            return None

    def _load_gainers(self, options):
        if options.flac:
            from gainers import FlacGainer
            self._gainers.append(FlacGainer(options.debug))

        if options.vorbis:
            from gainers import VorbisGainer
            self._gainers.append(VorbisGainer(options.debug))

        if options.mp3:
            from gainers import Mp3Gainer
            self._gainers.append(Mp3Gainer(options.debug))

    def _walk_mpd_dirs(self):
        dirs = [self._directory]
        while dirs:
            current_dir = dirs.pop()
            dirs.extend(directories(current_dir))
            yield current_dir
