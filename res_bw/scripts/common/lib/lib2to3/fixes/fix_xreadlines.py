# 2015.11.10 21:37:01 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/lib2to3/fixes/fix_xreadlines.py
"""Fix "for x in f.xreadlines()" -> "for x in f".

This fixer will also convert g(f.xreadlines) into g(f.__iter__)."""
from .. import fixer_base
from ..fixer_util import Name

class FixXreadlines(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = "\n    power< call=any+ trailer< '.' 'xreadlines' > trailer< '(' ')' > >\n    |\n    power< any+ trailer< '.' no_call='xreadlines' > >\n    "

    def transform(self, node, results):
        no_call = results.get('no_call')
        if no_call:
            no_call.replace(Name(u'__iter__', prefix=no_call.prefix))
        else:
            node.replace([ x.clone() for x in results['call'] ])
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\lib2to3\fixes\fix_xreadlines.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:37:01 St�edn� Evropa (b�n� �as)
