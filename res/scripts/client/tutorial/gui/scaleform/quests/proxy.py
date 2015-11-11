# 2015.11.10 21:31:13 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/client/tutorial/gui/Scaleform/quests/proxy.py
from tutorial.gui import GUI_EFFECT_NAME
from tutorial.gui.Scaleform import effects_player
from tutorial.gui.Scaleform.lobby.proxy import SfLobbyProxy
from tutorial.gui.Scaleform.quests import settings
from tutorial.gui.commands import GUICommandsFactory

class SfQuestsProxy(SfLobbyProxy):

    def __init__(self):
        effects = {GUI_EFFECT_NAME.SHOW_WINDOW: effects_player.ShowWindowEffect(settings.WINDOW_ALIAS_MAP),
         GUI_EFFECT_NAME.UPDATE_CONTENT: effects_player.UpdateContentEffect(),
         GUI_EFFECT_NAME.SHOW_HINT: effects_player.ShowChainHint()}
        super(SfQuestsProxy, self).__init__(effects_player.EffectsPlayer(effects))
        self._commands = GUICommandsFactory()

    def fini(self, isItemsRevert = True):
        self._commands = None
        super(SfQuestsProxy, self).fini(isItemsRevert)
        return

    def getViewSettings(self):
        return settings.QUESTS_VIEW_SETTINGS

    def invokeCommand(self, command):
        self._commands.invoke(None, command)
        return
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\tutorial\gui\scaleform\quests\proxy.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:31:13 St�edn� Evropa (b�n� �as)
