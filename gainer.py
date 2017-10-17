# coding: utf8

from os import listdir, mkdir, path
from time_range import TimeRange

MUSIC_DIRECTORY_KEY = "music_directory"


class Gainer(object):

    TIME_MARK_FILE = path.expanduser("~/.config/mpd_gainer/.time_mark")

    def __init__(self, options):
        self._debug = options.debug
        self._directory = options.directory or self._get_mpd_dir()
        self._force = options.force
        self._method = "add" if options.add_replay_gain else "remove"
        self._load_gainers(options)
        if self._debug:
            print("Running in debug mode, processed dirs will be printed.")

    def process(self, start_time):
        self._time_range = TimeRange(self._get_min_time(), start_time)
        for directory, used_gainers in self._walk_mpd_dirs():
            for gainer in used_gainers:
                print(
                    "Processing directory '%s' with %r" % (
                        directory, gainer.__class__.__name__
                    )
                )
                if not self._debug:
                    getattr(gainer, self._method)(directory)

        if not self._debug:
            self._create_time_mark()

    def _create_time_mark(self):
        if not path.isdir(path.dirname(self.TIME_MARK_FILE)):
            mkdir(path.dirname(self.TIME_MARK_FILE))

        with open(self.TIME_MARK_FILE, "w"):
            pass

    def _find_gainer(self, item_path):
        suffix = path.splitext(item_path)[1]
        file_mtime = path.getmtime(item_path)
        return (
            self.gainers[suffix]
            if (
                suffix in self.gainers and
                (file_mtime in self._time_range or self._force)
            )
            else None
        )

    def _get_min_time(self):
        return (
            path.getmtime(self.TIME_MARK_FILE)
            if path.isfile(self.TIME_MARK_FILE)
            else 0
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
            gainers.append(FlacGainer())

        if options.process_vorbis:
            from gainers import VorbisGainer
            gainers.append(VorbisGainer())

        if options.process_mp3:
            from gainers import Mp3Gainer
            gainers.append(Mp3Gainer())

        self.gainers = {
            suffix: gainer
            for gainer in gainers
            for suffix in gainer.supported_suffixes
        }

    def _process_dir(self, directory):
        new_dirs = []
        used_gainers = set()
        for item in listdir(directory):
            item_path = path.join(directory, item)
            if path.isdir(item_path):
                new_dirs.append(item_path)
            else:
                required_gainer = self._find_gainer(item_path)
                if required_gainer:
                    used_gainers.add(required_gainer)

        return used_gainers, new_dirs

    def _walk_mpd_dirs(self):
        dirs = [self._directory]
        while dirs:
            current_dir = dirs.pop()
            used_gainers, new_dirs = self._process_dir(current_dir)
            dirs.extend(new_dirs)
            yield current_dir, used_gainers
