# coding: utf8

from os import path, remove


class LockError(RuntimeError):
    pass


class Lock(object):

    lockfile = "/tmp/mpd_gainer.lock"

    def __init__(self):
        if path.isfile(self.lockfile):
            raise LockError("Another active lock already exists!")

        try:
            with open(self.lockfile, "w"):
                pass
        except Exception as exc:
            self.release()
            raise LockError(
                "Couldn't create lock file, error: %s" % (exc,)
            )

    def lock_time(self):
        try:
            return path.getmtime(self.lockfile)
        except:
            raise LockError("Lock is not active!")

    def release(self):
        if path.isfile(self.lockfile):
            remove(self.lockfile)
