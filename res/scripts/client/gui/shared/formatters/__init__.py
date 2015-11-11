# 2015.11.10 21:29:02 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/shared/formatters/__init__.py
import BigWorld
from gui.shared.formatters import icons
from gui.shared.formatters import text_styles
from gui.shared.formatters import time_formatters
__all__ = ('icons', 'text_styles', 'time_formatters')

def getClanAbbrevString(clanAbbrev):
    return '[{0:>s}]'.format(clanAbbrev)


def getGlobalRatingFmt(globalRating):
    if globalRating >= 0:
        return BigWorld.wg_getIntegralFormat(globalRating)
    return '--'
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\shared\formatters\__init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:29:02 Støední Evropa (bìžný èas)
