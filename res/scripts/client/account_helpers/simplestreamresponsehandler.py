# 2015.11.10 21:24:47 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/client/account_helpers/SimpleStreamResponseHandler.py
import weakref, zlib, cPickle
import AccountCommands
from debug_utils import *

class SimpleStreamResponseHandler(object):

    def __init__(self, account, callback, default = None):
        self.__accountRef = weakref.ref(account)
        self.__callback = callback
        self.__default = default

    def __call__(self, requestID, resultID, errorStr, ext = {}):
        if resultID != AccountCommands.RES_STREAM:
            self.__callback(resultID, self.__default)
        else:
            self.__accountRef()._subscribeForStream(requestID, self.__onStreamComplete)

    def __onStreamComplete(self, isSuccess, data):
        if isSuccess:
            if data is None:
                LOG_CODEPOINT_WARNING()
                isSuccess = False
            else:
                try:
                    data = zlib.decompress(data)
                    data = cPickle.loads(data)
                except:
                    LOG_CURRENT_EXCEPTION()
                    isSuccess = False

        if isSuccess:
            self.__callback(AccountCommands.RES_STREAM, data)
        else:
            self.__callback(AccountCommands.RES_FAILURE, self.__default)
        return
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\account_helpers\simplestreamresponsehandler.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:24:47 St�edn� Evropa (b�n� �as)
