# 2015.11.10 21:35:07 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/distutils/log.py
"""A simple log mechanism styled after PEP 282."""
DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
FATAL = 5
import sys

class Log:

    def __init__(self, threshold = WARN):
        self.threshold = threshold

    def _log(self, level, msg, args):
        if level not in (DEBUG,
         INFO,
         WARN,
         ERROR,
         FATAL):
            raise ValueError('%s wrong log level' % str(level))
        if level >= self.threshold:
            if args:
                msg = msg % args
            if level in (WARN, ERROR, FATAL):
                stream = sys.stderr
            else:
                stream = sys.stdout
            stream.write('%s\n' % msg)
            stream.flush()

    def log(self, level, msg, *args):
        self._log(level, msg, args)

    def debug(self, msg, *args):
        self._log(DEBUG, msg, args)

    def info(self, msg, *args):
        self._log(INFO, msg, args)

    def warn(self, msg, *args):
        self._log(WARN, msg, args)

    def error(self, msg, *args):
        self._log(ERROR, msg, args)

    def fatal(self, msg, *args):
        self._log(FATAL, msg, args)


_global_log = Log()
log = _global_log.log
debug = _global_log.debug
info = _global_log.info
warn = _global_log.warn
error = _global_log.error
fatal = _global_log.fatal

def set_threshold(level):
    old = _global_log.threshold
    _global_log.threshold = level
    return old


def set_verbosity(v):
    if v <= 0:
        set_threshold(WARN)
    elif v == 1:
        set_threshold(INFO)
    elif v >= 2:
        set_threshold(DEBUG)
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\distutils\log.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:35:07 St�edn� Evropa (b�n� �as)
