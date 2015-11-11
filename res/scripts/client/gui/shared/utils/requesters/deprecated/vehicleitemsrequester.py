# 2015.11.10 21:29:47 Støední Evropa (bìžný èas)
# Embedded file name: scripts/client/gui/shared/utils/requesters/deprecated/VehicleItemsRequester.py
from gui.shared.utils.gui_items import VehicleItem

class VehicleItemsRequester(object):

    def __init__(self, vehicles):
        self.__vehicles = vehicles

    def getItems(self, types):
        items = {}
        for v in self.__vehicles:
            for type in types:
                currents = self.__getItemsByType(v, type)
                for current in currents:
                    if current:
                        current = items.setdefault(current, VehicleItem(compactDescr=current))
                        current.count += 1
                        current.vehicles.append(v)

        return items.values()

    def __getItemsByType(self, v, itemTypeName):
        vd = v.descriptor
        if itemTypeName == 'vehicleChassis':
            return [vd.chassis['compactDescr']]
        if itemTypeName == 'vehicleEngine':
            return [vd.engine['compactDescr']]
        if itemTypeName == 'vehicleRadio':
            return [vd.radio['compactDescr']]
        if itemTypeName == 'vehicleFuelTank':
            return [vd.fuelTank['compactDescr']]
        if itemTypeName == 'vehicleTurret':
            if v.hasTurrets:
                return [vd.turret['compactDescr']]
        if itemTypeName == 'vehicleGun':
            return [vd.gun['compactDescr']]
        if itemTypeName == 'optionalDevice':
            return [ od['compactDescr'] for od in vd.optionalDevices if od ]
        if itemTypeName == 'equipment':
            return v.equipments
        return []
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\shared\utils\requesters\deprecated\vehicleitemsrequester.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:29:47 Støední Evropa (bìžný èas)
