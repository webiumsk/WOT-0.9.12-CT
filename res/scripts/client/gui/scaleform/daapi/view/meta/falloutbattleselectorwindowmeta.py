# 2015.11.10 21:27:49 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FalloutBattleSelectorWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class FalloutBattleSelectorWindowMeta(AbstractWindowView):

    def onDominationBtnClick(self):
        self._printOverrideError('onDominationBtnClick')

    def onMultiteamBtnClick(self):
        self._printOverrideError('onMultiteamBtnClick')

    def as_setInitDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setBtnStatesS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setBtnStates(data)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\scaleform\daapi\view\meta\falloutbattleselectorwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:27:49 Støední Evropa (bìžný èas)
