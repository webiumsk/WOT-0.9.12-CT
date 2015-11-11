# 2015.11.10 21:31:23 Støední Evropa (bìžný èas)
# Embedded file name: scripts/common/BWAutoImport.py
import collections
from collections import namedtuple as _orig_namedtuple
import sys as _sys

def _fixed_namedtuple(*args, **kwargs):
    res = _orig_namedtuple(*args, **kwargs)
    res._asdict = _fixed_asdict
    try:
        res.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass

    return res


def _fixed_asdict(t):
    return dict(zip(t._fields, t))


collections.namedtuple = _fixed_namedtuple
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\common\bwautoimport.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:31:23 Støední Evropa (bìžný èas)
