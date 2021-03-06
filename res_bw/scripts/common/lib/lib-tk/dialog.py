# 2015.11.10 21:36:32 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/lib-tk/Dialog.py
from Tkinter import *
from Tkinter import _cnfmerge
if TkVersion <= 3.6:
    DIALOG_ICON = 'warning'
else:
    DIALOG_ICON = 'questhead'

class Dialog(Widget):

    def __init__(self, master = None, cnf = {}, **kw):
        cnf = _cnfmerge((cnf, kw))
        self.widgetName = '__dialog__'
        Widget._setup(self, master, cnf)
        self.num = self.tk.getint(self.tk.call('tk_dialog', self._w, cnf['title'], cnf['text'], cnf['bitmap'], cnf['default'], *cnf['strings']))
        try:
            Widget.destroy(self)
        except TclError:
            pass

    def destroy(self):
        pass


def _test():
    d = Dialog(None, {'title': 'File Modified',
     'text': 'File "Python.h" has been modified since the last time it was saved. Do you want to save it before exiting the application.',
     'bitmap': DIALOG_ICON,
     'default': 0,
     'strings': ('Save File', 'Discard Changes', 'Return to Editor')})
    print d.num
    return


if __name__ == '__main__':
    t = Button(None, {'text': 'Test',
     'command': _test,
     Pack: {}})
    q = Button(None, {'text': 'Quit',
     'command': t.quit,
     Pack: {}})
    t.mainloop()
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\lib-tk\dialog.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:36:32 St�edn� Evropa (b�n� �as)
