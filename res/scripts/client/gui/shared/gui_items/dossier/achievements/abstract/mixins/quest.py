# 2015.11.10 21:29:22 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/shared/gui_items/dossier/achievements/abstract/mixins/Quest.py
from gui.shared.gui_items.dossier.achievements import validators

class Quest(object):

    @classmethod
    def checkIsValid(cls, block, name, dossier):
        return validators.questHasThisAchievementAsBonus(name, block) or validators.alreadyAchieved(cls, name, block, dossier)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\shared\gui_items\dossier\achievements\abstract\mixins\quest.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:29:22 Støední Evropa (bìžný èas)
