# 2015.11.10 21:25:59 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/prb_control/functional/__init__.py
from constants import IS_DEVELOPMENT
from gui.prb_control.functional.interfaces import IStatefulFunctional

def initDevFunctional():
    if IS_DEVELOPMENT:
        try:
            from gui.development.dev_prebattle import init
        except ImportError:
            init = lambda : None

        init()


def finiDevFunctional():
    if IS_DEVELOPMENT:
        try:
            from gui.development.dev_prebattle import fini
        except ImportError:
            fini = lambda : None

        fini()


def isStatefulFunctional(functional):
    return isinstance(functional, IStatefulFunctional)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\prb_control\functional\__init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:25:59 Støední Evropa (bìžný èas)
