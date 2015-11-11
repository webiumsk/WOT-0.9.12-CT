# 2015.11.10 21:30:09 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/messenger/ext/ROPropertyMeta.py


def getMethod(name):

    def _getMethod(self):
        return self.__readonly__[name]

    return _getMethod


class ROPropertyMeta(type):

    def __new__(cls, className, bases, classDict):
        readonly = classDict.get('__readonly__', {})
        for name, default in readonly.items():
            classDict[name] = property(getMethod(name))

        return type.__new__(cls, className, bases, classDict)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\messenger\ext\ropropertymeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:30:09 Støední Evropa (bìžný èas)
