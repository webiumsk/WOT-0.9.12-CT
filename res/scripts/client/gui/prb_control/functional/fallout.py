# 2015.11.10 21:25:54 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/prb_control/functional/fallout.py
from constants import QUEUE_TYPE
from debug_utils import LOG_ERROR
from gui.prb_control.context import pre_queue_ctx
from gui.prb_control.events_dispatcher import g_eventDispatcher
from gui.prb_control.functional.interfaces import IPrbEntry
from gui.prb_control.settings import FUNCTIONAL_EXIT

class FalloutEntry(IPrbEntry):

    def makeDefCtx(self):
        return pre_queue_ctx.JoinModeCtx(QUEUE_TYPE.EVENT_BATTLES, funcExit=FUNCTIONAL_EXIT.FALLOUT)

    def create(self, ctx, callback = None):
        raise Exception, 'FalloutEntry cannot be created'

    def join(self, ctx, callback = None):
        result = True
        if not isinstance(ctx, pre_queue_ctx.JoinModeCtx):
            result = False
            LOG_ERROR('Invalid context to join fallout mode', ctx)
        else:
            g_eventDispatcher.loadFallout()
        if callback:
            callback(result)

    def select(self, ctx, callback = None):
        self.join(ctx, callback=callback)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\prb_control\functional\fallout.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:25:54 Støední Evropa (bìžný èas)
