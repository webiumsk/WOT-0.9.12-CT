# 2015.11.10 21:25:42 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/miniclient/lobby/header/create_squad.py
from helpers import aop
from gui.shared import events
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS

class _OnCreateSquadClickAspect(aop.Aspect):

    def atCall(self, cd):
        cd.avoid()
        cd.self.fireEvent(events.LoadViewEvent(VIEW_ALIAS.SQUAD_PROMO_WINDOW))


class OnCreateSquadClickPointcut(aop.Pointcut):

    def __init__(self):
        aop.Pointcut.__init__(self, 'gui.Scaleform.daapi.view.lobby.header.LobbyHeader', 'LobbyHeader', 'showSquad', aspects=(_OnCreateSquadClickAspect,))
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\miniclient\lobby\header\create_squad.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:25:42 Støední Evropa (bìžný èas)
