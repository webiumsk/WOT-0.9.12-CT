# 2015.11.10 21:25:41 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/client/gui/miniclient/lobby/__init__.py
import tank_carousel
from hangar import configure_pointcuts as _configure_hangar_pointcuts
from header import configure_pointcuts as _configure_header_pointcuts
from tank_carousel import configure_pointcuts as _configure_carousel_pointcuts
from MiniclientDescriptionWindow import MiniclientDescriptionWindow

def configure_pointcuts(config):
    _configure_carousel_pointcuts(config)
    _configure_hangar_pointcuts(config)
    _configure_header_pointcuts(config)
    MiniclientDescriptionWindow()
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\miniclient\lobby\__init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:25:41 St�edn� Evropa (b�n� �as)
