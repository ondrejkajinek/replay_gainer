# coding: utf8

from os import listdir, path

MUSIC_DIRECTORY_KEY = "music_directory"


class Gainer(object):

    TIME_MARK_FILE = path.expanduser("~/.config/mpd_gainer/.time_mark")

    def __init__(self, options):
        self._directory = options.directory or self._get_mpd_dir()
        self._force = options.force
        self._method = "add" if options.add_replay_gain else "remove"
        self._load_gainers(options)
        if options.debug:
            print("Running in debug mode, processed dirs will be printed.")

    def process(self, start_time):
        for directory in self._walk_mpd_dirs():
            for gainer in self.gainers.itervalues():
                getattr(gainer, self._method)(
                    directory, start_time, self._force
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
        gainers = []
        if options.process_flac:
            from gainers import FlacGainer
            gainers.append(FlacGainer(options.debug))

        if options.process_vorbis:
            from gainers import VorbisGainer
            gainers.append(VorbisGainer(options.debug))

        if options.process_mp3:
            from gainers import Mp3Gainer
            gainers.append(Mp3Gainer(options.debug))

        self.gainers = {
            suffix: gainer
            for gainer in gainers
            for suffix in gainer.supported_suffixes
        }

    def _subdirs(self, directory):
        for item in listdir(directory):
            item_path = path.join(directory, item)
            if path.isdir(item_path):
                yield item_path

    def _walk_mpd_dirs(self):
        dirs = [self._directory]
        while dirs:
            current_dir = dirs.pop()
            dirs.extend(list(self._subdirs(current_dir)))
            yield current_dir
