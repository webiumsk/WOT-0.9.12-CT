# 2015.11.10 21:35:34 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/email/mime/message.py
"""Class representing message/* MIME documents."""
__all__ = ['MIMEMessage']
from email import message
from email.mime.nonmultipart import MIMENonMultipart

class MIMEMessage(MIMENonMultipart):
    """Class representing message/* MIME documents."""

    def __init__(self, _msg, _subtype = 'rfc822'):
        """Create a message/* type MIME document.
        
        _msg is a message object and must be an instance of Message, or a
        derived class of Message, otherwise a TypeError is raised.
        
        Optional _subtype defines the subtype of the contained message.  The
        default is "rfc822" (this is defined by the MIME standard, even though
        the term "rfc822" is technically outdated by RFC 2822).
        """
        MIMENonMultipart.__init__(self, 'message', _subtype)
        if not isinstance(_msg, message.Message):
            raise TypeError('Argument is not an instance of Message')
        message.Message.attach(self, _msg)
        self.set_default_type('message/rfc822')
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\email\mime\message.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:35:34 St�edn� Evropa (b�n� �as)
