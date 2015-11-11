# 2015.11.10 21:38:23 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/plat-sunos5/IN.py
_CHAR_ALIGNMENT = 1
_SHORT_ALIGNMENT = 2
_INT_ALIGNMENT = 4
_LONG_ALIGNMENT = 8
_LONG_LONG_ALIGNMENT = 8
_DOUBLE_ALIGNMENT = 8
_LONG_DOUBLE_ALIGNMENT = 16
_POINTER_ALIGNMENT = 8
_MAX_ALIGNMENT = 16
_ALIGNMENT_REQUIRED = 1
_CHAR_ALIGNMENT = 1
_SHORT_ALIGNMENT = 2
_INT_ALIGNMENT = 4
_LONG_ALIGNMENT = 4
_LONG_LONG_ALIGNMENT = 4
_DOUBLE_ALIGNMENT = 4
_LONG_DOUBLE_ALIGNMENT = 4
_POINTER_ALIGNMENT = 4
_MAX_ALIGNMENT = 4
_ALIGNMENT_REQUIRED = 0
_CHAR_ALIGNMENT = 1
_SHORT_ALIGNMENT = 2
_INT_ALIGNMENT = 4
_LONG_LONG_ALIGNMENT = 8
_DOUBLE_ALIGNMENT = 8
_ALIGNMENT_REQUIRED = 1
_LONG_ALIGNMENT = 4
_LONG_DOUBLE_ALIGNMENT = 8
_POINTER_ALIGNMENT = 4
_MAX_ALIGNMENT = 8
_LONG_ALIGNMENT = 8
_LONG_DOUBLE_ALIGNMENT = 16
_POINTER_ALIGNMENT = 8
_MAX_ALIGNMENT = 16
_POSIX_C_SOURCE = 1
_LARGEFILE64_SOURCE = 1
_LARGEFILE_SOURCE = 1
_FILE_OFFSET_BITS = 64
_FILE_OFFSET_BITS = 32
_POSIX_C_SOURCE = 199506L
_POSIX_PTHREAD_SEMANTICS = 1
_XOPEN_VERSION = 500
_XOPEN_VERSION = 4
_XOPEN_VERSION = 3
from TYPES import *
from TYPES import *
from TYPES import *
LOCK_HELD_VALUE = 255

def SPIN_LOCK(pl):
    return pl > ipltospl(LOCK_LEVEL)


def LOCK_SAMPLE_INTERVAL(i):
    return i & 255 == 0


CLOCK_LEVEL = 10
LOCK_LEVEL = 10
DISP_LEVEL = LOCK_LEVEL + 1
PTR24_LSB = 5
PTR24_MSB = PTR24_LSB + 24
PTR24_ALIGN = 32
PTR24_BASE = 3758096384L
from TYPES import *
_POSIX_VDISABLE = 0
MAX_INPUT = 512
MAX_CANON = 256
UID_NOBODY = 60001
GID_NOBODY = UID_NOBODY
UID_NOACCESS = 60002
MAX_TASKID = 999999
MAX_MAXPID = 999999
DEFAULT_MAXPID = 999999
DEFAULT_JUMPPID = 100000
DEFAULT_MAXPID = 30000
DEFAULT_JUMPPID = 0
MAXUID = 2147483647
MAXPROJID = MAXUID
MAXLINK = 32767
NMOUNT = 40
CANBSIZ = 256
NOFILE = 20
NGROUPS_UMIN = 0
NGROUPS_UMAX = 32
NGROUPS_MAX_DEFAULT = 16
NZERO = 20
NULL = 0L
NULL = 0
CMASK = 18
CDLIMIT = 2048L
NBPS = 131072
NBPSCTR = 512
UBSIZE = 512
SCTRSHFT = 9
SYSNAME = 9
PREMOTE = 39
MAXPATHLEN = 1024
MAXSYMLINKS = 20
MAXNAMELEN = 256
NADDR = 13
PIPE_BUF = 5120
PIPE_MAX = 5120
NBBY = 8
MAXBSIZE = 8192
DEV_BSIZE = 512
DEV_BSHIFT = 9
MAXFRAG = 8
MAXOFF32_T = 2147483647
MAXOFF_T = 9223372036854775807L
MAXOFFSET_T = 9223372036854775807L
MAXOFF_T = 2147483647L
MAXOFFSET_T = 2147483647

def btodb(bytes):
    pass


def dbtob(db):
    pass


def lbtodb(bytes):
    pass


def ldbtob(db):
    pass


NCARGS32 = 1048576
NCARGS64 = 2097152
NCARGS = NCARGS64
NCARGS = NCARGS32
FSHIFT = 8
FSCALE = 1 << FSHIFT

def DELAY(n):
    return drv_usecwait(n)


def mmu_ptob(x):
    return x << MMU_PAGESHIFT


def mmu_btop(x):
    return x >> MMU_PAGESHIFT


def mmu_btopr(x):
    return x + MMU_PAGEOFFSET >> MMU_PAGESHIFT


def mmu_ptod(x):
    return x << MMU_PAGESHIFT - DEV_BSHIFT


def ptod(x):
    return x << PAGESHIFT - DEV_BSHIFT


def ptob(x):
    return x << PAGESHIFT


def btop(x):
    return x >> PAGESHIFT


def btopr(x):
    return x + PAGEOFFSET >> PAGESHIFT


def dtop(DD):
    return DD + NDPP - 1 >> PAGESHIFT - DEV_BSHIFT


def dtopt(DD):
    return DD >> PAGESHIFT - DEV_BSHIFT


_AIO_LISTIO_MAX = 4096
_AIO_MAX = -1
_MQ_OPEN_MAX = 32
_MQ_PRIO_MAX = 32
_SEM_NSEMS_MAX = INT_MAX
_SEM_VALUE_MAX = INT_MAX
_CS_PATH = 65
_CS_LFS_CFLAGS = 68
_CS_LFS_LDFLAGS = 69
_CS_LFS_LIBS = 70
_CS_LFS_LINTFLAGS = 71
_CS_LFS64_CFLAGS = 72
_CS_LFS64_LDFLAGS = 73
_CS_LFS64_LIBS = 74
_CS_LFS64_LINTFLAGS = 75
_CS_XBS5_ILP32_OFF32_CFLAGS = 700
_CS_XBS5_ILP32_OFF32_LDFLAGS = 701
_CS_XBS5_ILP32_OFF32_LIBS = 702
_CS_XBS5_ILP32_OFF32_LINTFLAGS = 703
_CS_XBS5_ILP32_OFFBIG_CFLAGS = 705
_CS_XBS5_ILP32_OFFBIG_LDFLAGS = 706
_CS_XBS5_ILP32_OFFBIG_LIBS = 707
_CS_XBS5_ILP32_OFFBIG_LINTFLAGS = 708
_CS_XBS5_LP64_OFF64_CFLAGS = 709
_CS_XBS5_LP64_OFF64_LDFLAGS = 710
_CS_XBS5_LP64_OFF64_LIBS = 711
_CS_XBS5_LP64_OFF64_LINTFLAGS = 712
_CS_XBS5_LPBIG_OFFBIG_CFLAGS = 713
_CS_XBS5_LPBIG_OFFBIG_LDFLAGS = 714
_CS_XBS5_LPBIG_OFFBIG_LIBS = 715
_CS_XBS5_LPBIG_OFFBIG_LINTFLAGS = 716
_SC_ARG_MAX = 1
_SC_CHILD_MAX = 2
_SC_CLK_TCK = 3
_SC_NGROUPS_MAX = 4
_SC_OPEN_MAX = 5
_SC_JOB_CONTROL = 6
_SC_SAVED_IDS = 7
_SC_VERSION = 8
_SC_PASS_MAX = 9
_SC_LOGNAME_MAX = 10
_SC_PAGESIZE = 11
_SC_XOPEN_VERSION = 12
_SC_NPROCESSORS_CONF = 14
_SC_NPROCESSORS_ONLN = 15
_SC_STREAM_MAX = 16
_SC_TZNAME_MAX = 17
_SC_AIO_LISTIO_MAX = 18
_SC_AIO_MAX = 19
_SC_AIO_PRIO_DELTA_MAX = 20
_SC_ASYNCHRONOUS_IO = 21
_SC_DELAYTIMER_MAX = 22
_SC_FSYNC = 23
_SC_MAPPED_FILES = 24
_SC_MEMLOCK = 25
_SC_MEMLOCK_RANGE = 26
_SC_MEMORY_PROTECTION = 27
_SC_MESSAGE_PASSING = 28
_SC_MQ_OPEN_MAX = 29
_SC_MQ_PRIO_MAX = 30
_SC_PRIORITIZED_IO = 31
_SC_PRIORITY_SCHEDULING = 32
_SC_REALTIME_SIGNALS = 33
_SC_RTSIG_MAX = 34
_SC_SEMAPHORES = 35
_SC_SEM_NSEMS_MAX = 36
_SC_SEM_VALUE_MAX = 37
_SC_SHARED_MEMORY_OBJECTS = 38
_SC_SIGQUEUE_MAX = 39
_SC_SIGRT_MIN = 40
_SC_SIGRT_MAX = 41
_SC_SYNCHRONIZED_IO = 42
_SC_TIMERS = 43
_SC_TIMER_MAX = 44
_SC_2_C_BIND = 45
_SC_2_C_DEV = 46
_SC_2_C_VERSION = 47
_SC_2_FORT_DEV = 48
_SC_2_FORT_RUN = 49
_SC_2_LOCALEDEF = 50
_SC_2_SW_DEV = 51
_SC_2_UPE = 52
_SC_2_VERSION = 53
_SC_BC_BASE_MAX = 54
_SC_BC_DIM_MAX = 55
_SC_BC_SCALE_MAX = 56
_SC_BC_STRING_MAX = 57
_SC_COLL_WEIGHTS_MAX = 58
_SC_EXPR_NEST_MAX = 59
_SC_LINE_MAX = 60
_SC_RE_DUP_MAX = 61
_SC_XOPEN_CRYPT = 62
_SC_XOPEN_ENH_I18N = 63
_SC_XOPEN_SHM = 64
_SC_2_CHAR_TERM = 66
_SC_XOPEN_XCU_VERSION = 67
_SC_ATEXIT_MAX = 76
_SC_IOV_MAX = 77
_SC_XOPEN_UNIX = 78
_SC_PAGE_SIZE = _SC_PAGESIZE
_SC_T_IOV_MAX = 79
_SC_PHYS_PAGES = 500
_SC_AVPHYS_PAGES = 501
_SC_COHER_BLKSZ = 503
_SC_SPLIT_CACHE = 504
_SC_ICACHE_SZ = 505
_SC_DCACHE_SZ = 506
_SC_ICACHE_LINESZ = 507
_SC_DCACHE_LINESZ = 508
_SC_ICACHE_BLKSZ = 509
_SC_DCACHE_BLKSZ = 510
_SC_DCACHE_TBLKSZ = 511
_SC_ICACHE_ASSOC = 512
_SC_DCACHE_ASSOC = 513
_SC_MAXPID = 514
_SC_STACK_PROT = 515
_SC_THREAD_DESTRUCTOR_ITERATIONS = 568
_SC_GETGR_R_SIZE_MAX = 569
_SC_GETPW_R_SIZE_MAX = 570
_SC_LOGIN_NAME_MAX = 571
_SC_THREAD_KEYS_MAX = 572
_SC_THREAD_STACK_MIN = 573
_SC_THREAD_THREADS_MAX = 574
_SC_TTY_NAME_MAX = 575
_SC_THREADS = 576
_SC_THREAD_ATTR_STACKADDR = 577
_SC_THREAD_ATTR_STACKSIZE = 578
_SC_THREAD_PRIORITY_SCHEDULING = 579
_SC_THREAD_PRIO_INHERIT = 580
_SC_THREAD_PRIO_PROTECT = 581
_SC_THREAD_PROCESS_SHARED = 582
_SC_THREAD_SAFE_FUNCTIONS = 583
_SC_XOPEN_LEGACY = 717
_SC_XOPEN_REALTIME = 718
_SC_XOPEN_REALTIME_THREADS = 719
_SC_XBS5_ILP32_OFF32 = 720
_SC_XBS5_ILP32_OFFBIG = 721
_SC_XBS5_LP64_OFF64 = 722
_SC_XBS5_LPBIG_OFFBIG = 723
_PC_LINK_MAX = 1
_PC_MAX_CANON = 2
_PC_MAX_INPUT = 3
_PC_NAME_MAX = 4
_PC_PATH_MAX = 5
_PC_PIPE_BUF = 6
_PC_NO_TRUNC = 7
_PC_VDISABLE = 8
_PC_CHOWN_RESTRICTED = 9
_PC_ASYNC_IO = 10
_PC_PRIO_IO = 11
_PC_SYNC_IO = 12
_PC_FILESIZEBITS = 67
_PC_LAST = 67
_POSIX_VERSION = 199506L
_POSIX2_VERSION = 199209L
_POSIX2_C_VERSION = 199209L
_XOPEN_XCU_VERSION = 4
_XOPEN_REALTIME = 1
_XOPEN_ENH_I18N = 1
_XOPEN_SHM = 1
_POSIX2_C_BIND = 1
_POSIX2_CHAR_TERM = 1
_POSIX2_LOCALEDEF = 1
_POSIX2_C_DEV = 1
_POSIX2_SW_DEV = 1
_POSIX2_UPE = 1
from TYPES import *

def MUTEX_HELD(x):
    return mutex_owned(x)


from TYPES import *

def RW_READ_HELD(x):
    return rw_read_held(x)


def RW_WRITE_HELD(x):
    return rw_write_held(x)


def RW_LOCK_HELD(x):
    return rw_lock_held(x)


def RW_ISWRITER(x):
    return rw_iswriter(x)


from TYPES import *
from TYPES import *
from TYPES import *
TIME32_MAX = INT32_MAX
TIME32_MIN = INT32_MIN

def TIMEVAL_OVERFLOW(tv):
    pass


from TYPES import *
DST_NONE = 0
DST_USA = 1
DST_AUST = 2
DST_WET = 3
DST_MET = 4
DST_EET = 5
DST_CAN = 6
DST_GB = 7
DST_RUM = 8
DST_TUR = 9
DST_AUSTALT = 10
ITIMER_REAL = 0
ITIMER_VIRTUAL = 1
ITIMER_PROF = 2
ITIMER_REALPROF = 3

def ITIMERVAL_OVERFLOW(itv):
    pass


SEC = 1
MILLISEC = 1000
MICROSEC = 1000000
NANOSEC = 1000000000

def TIMESPEC_OVERFLOW(ts):
    pass


def ITIMERSPEC_OVERFLOW(it):
    pass


__CLOCK_REALTIME0 = 0
CLOCK_VIRTUAL = 1
CLOCK_PROF = 2
__CLOCK_REALTIME3 = 3
CLOCK_HIGHRES = 4
CLOCK_MAX = 5
CLOCK_REALTIME = __CLOCK_REALTIME3
CLOCK_REALTIME = __CLOCK_REALTIME0
TIMER_RELTIME = 0
TIMER_ABSTIME = 1

def TICK_TO_SEC(tick):
    return tick / hz


def SEC_TO_TICK(sec):
    return sec * hz


def TICK_TO_MSEC(tick):
    pass


def MSEC_TO_TICK(msec):
    pass


def MSEC_TO_TICK_ROUNDUP(msec):
    pass


def TICK_TO_USEC(tick):
    return tick * usec_per_tick


def USEC_TO_TICK(usec):
    return usec / usec_per_tick


def USEC_TO_TICK_ROUNDUP(usec):
    pass


def TICK_TO_NSEC(tick):
    return tick * nsec_per_tick


def NSEC_TO_TICK(nsec):
    return nsec / nsec_per_tick


def NSEC_TO_TICK_ROUNDUP(nsec):
    pass


def TIMEVAL_TO_TICK(tvp):
    pass


def TIMESTRUC_TO_TICK(tsp):
    pass


from TYPES import *
NULL = 0L
NULL = 0
CLOCKS_PER_SEC = 1000000
FD_SETSIZE = 65536
FD_SETSIZE = 1024
_NBBY = 8
NBBY = _NBBY

def FD_ZERO(p):
    return bzero(p, sizeof(*p))


SIGHUP = 1
SIGINT = 2
SIGQUIT = 3
SIGILL = 4
SIGTRAP = 5
SIGIOT = 6
SIGABRT = 6
SIGEMT = 7
SIGFPE = 8
SIGKILL = 9
SIGBUS = 10
SIGSEGV = 11
SIGSYS = 12
SIGPIPE = 13
SIGALRM = 14
SIGTERM = 15
SIGUSR1 = 16
SIGUSR2 = 17
SIGCLD = 18
SIGCHLD = 18
SIGPWR = 19
SIGWINCH = 20
SIGURG = 21
SIGPOLL = 22
SIGIO = SIGPOLL
SIGSTOP = 23
SIGTSTP = 24
SIGCONT = 25
SIGTTIN = 26
SIGTTOU = 27
SIGVTALRM = 28
SIGPROF = 29
SIGXCPU = 30
SIGXFSZ = 31
SIGWAITING = 32
SIGLWP = 33
SIGFREEZE = 34
SIGTHAW = 35
SIGCANCEL = 36
SIGLOST = 37
_SIGRTMIN = 38
_SIGRTMAX = 45
SIG_BLOCK = 1
SIG_UNBLOCK = 2
SIG_SETMASK = 3
SIGNO_MASK = 255
SIGDEFER = 256
SIGHOLD = 512
SIGRELSE = 1024
SIGIGNORE = 2048
SIGPAUSE = 4096
from TYPES import *
SIGEV_NONE = 1
SIGEV_SIGNAL = 2
SIGEV_THREAD = 3
SI_NOINFO = 32767
SI_USER = 0
SI_LWP = -1
SI_QUEUE = -2
SI_TIMER = -3
SI_ASYNCIO = -4
SI_MESGQ = -5
ILL_ILLOPC = 1
ILL_ILLOPN = 2
ILL_ILLADR = 3
ILL_ILLTRP = 4
ILL_PRVOPC = 5
ILL_PRVREG = 6
ILL_COPROC = 7
ILL_BADSTK = 8
NSIGILL = 8
EMT_TAGOVF = 1
EMT_CPCOVF = 2
NSIGEMT = 2
FPE_INTDIV = 1
FPE_INTOVF = 2
FPE_FLTDIV = 3
FPE_FLTOVF = 4
FPE_FLTUND = 5
FPE_FLTRES = 6
FPE_FLTINV = 7
FPE_FLTSUB = 8
NSIGFPE = 8
SEGV_MAPERR = 1
SEGV_ACCERR = 2
NSIGSEGV = 2
BUS_ADRALN = 1
BUS_ADRERR = 2
BUS_OBJERR = 3
NSIGBUS = 3
TRAP_BRKPT = 1
TRAP_TRACE = 2
TRAP_RWATCH = 3
TRAP_WWATCH = 4
TRAP_XWATCH = 5
NSIGTRAP = 5
CLD_EXITED = 1
CLD_KILLED = 2
CLD_DUMPED = 3
CLD_TRAPPED = 4
CLD_STOPPED = 5
CLD_CONTINUED = 6
NSIGCLD = 6
POLL_IN = 1
POLL_OUT = 2
POLL_MSG = 3
POLL_ERR = 4
POLL_PRI = 5
POLL_HUP = 6
NSIGPOLL = 6
PROF_SIG = 1
NSIGPROF = 1
SI_MAXSZ = 256
SI_MAXSZ = 128
from TYPES import *
SI32_MAXSZ = 128

def SI_CANQUEUE(c):
    return c <= SI_QUEUE


SA_NOCLDSTOP = 131072
SA_ONSTACK = 1
SA_RESETHAND = 2
SA_RESTART = 4
SA_SIGINFO = 8
SA_NODEFER = 16
SA_NOCLDWAIT = 65536
SA_WAITSIG = 65536
NSIG = 46
MAXSIG = 45
S_SIGNAL = 1
S_SIGSET = 2
S_SIGACTION = 3
S_NONE = 4
MINSIGSTKSZ = 2048
SIGSTKSZ = 8192
SS_ONSTACK = 1
SS_DISABLE = 2
SN_PROC = 1
SN_CANCEL = 2
SN_SEND = 3
from TYPES import *
REG_CCR = 0
REG_PSR = 0
REG_PSR = 0
REG_PC = 1
REG_nPC = 2
REG_Y = 3
REG_G1 = 4
REG_G2 = 5
REG_G3 = 6
REG_G4 = 7
REG_G5 = 8
REG_G6 = 9
REG_G7 = 10
REG_O0 = 11
REG_O1 = 12
REG_O2 = 13
REG_O3 = 14
REG_O4 = 15
REG_O5 = 16
REG_O6 = 17
REG_O7 = 18
REG_ASI = 19
REG_FPRS = 20
REG_PS = REG_PSR
REG_SP = REG_O6
REG_R0 = REG_O0
REG_R1 = REG_O1
_NGREG = 21
_NGREG = 19
NGREG = _NGREG
_NGREG32 = 19
_NGREG64 = 21
SPARC_MAXREGWINDOW = 31
MAXFPQ = 16
XRS_ID = 2020766464
PSR_CWP = 31
PSR_ET = 32
PSR_PS = 64
PSR_S = 128
PSR_PIL = 3840
PSR_EF = 4096
PSR_EC = 8192
PSR_RSV = 1032192
PSR_ICC = 15728640
PSR_C = 1048576
PSR_V = 2097152
PSR_Z = 4194304
PSR_N = 8388608
PSR_VER = 251658240
PSR_IMPL = 4026531840L
PSL_ALLCC = PSR_ICC
PSL_USER = PSR_S
PSL_USERMASK = PSR_ICC
PSL_UBITS = PSR_ICC | PSR_EF

def USERMODE(ps):
    return ps & PSR_PS == 0


FSR_CEXC = 31
FSR_AEXC = 992
FSR_FCC = 3072
FSR_PR = 4096
FSR_QNE = 8192
FSR_FTT = 114688
FSR_VER = 917504
FSR_TEM = 260046848
FSR_RP = 805306368
FSR_RD = 3221225472L
FSR_VER_SHIFT = 17
FSR_FCC1 = 3
FSR_FCC2 = 12
FSR_FCC3 = 48
FSR_CEXC_NX = 1
FSR_CEXC_DZ = 2
FSR_CEXC_UF = 4
FSR_CEXC_OF = 8
FSR_CEXC_NV = 16
FSR_AEXC_NX = 32
FSR_AEXC_DZ = 64
FSR_AEXC_UF = 128
FSR_AEXC_OF = 256
FSR_AEXC_NV = 512
FTT_NONE = 0
FTT_IEEE = 1
FTT_UNFIN = 2
FTT_UNIMP = 3
FTT_SEQ = 4
FTT_ALIGN = 5
FTT_DFAULT = 6
FSR_FTT_SHIFT = 14
FSR_FTT_IEEE = FTT_IEEE << FSR_FTT_SHIFT
FSR_FTT_UNFIN = FTT_UNFIN << FSR_FTT_SHIFT
FSR_FTT_UNIMP = FTT_UNIMP << FSR_FTT_SHIFT
FSR_FTT_SEQ = FTT_SEQ << FSR_FTT_SHIFT
FSR_FTT_ALIGN = FTT_ALIGN << FSR_FTT_SHIFT
FSR_FTT_DFAULT = FTT_DFAULT << FSR_FTT_SHIFT
FSR_TEM_NX = 8388608
FSR_TEM_DZ = 16777216
FSR_TEM_UF = 33554432
FSR_TEM_OF = 67108864
FSR_TEM_NV = 134217728
RP_DBLEXT = 0
RP_SINGLE = 1
RP_DOUBLE = 2
RP_RESERVED = 3
RD_NEAR = 0
RD_ZER0 = 1
RD_POSINF = 2
RD_NEGINF = 3
FPRS_DL = 1
FPRS_DU = 2
FPRS_FEF = 4
PIL_MAX = 15

def SAVE_GLOBALS(RP):
    pass


def RESTORE_GLOBALS(RP):
    pass


def SAVE_OUTS(RP):
    pass


def RESTORE_OUTS(RP):
    pass


def SAVE_WINDOW(SBP):
    pass


def RESTORE_WINDOW(SBP):
    pass


def STORE_FPREGS(FP):
    pass


def LOAD_FPREGS(FP):
    pass


_SPARC_MAXREGWINDOW = 31
_XRS_ID = 2020766464
GETCONTEXT = 0
SETCONTEXT = 1
UC_SIGMASK = 1
UC_STACK = 2
UC_CPU = 4
UC_MAU = 8
UC_FPU = UC_MAU
UC_INTR = 16
UC_ASR = 32
UC_MCONTEXT = UC_CPU | UC_FPU | UC_ASR
UC_ALL = UC_SIGMASK | UC_STACK | UC_MCONTEXT
_SIGQUEUE_MAX = 32
_SIGNOTIFY_MAX = 32
INSTR_VALID = 2
NORMAL_STEP = 4
WATCH_STEP = 8
CPC_OVERFLOW = 16
ASYNC_HWERR = 32
STEP_NONE = 0
STEP_REQUESTED = 1
STEP_ACTIVE = 2
STEP_WASACTIVE = 3
LMS_USER = 0
LMS_SYSTEM = 1
LMS_TRAP = 2
LMS_TFAULT = 3
LMS_DFAULT = 4
LMS_KFAULT = 5
LMS_USER_LOCK = 6
LMS_SLEEP = 7
LMS_WAIT_CPU = 8
LMS_STOPPED = 9
NMSTATES = 10
from TYPES import *
USYNC_THREAD = 0
USYNC_PROCESS = 1
LOCK_NORMAL = 0
LOCK_ERRORCHECK = 2
LOCK_RECURSIVE = 4
USYNC_PROCESS_ROBUST = 8
LOCK_PRIO_NONE = 0
LOCK_PRIO_INHERIT = 16
LOCK_PRIO_PROTECT = 32
LOCK_STALL_NP = 0
LOCK_ROBUST_NP = 64
LOCK_OWNERDEAD = 1
LOCK_NOTRECOVERABLE = 2
LOCK_INITED = 4
LOCK_UNMAPPED = 8
LWP_DETACHED = 64
LWP_SUSPENDED = 128
__LWP_ASLWP = 256
MAXSYSARGS = 8
NORMALRETURN = 0
JUSTRETURN = 1
LWP_USER = 1
LWP_SYS = 2
TS_FREE = 0
TS_SLEEP = 1
TS_RUN = 2
TS_ONPROC = 4
TS_ZOMB = 8
TS_STOPPED = 16
T_INTR_THREAD = 1
T_WAKEABLE = 2
T_TOMASK = 4
T_TALLOCSTK = 8
T_WOULDBLOCK = 32
T_DONTBLOCK = 64
T_DONTPEND = 128
T_SYS_PROF = 256
T_WAITCVSEM = 512
T_WATCHPT = 1024
T_PANIC = 2048
TP_HOLDLWP = 2
TP_TWAIT = 4
TP_LWPEXIT = 8
TP_PRSTOP = 16
TP_CHKPT = 32
TP_EXITLWP = 64
TP_PRVSTOP = 128
TP_MSACCT = 256
TP_STOPPING = 512
TP_WATCHPT = 1024
TP_PAUSE = 2048
TP_CHANGEBIND = 4096
TS_LOAD = 1
TS_DONT_SWAP = 2
TS_SWAPENQ = 4
TS_ON_SWAPQ = 8
TS_CSTART = 256
TS_UNPAUSE = 512
TS_XSTART = 1024
TS_PSTART = 2048
TS_RESUME = 4096
TS_CREATE = 8192
TS_ALLSTART = TS_CSTART | TS_UNPAUSE | TS_XSTART | TS_PSTART | TS_RESUME | TS_CREATE

def CPR_VSTOPPED(t):
    pass


def THREAD_TRANSITION(tp):
    return thread_transition(tp)


def THREAD_STOP(tp):
    pass


def THREAD_ZOMB(tp):
    return THREAD_SET_STATE(tp, TS_ZOMB, NULL)


def SEMA_HELD(x):
    return sema_held(x)


NO_LOCKS_HELD = 1
NO_COMPETING_THREADS = 1
from TYPES import *
from TYPES import *
PRIO_PROCESS = 0
PRIO_PGRP = 1
PRIO_USER = 2
RLIMIT_CPU = 0
RLIMIT_FSIZE = 1
RLIMIT_DATA = 2
RLIMIT_STACK = 3
RLIMIT_CORE = 4
RLIMIT_NOFILE = 5
RLIMIT_VMEM = 6
RLIMIT_AS = RLIMIT_VMEM
RLIM_NLIMITS = 7
RLIM_INFINITY = -3L
RLIM_SAVED_MAX = -2L
RLIM_SAVED_CUR = -1L
RLIM_INFINITY = 2147483647
RLIM_SAVED_MAX = 2147483646
RLIM_SAVED_CUR = 2147483645
RLIM32_INFINITY = 2147483647
RLIM32_SAVED_MAX = 2147483646
RLIM32_SAVED_CUR = 2147483645

def ASSERT64(x):
    return ASSERT(x)


def ASSERT32(x):
    return ASSERT(x)


DATAMODEL_MASK = 267386880
DATAMODEL_ILP32 = 1048576
DATAMODEL_LP64 = 2097152
DATAMODEL_NONE = 0
DATAMODEL_NATIVE = DATAMODEL_LP64
DATAMODEL_NATIVE = DATAMODEL_ILP32

def STRUCT_SIZE(handle):
    pass


def STRUCT_BUF(handle):
    return handle.ptr.m64


def SIZEOF_PTR(umodel):
    pass


def STRUCT_SIZE(handle):
    return sizeof(*handle.ptr)


def STRUCT_BUF(handle):
    return handle.ptr


def SIZEOF_PTR(umodel):
    return sizeof(caddr_t)


def lwp_getdatamodel(t):
    return DATAMODEL_ILP32


RUSAGE_SELF = 0
RUSAGE_CHILDREN = -1
from TYPES import *
KSTAT_STRLEN = 31

def KSTAT_ENTER(k):
    pass


def KSTAT_EXIT(k):
    pass


KSTAT_TYPE_RAW = 0
KSTAT_TYPE_NAMED = 1
KSTAT_TYPE_INTR = 2
KSTAT_TYPE_IO = 3
KSTAT_TYPE_TIMER = 4
KSTAT_NUM_TYPES = 5
KSTAT_FLAG_VIRTUAL = 1
KSTAT_FLAG_VAR_SIZE = 2
KSTAT_FLAG_WRITABLE = 4
KSTAT_FLAG_PERSISTENT = 8
KSTAT_FLAG_DORMANT = 16
KSTAT_FLAG_INVALID = 32
KSTAT_READ = 0
KSTAT_WRITE = 1
KSTAT_DATA_CHAR = 0
KSTAT_DATA_INT32 = 1
KSTAT_DATA_UINT32 = 2
KSTAT_DATA_INT64 = 3
KSTAT_DATA_UINT64 = 4
KSTAT_DATA_LONG = KSTAT_DATA_INT32
KSTAT_DATA_ULONG = KSTAT_DATA_UINT32
KSTAT_DATA_LONG = KSTAT_DATA_INT64
KSTAT_DATA_ULONG = KSTAT_DATA_UINT64
KSTAT_DATA_LONG = 7
KSTAT_DATA_ULONG = 8
KSTAT_DATA_LONGLONG = KSTAT_DATA_INT64
KSTAT_DATA_ULONGLONG = KSTAT_DATA_UINT64
KSTAT_DATA_FLOAT = 5
KSTAT_DATA_DOUBLE = 6
KSTAT_INTR_HARD = 0
KSTAT_INTR_SOFT = 1
KSTAT_INTR_WATCHDOG = 2
KSTAT_INTR_SPURIOUS = 3
KSTAT_INTR_MULTSVC = 4
KSTAT_NUM_INTRS = 5
B_BUSY = 1
B_DONE = 2
B_ERROR = 4
B_PAGEIO = 16
B_PHYS = 32
B_READ = 64
B_WRITE = 256
B_KERNBUF = 8
B_WANTED = 128
B_AGE = 512
B_ASYNC = 1024
B_DELWRI = 2048
B_STALE = 4096
B_DONTNEED = 8192
B_REMAPPED = 16384
B_FREE = 32768
B_INVAL = 65536
B_FORCE = 131072
B_HEAD = 262144
B_NOCACHE = 524288
B_TRUNC = 1048576
B_SHADOW = 2097152
B_RETRYWRI = 4194304

def notavail(bp):
    pass


def BWRITE(bp):
    pass


def BWRITE2(bp):
    pass


VROOT = 1
VNOCACHE = 2
VNOMAP = 4
VDUP = 8
VNOSWAP = 16
VNOMOUNT = 32
VISSWAP = 64
VSWAPLIKE = 128
VVFSLOCK = 256
VVFSWAIT = 512
VVMLOCK = 1024
VDIROPEN = 2048
VVMEXEC = 4096
VPXFS = 8192
AT_TYPE = 1
AT_MODE = 2
AT_UID = 4
AT_GID = 8
AT_FSID = 16
AT_NODEID = 32
AT_NLINK = 64
AT_SIZE = 128
AT_ATIME = 256
AT_MTIME = 512
AT_CTIME = 1024
AT_RDEV = 2048
AT_BLKSIZE = 4096
AT_NBLOCKS = 8192
AT_VCODE = 16384
AT_ALL = AT_TYPE | AT_MODE | AT_UID | AT_GID | AT_FSID | AT_NODEID | AT_NLINK | AT_SIZE | AT_ATIME | AT_MTIME | AT_CTIME | AT_RDEV | AT_BLKSIZE | AT_NBLOCKS | AT_VCODE
AT_STAT = AT_MODE | AT_UID | AT_GID | AT_FSID | AT_NODEID | AT_NLINK | AT_SIZE | AT_ATIME | AT_MTIME | AT_CTIME | AT_RDEV
AT_TIMES = AT_ATIME | AT_MTIME | AT_CTIME
AT_NOSET = AT_NLINK | AT_RDEV | AT_FSID | AT_NODEID | AT_TYPE | AT_BLKSIZE | AT_NBLOCKS | AT_VCODE
VSUID = 2048
VSGID = 1024
VSVTX = 512
VREAD = 256
VWRITE = 128
VEXEC = 64
MODEMASK = 4095
PERMMASK = 511

def MANDMODE(mode):
    return mode & (VSGID | VEXEC >> 3) == VSGID


VSA_ACL = 1
VSA_ACLCNT = 2
VSA_DFACL = 4
VSA_DFACLCNT = 8
LOOKUP_DIR = 1
DUMP_ALLOC = 0
DUMP_FREE = 1
DUMP_SCAN = 2
ATTR_UTIME = 1
ATTR_EXEC = 2
ATTR_COMM = 4
ATTR_HINT = 8
ATTR_REAL = 16
POLLIN = 1
POLLPRI = 2
POLLOUT = 4
POLLRDNORM = 64
POLLWRNORM = POLLOUT
POLLRDBAND = 128
POLLWRBAND = 256
POLLNORM = POLLRDNORM
POLLERR = 8
POLLHUP = 16
POLLNVAL = 32
POLLREMOVE = 2048
POLLRDDATA = 512
POLLNOERR = 1024
POLLCLOSED = 32768

def str_aligned(X):
    return ulong_t(X) & sizeof(long) - 1 == 0


tdelta_t_sz = 12
FTEV_MASK = 8191
FTEV_ISWR = 32768
FTEV_CS = 16384
FTEV_PS = 8192
FTEV_QMASK = 7936
FTEV_ALLOCMASK = 8184
FTEV_ALLOCB = 0
FTEV_ESBALLOC = 1
FTEV_DESBALLOC = 2
FTEV_ESBALLOCA = 3
FTEV_DESBALLOCA = 4
FTEV_ALLOCBIG = 5
FTEV_ALLOCBW = 6
FTEV_FREEB = 8
FTEV_DUPB = 9
FTEV_COPYB = 10
FTEV_CALLER = 15
FTEV_PUT = 256
FTEV_FSYNCQ = 259
FTEV_DSYNCQ = 260
FTEV_PUTQ = 261
FTEV_GETQ = 262
FTEV_RMVQ = 263
FTEV_INSQ = 264
FTEV_PUTBQ = 265
FTEV_FLUSHQ = 266
FTEV_REPLYQ = 267
FTEV_PUTNEXT = 269
FTEV_RWNEXT = 270
FTEV_QWINNER = 271
FTEV_GEWRITE = 257

def FTFLW_HASH(h):
    return unsigned(h) % ftflw_hash_sz


FTBLK_EVNTS = 9
QENAB = 1
QWANTR = 2
QWANTW = 4
QFULL = 8
QREADR = 16
QUSE = 32
QNOENB = 64
QBACK = 256
QHLIST = 512
QPAIR = 2048
QPERQ = 4096
QPERMOD = 8192
QMTSAFE = 16384
QMTOUTPERIM = 32768
QMT_TYPEMASK = QPAIR | QPERQ | QPERMOD | QMTSAFE | QMTOUTPERIM
QINSERVICE = 65536
QWCLOSE = 131072
QEND = 262144
QWANTWSYNC = 524288
QSYNCSTR = 1048576
QISDRV = 2097152
QHOT = 4194304
QNEXTHOT = 8388608
_QINSERTING = 67108864
_QREMOVING = 134217728
Q_SQQUEUED = 1
Q_SQDRAINING = 2
QB_FULL = 1
QB_WANTW = 2
QB_BACK = 4
NBAND = 256
STRUIOT_NONE = -1
STRUIOT_DONTCARE = 0
STRUIOT_STANDARD = 1
STRUIOT_IP = 2
DBLK_REFMIN = 1
STRUIO_SPEC = 1
STRUIO_DONE = 2
STRUIO_IP = 4
STRUIO_ZC = 8
STRUIO_ICK = 16
MSGMARK = 1
MSGNOLOOP = 2
MSGDELIM = 4
MSGNOGET = 8
MSGMARKNEXT = 16
MSGNOTMARKNEXT = 32
M_DATA = 0
M_PROTO = 1
M_BREAK = 8
M_PASSFP = 9
M_EVENT = 10
M_SIG = 11
M_DELAY = 12
M_CTL = 13
M_IOCTL = 14
M_SETOPTS = 16
M_RSE = 17
M_IOCACK = 129
M_IOCNAK = 130
M_PCPROTO = 131
M_PCSIG = 132
M_READ = 133
M_FLUSH = 134
M_STOP = 135
M_START = 136
M_HANGUP = 137
M_ERROR = 138
M_COPYIN = 139
M_COPYOUT = 140
M_IOCDATA = 141
M_PCRSE = 142
M_STOPI = 143
M_STARTI = 144
M_PCEVENT = 145
M_UNHANGUP = 146
QNORM = 0
QPCTL = 128
IOC_MODELS = DATAMODEL_MASK
IOC_ILP32 = DATAMODEL_ILP32
IOC_LP64 = DATAMODEL_LP64
IOC_NATIVE = DATAMODEL_NATIVE
IOC_NONE = DATAMODEL_NONE
STRCANON = 1
RECOPY = 2
SO_ALL = 63
SO_READOPT = 1
SO_WROFF = 2
SO_MINPSZ = 4
SO_MAXPSZ = 8
SO_HIWAT = 16
SO_LOWAT = 32
SO_MREADON = 64
SO_MREADOFF = 128
SO_NDELON = 256
SO_NDELOFF = 512
SO_ISTTY = 1024
SO_ISNTTY = 2048
SO_TOSTOP = 4096
SO_TONSTOP = 8192
SO_BAND = 16384
SO_DELIM = 32768
SO_NODELIM = 65536
SO_STRHOLD = 131072
SO_ERROPT = 262144
SO_COPYOPT = 524288
SO_MAXBLK = 1048576
DEF_IOV_MAX = 16
INFOD_FIRSTBYTES = 2
INFOD_BYTES = 4
INFOD_COUNT = 8
INFOD_COPYOUT = 16
MODOPEN = 1
CLONEOPEN = 2
CONSOPEN = 4
OPENFAIL = -1
BPRI_LO = 1
BPRI_MED = 2
BPRI_HI = 3
BPRI_FT = 4
INFPSZ = -1
FLUSHALL = 1
FLUSHDATA = 0
STRHIGH = 5120
STRLOW = 1024
MAXIOCBSZ = 1024
PERIM_INNER = 1
PERIM_OUTER = 2

def datamsg(type):
    pass


def straln(a):
    return caddr_t(intptr_t(a) & ~(sizeof(int) - 1))


def ntohl(x):
    return x


def ntohs(x):
    return x


def htonl(x):
    return x


def htons(x):
    return x


IPPROTO_IP = 0
IPPROTO_HOPOPTS = 0
IPPROTO_ICMP = 1
IPPROTO_IGMP = 2
IPPROTO_GGP = 3
IPPROTO_ENCAP = 4
IPPROTO_TCP = 6
IPPROTO_EGP = 8
IPPROTO_PUP = 12
IPPROTO_UDP = 17
IPPROTO_IDP = 22
IPPROTO_IPV6 = 41
IPPROTO_ROUTING = 43
IPPROTO_FRAGMENT = 44
IPPROTO_RSVP = 46
IPPROTO_ESP = 50
IPPROTO_AH = 51
IPPROTO_ICMPV6 = 58
IPPROTO_NONE = 59
IPPROTO_DSTOPTS = 60
IPPROTO_HELLO = 63
IPPROTO_ND = 77
IPPROTO_EON = 80
IPPROTO_PIM = 103
IPPROTO_RAW = 255
IPPROTO_MAX = 256
IPPORT_ECHO = 7
IPPORT_DISCARD = 9
IPPORT_SYSTAT = 11
IPPORT_DAYTIME = 13
IPPORT_NETSTAT = 15
IPPORT_FTP = 21
IPPORT_TELNET = 23
IPPORT_SMTP = 25
IPPORT_TIMESERVER = 37
IPPORT_NAMESERVER = 42
IPPORT_WHOIS = 43
IPPORT_MTP = 57
IPPORT_BOOTPS = 67
IPPORT_BOOTPC = 68
IPPORT_TFTP = 69
IPPORT_RJE = 77
IPPORT_FINGER = 79
IPPORT_TTYLINK = 87
IPPORT_SUPDUP = 95
IPPORT_EXECSERVER = 512
IPPORT_LOGINSERVER = 513
IPPORT_CMDSERVER = 514
IPPORT_EFSSERVER = 520
IPPORT_BIFFUDP = 512
IPPORT_WHOSERVER = 513
IPPORT_ROUTESERVER = 520
IPPORT_RESERVED = 1024
IPPORT_USERRESERVED = 5000
IMPLINK_IP = 155
IMPLINK_LOWEXPER = 156
IMPLINK_HIGHEXPER = 158
IN_CLASSA_NSHIFT = 24
IN_CLASSA_MAX = 128
IN_CLASSB_NSHIFT = 16
IN_CLASSB_MAX = 65536
IN_CLASSC_NSHIFT = 8
IN_CLASSD_NSHIFT = 28

def IN_MULTICAST(i):
    return IN_CLASSD(i)


IN_LOOPBACKNET = 127

def IN_SET_LOOPBACK_ADDR(a):
    pass


def IN6_IS_ADDR_UNSPECIFIED(addr):
    pass


def IN6_IS_ADDR_LOOPBACK(addr):
    pass


def IN6_IS_ADDR_LOOPBACK(addr):
    pass


def IN6_IS_ADDR_MULTICAST(addr):
    pass


def IN6_IS_ADDR_MULTICAST(addr):
    pass


def IN6_IS_ADDR_LINKLOCAL(addr):
    pass


def IN6_IS_ADDR_LINKLOCAL(addr):
    pass


def IN6_IS_ADDR_SITELOCAL(addr):
    pass


def IN6_IS_ADDR_SITELOCAL(addr):
    pass


def IN6_IS_ADDR_V4MAPPED(addr):
    pass


def IN6_IS_ADDR_V4MAPPED(addr):
    pass


def IN6_IS_ADDR_V4MAPPED_ANY(addr):
    pass


def IN6_IS_ADDR_V4MAPPED_ANY(addr):
    pass


def IN6_IS_ADDR_V4COMPAT(addr):
    pass


def IN6_IS_ADDR_V4COMPAT(addr):
    pass


def IN6_IS_ADDR_MC_RESERVED(addr):
    pass


def IN6_IS_ADDR_MC_RESERVED(addr):
    pass


def IN6_IS_ADDR_MC_NODELOCAL(addr):
    pass


def IN6_IS_ADDR_MC_NODELOCAL(addr):
    pass


def IN6_IS_ADDR_MC_LINKLOCAL(addr):
    pass


def IN6_IS_ADDR_MC_LINKLOCAL(addr):
    pass


def IN6_IS_ADDR_MC_SITELOCAL(addr):
    pass


def IN6_IS_ADDR_MC_SITELOCAL(addr):
    pass


def IN6_IS_ADDR_MC_ORGLOCAL(addr):
    pass


def IN6_IS_ADDR_MC_ORGLOCAL(addr):
    pass


def IN6_IS_ADDR_MC_GLOBAL(addr):
    pass


def IN6_IS_ADDR_MC_GLOBAL(addr):
    pass


IP_OPTIONS = 1
IP_HDRINCL = 2
IP_TOS = 3
IP_TTL = 4
IP_RECVOPTS = 5
IP_RECVRETOPTS = 6
IP_RECVDSTADDR = 7
IP_RETOPTS = 8
IP_MULTICAST_IF = 16
IP_MULTICAST_TTL = 17
IP_MULTICAST_LOOP = 18
IP_ADD_MEMBERSHIP = 19
IP_DROP_MEMBERSHIP = 20
IP_SEC_OPT = 34
IPSEC_PREF_NEVER = 1
IPSEC_PREF_REQUIRED = 2
IPSEC_PREF_UNIQUE = 4
IP_ADD_PROXY_ADDR = 64
IP_BOUND_IF = 65
IP_UNSPEC_SRC = 66
IP_REUSEADDR = 260
IP_DONTROUTE = 261
IP_BROADCAST = 262
IP_DEFAULT_MULTICAST_TTL = 1
IP_DEFAULT_MULTICAST_LOOP = 1
IPV6_RTHDR_TYPE_0 = 0
IPV6_UNICAST_HOPS = 5
IPV6_MULTICAST_IF = 6
IPV6_MULTICAST_HOPS = 7
IPV6_MULTICAST_LOOP = 8
IPV6_JOIN_GROUP = 9
IPV6_LEAVE_GROUP = 10
IPV6_ADD_MEMBERSHIP = 9
IPV6_DROP_MEMBERSHIP = 10
IPV6_PKTINFO = 11
IPV6_HOPLIMIT = 12
IPV6_NEXTHOP = 13
IPV6_HOPOPTS = 14
IPV6_DSTOPTS = 15
IPV6_RTHDR = 16
IPV6_RTHDRDSTOPTS = 17
IPV6_RECVPKTINFO = 18
IPV6_RECVHOPLIMIT = 19
IPV6_RECVHOPOPTS = 20
IPV6_RECVDSTOPTS = 21
IPV6_RECVRTHDR = 22
IPV6_RECVRTHDRDSTOPTS = 23
IPV6_CHECKSUM = 24
IPV6_BOUND_IF = 65
IPV6_UNSPEC_SRC = 66
INET_ADDRSTRLEN = 16
INET6_ADDRSTRLEN = 46
IPV6_PAD1_OPT = 0
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\plat-sunos5\in.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:38:23 St�edn� Evropa (b�n� �as)