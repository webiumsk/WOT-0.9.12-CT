# 2015.11.10 21:35:48 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/encodings/euc_kr.py
import _codecs_kr, codecs
import _multibytecodec as mbc
codec = _codecs_kr.getcodec('euc_kr')

class Codec(codecs.Codec):
    encode = codec.encode
    decode = codec.decode


class IncrementalEncoder(mbc.MultibyteIncrementalEncoder, codecs.IncrementalEncoder):
    codec = codec


class IncrementalDecoder(mbc.MultibyteIncrementalDecoder, codecs.IncrementalDecoder):
    codec = codec


class StreamReader(Codec, mbc.MultibyteStreamReader, codecs.StreamReader):
    codec = codec


class StreamWriter(Codec, mbc.MultibyteStreamWriter, codecs.StreamWriter):
    codec = codec


def getregentry():
    return codecs.CodecInfo(name='euc_kr', encode=Codec().encode, decode=Codec().decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamreader=StreamReader, streamwriter=StreamWriter)
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\encodings\euc_kr.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:35:48 St�edn� Evropa (b�n� �as)
