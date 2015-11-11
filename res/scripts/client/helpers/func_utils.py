# 2015.11.10 21:30:00 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/helpers/func_utils.py
import BigWorld
from functools import partial

def callback(delay, obj, methodName, *args):
    return BigWorld.callback(delay, partial(callMethod, obj, methodName, *args))


def callMethod(obj, methodName, *args):
    if hasattr(obj, methodName):
        getattr(obj, methodName)(*args)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\helpers\func_utils.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:30:00 Støední Evropa (bìžný èas)
