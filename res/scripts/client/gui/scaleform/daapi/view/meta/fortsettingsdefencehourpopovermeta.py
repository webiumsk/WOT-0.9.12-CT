# 2015.11.10 21:27:54 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FortSettingsDefenceHourPopoverMeta.py
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class FortSettingsDefenceHourPopoverMeta(SmartPopOverView):

    def onApply(self, hour):
        self._printOverrideError('onApply')

    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setTextsS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setTexts(data)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\scaleform\daapi\view\meta\fortsettingsdefencehourpopovermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:27:54 St�edn� Evropa (b�n� �as)
