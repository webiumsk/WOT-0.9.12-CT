# 2015.11.10 21:26:23 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/meta/FalloutScorePanelMeta.py
from gui.Scaleform.daapi.view.battle.meta.BattleComponentMeta import BattleComponentMeta

class FalloutScorePanelMeta(BattleComponentMeta):

    def as_initWarningValue(self, warningValue):
        self._flashObject.as_initWarningValue(warningValue)

    def as_setDataS(self, contextType, maxValue, playerScore, allyValue, enemyValue, playerName, enemyName, props):
        self._flashObject.as_setData(contextType, maxValue, playerScore, allyValue, enemyValue, playerName, enemyName, props)

    def as_onSettingsChanged(self):
        self._flashObject.as_onSettingsChanged()
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\scaleform\daapi\view\battle\meta\falloutscorepanelmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:26:23 St�edn� Evropa (b�n� �as)
