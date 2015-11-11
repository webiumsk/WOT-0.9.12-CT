# 2015.11.10 21:30:45 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/client/messenger/proto/xmpp/extensions/contact_item.py
from messenger.proto.xmpp.extensions import PyExtension
from messenger.proto.xmpp.extensions.ext_constants import XML_TAG_NAME as _TAG
from messenger.proto.xmpp.extensions.wg_items import WgSharedExtension
from messenger.proto.xmpp.jid import ContactJID

class ContactItemExtension(PyExtension):

    def __init__(self, jid = None):
        super(ContactItemExtension, self).__init__(_TAG.ITEM)
        if jid:
            self.setAttribute('jid', str(jid))
        self.setChild(WgSharedExtension())

    @classmethod
    def getDefaultData(cls):
        return (None, WgSharedExtension.getDefaultData())

    def parseTag(self, pyGlooxTag):
        jid = pyGlooxTag.findAttribute('jid')
        if jid:
            jid = ContactJID(jid)
        else:
            jid = None
        info = self._getChildData(pyGlooxTag, 0, WgSharedExtension.getDefaultData())
        return (jid, info)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\messenger\proto\xmpp\extensions\contact_item.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:30:45 St�edn� Evropa (b�n� �as)