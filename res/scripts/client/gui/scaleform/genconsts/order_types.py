# 2015.11.10 21:28:19 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/client/gui/Scaleform/genConsts/ORDER_TYPES.py


class ORDER_TYPES(object):
    REQUISITION = 'requisition'
    EVACUATION = 'evacuation'
    HEAVY_TRUCKS = 'heavyTrucks'
    MILITARY_MANEUVERS = 'militaryManeuvers'
    ADDITIONAL_BRIEFING = 'additionalBriefing'
    TACTICAL_TRAINING = 'tacticalTraining'
    BATTLE_PAYMENTS = 'battlePayments'
    SPECIAL_MISSION = 'specialMission'
    ARTILLERY = 'artillery'
    BOMBER = 'bomber'
    EMPTY_ORDER = 'emptyOrder'
    FORT_CONSUMABLES_ACTIVE_TYPE = [ARTILLERY, BOMBER]
    FORT_CONSUMABLES_ORDER_GROUP = [FORT_CONSUMABLES_ACTIVE_TYPE]
    FORT_GENERAL_ACTIVE_TYPE = [HEAVY_TRUCKS,
     MILITARY_MANEUVERS,
     ADDITIONAL_BRIEFING,
     TACTICAL_TRAINING,
     BATTLE_PAYMENTS,
     SPECIAL_MISSION]
    FORT_GENERAL_PASSIVE_TYPE = [REQUISITION, EVACUATION]
    FORT_GENERAL_ORDER_GROUP = [FORT_GENERAL_PASSIVE_TYPE, FORT_GENERAL_ACTIVE_TYPE]
    FORT_ORDER_ALL_GROUP = 0
    FORT_ORDER_GENERAL_GROUP = 1
    FORT_ORDER_CONSUMABLES_GROUP = 2
    FORT_ORDER_GENERAL_ACTIVE_TYPE = 1
    FORT_ORDER_GENERAL_PASSIVE_TYPE = 2
    FORT_ORDER_CONSUMABLES_ACTIVE_TYPE = 3
    FORT_ORDER_CONSUMABLES_PASSIVE_TYPE = 4
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\scaleform\genconsts\order_types.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:28:19 St�edn� Evropa (b�n� �as)
