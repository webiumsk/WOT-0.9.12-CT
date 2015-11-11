# 2015.11.10 21:38:39 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/xml/__init__.py
"""Core XML support for Python.

This package contains four sub-packages:

dom -- The W3C Document Object Model.  This supports DOM Level 1 +
       Namespaces.

parsers -- Python wrappers for XML parsers (currently only supports Expat).

sax -- The Simple API for XML, developed by XML-Dev, led by David
       Megginson and ported to Python by Lars Marius Garshol.  This
       supports the SAX 2 API.

etree -- The ElementTree XML library.  This is a subset of the full
       ElementTree XML release.

"""
__all__ = ['dom',
 'parsers',
 'sax',
 'etree']
_MINIMUM_XMLPLUS_VERSION = (0, 8, 4)
try:
    import _xmlplus
except ImportError:
    pass
else:
    try:
        v = _xmlplus.version_info
    except AttributeError:
        pass
    else:
        if v >= _MINIMUM_XMLPLUS_VERSION:
            import sys
            _xmlplus.__path__.extend(__path__)
            sys.modules[__name__] = _xmlplus
        else:
            del v
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\xml\__init__.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:38:39 St�edn� Evropa (b�n� �as)
