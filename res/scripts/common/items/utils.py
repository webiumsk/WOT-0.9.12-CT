# 2015.11.10 21:32:03 Støední Evropa (bìžný èas)
# Embedded file name: scripts/common/items/utils.py
from VehicleDescrCrew import VehicleDescrCrew

def updateVehicleAttrFactors(vehicleDescr, crewCompactDescrs, eqs, factors):
    crewLevelIncrease = vehicleDescr.miscAttrs['crewLevelIncrease'] + sumCrewLevelIncrease(eqs)
    factors['crewLevelIncrease'] = crewLevelIncrease
    vehicleDescrCrew = VehicleDescrCrew(vehicleDescr, crewCompactDescrs)
    vehicleDescrCrew.onCollectFactors(factors)
    for eq in eqs:
        if eq is not None:
            eq.updateVehicleAttrFactors(factors)

    return


def sumCrewLevelIncrease(eqs):
    crewLevelIncrease = 0
    for eq in eqs:
        if eq and hasattr(eq, 'crewLevelIncrease'):
            crewLevelIncrease += eq.crewLevelIncrease

    return crewLevelIncrease
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\common\items\utils.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:32:03 Støední Evropa (bìžný èas)
