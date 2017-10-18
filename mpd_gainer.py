# coding: utf8

from argparse import ArgumentParser

from gainer import Gainer
from lock import Lock, LockError


def _check_options(options):
    if all((options.add_replay_gain, options.remove_replay_gain)):
        raise RuntimeError(
            "Conflict in arguments: "
            "--add-replay-gain and --remove-replay-gain are mutually exclusive"
        )
    elif not any((options.add_replay_gain, options.remove_replay_gain)):
        print("No action selected, --add-replay-gain used as default")
        options.add_replay_gain = True

    if options.all:
        # for opt in ("flac", "vorbis", "mp3"):
        for opt in ("flac", "mp3"):
            setattr(options, opt, True)

    if not any(
        # (options.flac, options.vorbis, options.mp3)
        (options.flac, options.mp3)
    ):
        raise RuntimeError(
            "No media type selected, will do nothing. "
            "Enable at least one of the following: "
            "--process-flac, --process-mp3, --process-flac"
        )


def _get_options():

    def add_switch(parser, *args, **kwargs):
        parser.add_argument(
            *args, action="store_const", const=True, default=False, **kwargs
        )

    parser = ArgumentParser(
        description="MPD ReplayGain tool"
    )
    parser.add_argument("--directory", "-d", default=None)
    add_switch(parser, "--add-replay-gain", "-A")
    add_switch(parser, "--remove-replay-gain", "-R")
    add_switch(parser, "--debug")
    add_switch(parser, "--dry", dest="debug")
    add_switch(parser, "--force", "-F")
    media_types = ("flac", "vorbis", "mp3")
    add_switch(parser, "--all")
    for media_type in media_types:
        add_switch(parser, "--%s" % media_type)

    options = parser.parse_args()
    _check_options(options)
    return options


if __name__ == "__main__":
    try:
        lock = Lock()
    except LockError as exc:
        # TODO stderr
        print("Couldn't create lock file: %s" % exc)
        lock = None
    else:
        gainer = Gainer(_get_options())
        gainer.process()
    finally:
        if lock:
            lock.release()
