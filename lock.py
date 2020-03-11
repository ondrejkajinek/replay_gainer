"""
Provides simple locking mechanism via tmpfile
"""

import os


class LockError(RuntimeError):
    """
    Raised when lock operations fails, e.g., lock cannot be obtained
    """
    pass


class Lock():
    """
    Implements locking facility for gainer
    """

    lockfile = "/tmp/mpd_gainer.lock"

    def __init__(self):
        pass

    def acquire(self):
        """Tries to acquire lock. Raises LockError on failure"""
        if os.path.isfile(self.lockfile):
            raise LockError("Another active lock already exists!")

        try:
            with open(self.lockfile, "w"):
                pass
        except Exception as exc:
            self.release()
            raise LockError(
                "Couldn't create lock file, error: %s" % (exc,)
            )


    def release(self):
        """
        Releases acquired lock
        """
        if os.path.isfile(self.lockfile):
            os.remove(self.lockfile)
