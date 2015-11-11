# 2015.11.10 21:26:17 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/__init__.py
from gui.Scaleform.genConsts.CONTEXT_MENU_HANDLER_TYPE import CONTEXT_MENU_HANDLER_TYPE
from gui.Scaleform.managers.context_menu import ContextMenuManager
ContextMenuManager.registerHandler(CONTEXT_MENU_HANDLER_TYPE.APPEAL_USER, 'gui.Scaleform.daapi.view.lobby.user_cm_handlers', 'AppealCMHandler')
ContextMenuManager.registerHandler(CONTEXT_MENU_HANDLER_TYPE.BASE_USER, 'gui.Scaleform.daapi.view.lobby.user_cm_handlers', 'BaseUserCMHandler')
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\scaleform\daapi\view\__init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:26:17 Støední Evropa (bìžný èas)
