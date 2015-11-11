# 2015.11.10 21:28:08 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/WaitingViewMeta.py
from gui.Scaleform.framework.entities.View import View

class WaitingViewMeta(View):

    def showS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.show(data)

    def hideS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.hide(data)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\scaleform\daapi\view\meta\waitingviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:28:08 Støední Evropa (bìžný èas)
