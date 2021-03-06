# 2015.11.10 21:36:00 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/hotshot/stones.py
import errno
import hotshot
import hotshot.stats
import sys
import test.pystone

def main(logfile):
    p = hotshot.Profile(logfile)
    benchtime, stones = p.runcall(test.pystone.pystones)
    p.close()
    print 'Pystone(%s) time for %d passes = %g' % (test.pystone.__version__, test.pystone.LOOPS, benchtime)
    print 'This machine benchmarks at %g pystones/second' % stones
    stats = hotshot.stats.load(logfile)
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    try:
        stats.print_stats(20)
    except IOError as e:
        if e.errno != errno.EPIPE:
            raise


if __name__ == '__main__':
    if sys.argv[1:]:
        main(sys.argv[1])
    else:
        import tempfile
        main(tempfile.NamedTemporaryFile().name)
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\hotshot\stones.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:36:00 St�edn� Evropa (b�n� �as)
