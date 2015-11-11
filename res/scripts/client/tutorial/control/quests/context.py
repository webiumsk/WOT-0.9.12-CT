# 2015.11.10 21:31:02 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/tutorial/control/quests/context.py
from tutorial.control import game_vars
from tutorial.control.context import StartReqs
from tutorial.settings import TUTORIAL_SETTINGS
from tutorial import doc_loader

def getQuestsDescriptor():
    return doc_loader.loadDescriptorData(TUTORIAL_SETTINGS.QUESTS)


class QuestsStartReqs(StartReqs):

    def isEnabled(self):
        return True

    def __validateTutorialsCompleted(self, ctx, descriptor):
        cache = ctx.cache
        self._areAllBonusesReceived = descriptor.areAllBonusesReceived(ctx.bonusCompleted)
        if not self._areAllBonusesReceived:
            return False
        else:
            if cache.wasReset():
                cache.setRefused(True)
            return True

    def prepare(self, ctx):
        ctx.bonusCompleted = game_vars.getTutorialsCompleted()

    def process(self, descriptor, ctx):
        return not self.__validateTutorialsCompleted(ctx, descriptor)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\tutorial\control\quests\context.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:31:02 Støední Evropa (bìžný èas)
