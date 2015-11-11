# 2015.11.10 21:27:13 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/historicalBattles/__init__.py
from gui.Scaleform.framework import GroupedViewSettings, ViewTypes, ScopeTemplates
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.Scaleform.genConsts.PREBATTLE_ALIASES import PREBATTLE_ALIASES
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE

def getViewSettings():
    from gui.Scaleform.daapi.view.lobby.historicalBattles.HistoricalBattlesListWindow import HistoricalBattlesListWindow
    return (GroupedViewSettings(PREBATTLE_ALIASES.HISTORICAL_BATTLES_LIST_WINDOW_PY, HistoricalBattlesListWindow, 'historicalBattlesListWindow.swf', ViewTypes.WINDOW, '', PREBATTLE_ALIASES.HISTORICAL_BATTLES_LIST_WINDOW_PY, ScopeTemplates.DEFAULT_SCOPE, True),)


def getBusinessHandlers():
    return (_HistoricalBattlesBusinessHandler(),)


class _HistoricalBattlesBusinessHandler(PackageBusinessHandler):

    def __init__(self):
        listeners = ((PREBATTLE_ALIASES.HISTORICAL_BATTLES_LIST_WINDOW_PY, self.__showHBListWindow),)
        super(_HistoricalBattlesBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)

    def __showHBListWindow(self, _):
        alias = name = PREBATTLE_ALIASES.HISTORICAL_BATTLES_LIST_WINDOW_PY
        self.loadViewWithDefName(alias, name)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\scaleform\daapi\view\lobby\historicalbattles\__init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:27:13 Støední Evropa (bìžný èas)
