# 2015.11.10 21:26:13 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/BattleResultsWindow.py
from collections import defaultdict
import re
import math
import operator
from functools import partial
import BigWorld
from gui.LobbyContext import g_lobbyContext
from gui.Scaleform.locale.MENU import MENU
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.battle_control.arena_info import getArenaIcon, hasResourcePoints
from gui.battle_results.VehicleProgressCache import g_vehicleProgressCache
from gui.battle_results.VehicleProgressHelper import VehicleProgressHelper, PROGRESS_ACTION
from gui.shared.event_dispatcher import showResearchView, showPersonalCase, showBattleResultsFromData
from gui.shared.notifications import NotificationPriorityLevel
from gui.shared.utils.functions import getArenaSubTypeName
from gui.Scaleform.daapi.view.fallout_info_panel_helper import getCosts
import nations
import potapov_quests
from account_helpers.AccountSettings import AccountSettings
from account_helpers import getAccountDatabaseID
from account_shared import getFairPlayViolationName
from debug_utils import LOG_DEBUG
from helpers import i18n, time_utils
from adisp import async, process
from CurrentVehicle import g_currentVehicle
from constants import ARENA_BONUS_TYPE, IS_DEVELOPMENT, ARENA_GUI_TYPE, IGR_TYPE, EVENT_TYPE, FINISH_REASON as FR, FLAG_ACTION, TEAMS_IN_ARENA
from dossiers2.custom.records import RECORD_DB_IDS, DB_ID_TO_RECORD
from dossiers2.ui import achievements
from dossiers2.ui.achievements import ACHIEVEMENT_TYPE, MARK_ON_GUN_RECORD, MARK_OF_MASTERY_RECORD
from dossiers2.ui.layouts import IGNORED_BY_BATTLE_RESULTS, isAchievementRegistered
from gui import makeHtmlString, GUI_SETTINGS, SystemMessages
from gui.server_events import g_eventsCache, events_dispatcher as quests_events
from gui.shared import g_itemsCache, events
from gui.shared.utils import isVehicleObserver
from items import vehicles as vehicles_core, vehicles
from items.vehicles import VEHICLE_CLASS_TAGS
from shared_utils import findFirst
from gui.clubs import events_dispatcher as club_events
from gui.clubs.club_helpers import ClubListener
from gui.clubs.settings import getLeagueByDivision, getDivisionWithinLeague
from gui.shared.ClanCache import g_clanCache
from gui.shared.fortifications.FortBuilding import FortBuilding
from gui.shared.gui_items.dossier import getAchievementFactory
from gui.shared.gui_items.Vehicle import VEHICLE_BATTLE_TYPES_ORDER_INDICES
from gui.shared.gui_items.dossier.achievements.MarkOnGunAchievement import MarkOnGunAchievement
from gui.Scaleform.locale.BATTLE_RESULTS import BATTLE_RESULTS
from gui.Scaleform.daapi.view.meta.BattleResultsMeta import BattleResultsMeta
from messenger.storage import storage_getter
from gui.Scaleform.genConsts.CYBER_SPORT_ALIASES import CYBER_SPORT_ALIASES
from gui.Scaleform.locale.CYBERSPORT import CYBERSPORT
from gui.shared.formatters import text_styles
from gui.battle_results import formatters as battle_res_fmts

def _wrapEmblemUrl(emblemUrl):
    return ' <IMG SRC="img://%s" width="24" height="24" vspace="-10"/>' % emblemUrl


RESULT_ = '#menu:finalStatistic/commonStats/resultlabel/{0}'
BATTLE_RESULTS_STR = '#battle_results:{0}'
FINISH_REASON = BATTLE_RESULTS_STR.format('finish/reason/{0}')
CLAN_BATTLE_FINISH_REASON_DEF = BATTLE_RESULTS_STR.format('finish/clanBattle_reason_def/{0}')
CLAN_BATTLE_FINISH_REASON_ATTACK = BATTLE_RESULTS_STR.format('finish/clanBattle_reason_attack/{0}')
RESULT_LINE_STR = BATTLE_RESULTS_STR.format('details/calculations/{0}')
STATS_KEY_BASE = BATTLE_RESULTS_STR.format('team/stats/labels_{0}')
TIME_STATS_KEY_BASE = BATTLE_RESULTS_STR.format('details/time/lbl_{0}')
XP_TITLE = BATTLE_RESULTS_STR.format('common/details/xpTitle')
XP_TITLE_DAILY = BATTLE_RESULTS_STR.format('common/details/xpTitleFirstVictory')
MILEAGE_STR_KEY = BATTLE_RESULTS_STR.format('team/stats/mileage')
TIME_DURATION_STR = BATTLE_RESULTS_STR.format('details/time/value')
XP_MULTIPLIER_SIGN_KEY = BATTLE_RESULTS_STR.format('common/xpMultiplierSign')
EFFICIENCY_ALLIES_STR = BATTLE_RESULTS_STR.format('common/battleEfficiency/allies')
UNKNOWN_PLAYER_NAME_VALUE = '#ingame_gui:players_panel/unknown_name'
UNKNOWN_VEHICLE_NAME_VALUE = '#ingame_gui:players_panel/unknown_vehicle'
ARENA_TYPE = '#arenas:type/{0}/name'
ARENA_SPECIAL_TYPE = '#menu:loading/battleTypes/{0}'
VEHICLE_ICON_FILE = '../maps/icons/vehicle/{0}.png'
VEHICLE_ICON_FALLOUT_FILE = '../maps/icons/vehicle/falloutBattleResults/{0}.png'
VEHICLE_ICON_SMALL_FILE = '../maps/icons/vehicle/small/{0}.png'
VEHICLE_NO_IMAGE_FILE_NAME = 'noImage'
ARENA_SCREEN_FILE = '../maps/icons/map/stats/%s.png'
ARENA_NAME_PATTERN = '{0} - {1}'
LINE_BRAKE_STR = '<br/>'
STATS_KEYS = (('shots', True, None),
 ('hits', False, None),
 ('explosionHits', True, None),
 ('damageDealt', True, None),
 ('damageDealtByOrder', True, None),
 ('sniperDamageDealt', True, None),
 ('directHitsReceived', True, None),
 ('piercingsReceived', True, None),
 ('noDamageDirectHitsReceived', True, None),
 ('explosionHitsReceived', True, None),
 ('damageBlockedByArmor', True, None),
 ('teamHitsDamage', False, None),
 ('spotted', True, None),
 ('damagedKilled', False, None),
 ('killed', True, None),
 ('killsByOrder', True, None),
 ('damageAssisted', True, 'damageAssistedSelf'),
 ('capturePointsVal', False, None),
 ('mileage', False, None),
 ('flags', True, None),
 ('deaths', True, None))
TIME_STATS_KEYS = ('arenaCreateTimeOnlyStr', 'duration', 'playerKilled')
FALLOUT_ONLY_STATS = ('killed', 'killsByOrder', 'damageDealtByOrder', 'flags', 'deaths')
FALLOUT_ORDER_STATS = ('damageDealtByOrder', 'killsByOrder')
FALLOUT_EXCLUDE_VEHICLE_STATS = ('damagedKilled', 'sniperDamageDealt', 'capturePoints', 'droppedCapturePoints', 'capturePointsVal', 'mileage')

def _intSum(a, b):
    return a + b


def _intMax(a, b):
    return max(a, b)


def _listSum(a, b):
    return map(operator.add, a, b)


def _listCollect(a, b):
    return tuple(a) + tuple(b)


def _calculateDailyXP(oritinalData, data):
    return (data['originalXP'] - int(data.get('xpPenaltyBase', 0))) * data['dailyXPFactor10'] / 10.0


def _calculateDailyFreeXP(oritinalData, data):
    return data['originalFreeXP'] * data['dailyXPFactor10'] / 10.0


def _calculateBaseXpPenalty(originalData, data):
    aogasFactor = originalData.get('aogasFactor10', 10) / 10.0
    if not aogasFactor:
        return 0
    isPremium = originalData.get('isPremium', False)
    igrXpFactor = originalData.get('igrXPFactor10', 10) / 10.0
    premXpFactor = originalData.get('premiumXPFactor10', 10) / 10.0
    dailyXpFactor = originalData.get('dailyXPFactor10', 10) / 10.0
    xpPenalty = data['xpPenalty']
    xpPenalty = math.ceil(int(xpPenalty / aogasFactor) / dailyXpFactor)
    if isPremium:
        xpPenalty = math.ceil(xpPenalty / premXpFactor)
    if igrXpFactor:
        xpPenalty = math.ceil(xpPenalty / igrXpFactor)
    return xpPenalty


RELATED_ACCOUNT_DATA = {'dailyXP': _calculateDailyXP,
 'dailyFreeXP': _calculateDailyFreeXP,
 'xpPenaltyBase': _calculateBaseXpPenalty}
CUMULATIVE_ACCOUNT_DATA = (('credits', (0, _intSum)),
 ('achievementCredits', (0, _intSum)),
 ('creditsContributionIn', (0, _intSum)),
 ('creditsToDraw', (0, _intSum)),
 ('creditsPenalty', (0, _intSum)),
 ('creditsContributionOut', (0, _intSum)),
 ('originalCredits', (0, _intSum)),
 ('eventCredits', (0, _intSum)),
 ('eventGold', (0, _intSum)),
 ('orderCredits', (0, _intSum)),
 ('boosterCredits', (0, _intSum)),
 ('autoRepairCost', (0, _intSum)),
 ('autoLoadCost', ((0, 0), _listSum)),
 ('autoEquipCost', ((0, 0), _listSum)),
 ('histAmmoCost', ((0, 0), _listSum)),
 ('xp', (0, _intSum)),
 ('freeXP', (0, _intSum)),
 ('achievementXP', (0, _intSum)),
 ('achievementFreeXP', (0, _intSum)),
 ('xpPenalty', (0, _intSum)),
 ('originalXP', (0, _intSum)),
 ('originalFreeXP', (0, _intSum)),
 ('dossierPopUps', ((), _listCollect)),
 ('orderXP', (0, _intSum)),
 ('boosterXP', (0, _intSum)),
 ('orderFreeXP', (0, _intSum)),
 ('boosterFreeXP', (0, _intSum)),
 ('eventXP', (0, _intSum)),
 ('eventFreeXP', (0, _intSum)),
 ('premiumVehicleXP', (0, _intSum)),
 ('dailyXPFactor10', (10, _intMax)),
 ('xpPenaltyBase', (0, _intSum)),
 ('dailyXP', (0, _intSum)),
 ('dailyFreeXP', (0, _intSum)))
CUMULATIVE_STATS_DATA = {'shots': (0, _intSum),
 'tkills': (0, _intSum),
 'damageDealt': (0, _intSum),
 'sniperDamageDealt': (0, _intSum),
 'tdamageDealt': (0, _intSum),
 'directHits': (0, _intSum),
 'explosionHits': (0, _intSum),
 'piercings': (0, _intSum),
 'directHitsReceived': (0, _intSum),
 'piercingsReceived': (0, _intSum),
 'noDamageDirectHitsReceived': (0, _intSum),
 'explosionHitsReceived': (0, _intSum),
 'damageBlockedByArmor': (0, _intSum),
 'damaged': (0, _intSum),
 'kills': (0, _intSum),
 'capturePoints': (0, _intSum),
 'droppedCapturePoints': (0, _intSum),
 'mileage': (0, _intSum),
 'flagActions': ([0] * len(FLAG_ACTION.RANGE), _listSum),
 'deathCount': (0, _intSum),
 'winPoints': (0, _intSum),
 'resourceAbsorbed': (0, _intSum),
 'damageAssistedTrack': (0, _intSum),
 'damageAssistedRadio': (0, _intSum),
 'spotted': (0, _intSum)}

class BattleResultsWindow(BattleResultsMeta, ClubListener):
    RESEARCH_UNLOCK_TYPE = 'UNLOCK_LINK_TYPE'
    PURCHASE_UNLOCK_TYPE = 'PURCHASE_LINK_TYPE'
    NEW_SKILL_UNLOCK_TYPE = 'NEW_SKILL_LINK_TYPE'
    __playersNameCache = dict()
    __rated7x7Animations = set()
    __buyPremiumCache = set()

    def __init__(self, ctx = None):
        super(BattleResultsWindow, self).__init__()
        raise 'dataProvider' in ctx or AssertionError
        raise ctx['dataProvider'] is not None or AssertionError
        self.dataProvider = ctx['dataProvider']
        self.__premiumBonusesDiff = {}
        return

    @storage_getter('users')
    def usersStorage(self):
        return None

    @process
    def _populate(self):
        super(BattleResultsWindow, self)._populate()
        self.addListener(events.LobbySimpleEvent.PREMIUM_BOUGHT, self.__onPremiumBought)
        commonData = yield self.__getCommonData()
        self.as_setDataS(commonData)
        if commonData is not None:
            results = self.dataProvider.results
            if self._isRated7x7Battle():
                cur, prev = results.getDivisions()
                if cur != prev:
                    self.__showDivisionAnimation(cur, prev)
        return

    def _dispose(self):
        self.dataProvider.destroy()
        self.removeListener(events.LobbySimpleEvent.PREMIUM_BOUGHT, self.__onPremiumBought)
        super(BattleResultsWindow, self)._dispose()

    def onWindowClose(self):
        import MusicController
        MusicController.g_musicController.setAccountAttrs(g_itemsCache.items.stats.attributes, True)
        MusicController.g_musicController.play(MusicController.MUSIC_EVENT_LOBBY)
        MusicController.g_musicController.play(MusicController.MUSIC_EVENT_LOBBY)
        self.destroy()

    def getDenunciations(self):
        return g_itemsCache.items.stats.denunciationsLeft

    def showEventsWindow(self, eID, eventType):
        return quests_events.showEventsWindow(eID, eventType)

    def saveSorting(self, iconType, sortDirection, bonusType):
        AccountSettings.setSettings('statsSorting' if bonusType != ARENA_BONUS_TYPE.SORTIE else 'statsSortingSortie', {'iconType': iconType,
         'sortDirection': sortDirection})

    def __getPlayerName(self, playerDBID):
        playerNameRes = self.__playersNameCache.get(playerDBID)
        if playerNameRes is None:
            player = self.dataProvider.getPlayerData(playerDBID)
            playerNameRes = self.__playersNameCache[playerDBID] = (player.getFullName(), (player.name,
              player.clanAbbrev,
              player.getRegionCode(),
              player.igrType))
        return playerNameRes

    def __getVehicleData(self, vehicleCompDesc):
        vehicleName = i18n.makeString(UNKNOWN_VEHICLE_NAME_VALUE)
        vehicleShortName = i18n.makeString(UNKNOWN_VEHICLE_NAME_VALUE)
        vehicleIcon = VEHICLE_ICON_FILE.format(VEHICLE_NO_IMAGE_FILE_NAME)
        vehicleIconSmall = VEHICLE_ICON_SMALL_FILE.format(VEHICLE_NO_IMAGE_FILE_NAME)
        vehicleBalanceWeight = 0
        nation = -1
        if vehicleCompDesc:
            vehicle = g_itemsCache.items.getItemByCD(vehicleCompDesc)
            vehicleName = vehicle.userName
            vehicleShortName = vehicle.shortUserName
            nameReplaced = vehicle.name.replace(':', '-')
            if vehicle.isEvent:
                vehicleIcon = VEHICLE_ICON_FALLOUT_FILE.format(nameReplaced)
            else:
                vehicleIcon = vehicle.icon
            vehicleIconSmall = vehicle.iconSmall
            nation = vehicle.nationID
            vehicleBalanceWeight = vehicle.descriptor.balanceWeight
        return (vehicleName,
         vehicleShortName,
         vehicleIcon,
         vehicleIconSmall,
         vehicleBalanceWeight,
         nation)

    def __vehiclesComparator(self, item, other):
        res = 0
        iKiller = item.get('killerID', 0)
        cd = item.get('typeCompDescr')
        if cd is not None:
            iType = vehicles_core.getVehicleType(cd)
            iLevel = iType.level if iType else -1
            iWeight = VEHICLE_BATTLE_TYPES_ORDER_INDICES.get(set(VEHICLE_CLASS_TAGS.intersection(iType.tags)).pop(), 10) if iType else 10
        else:
            iLevel = -1
            iWeight = 10
        oKiller = other.get('killerID', 0)
        cd = other.get('typeCompDescr')
        if cd is not None:
            oType = vehicles_core.getVehicleType(other.get('typeCompDescr', None))
            oLevel = oType.level if oType else -1
            oWeight = VEHICLE_BATTLE_TYPES_ORDER_INDICES.get(set(VEHICLE_CLASS_TAGS.intersection(oType.tags)).pop(), 10) if oType else 10
        else:
            oLevel = -1
            oWeight = 10
        if iKiller == 0 and oKiller == 0 or iKiller != 0 and oKiller != 0:
            res = cmp(oLevel, iLevel) or cmp(iWeight, oWeight) or cmp(item.get('vehicleName', ''), other.get('vehicleName', ''))
        elif not iKiller:
            res = -1
        else:
            res = 1
        return res

    def __getStatsLine(self, label = None, col1 = None, col2 = None, col3 = None, col4 = None):
        if col2 is not None:
            lineType = 'wideLine'
        else:
            lineType = 'normalLine'
        lbl = label + '\n' if label is not None else '\n'
        lblStripped = re.sub('<[^<]+?>', '', lbl)
        return {'label': lbl,
         'labelStripped': lblStripped,
         'col1': col1 if col1 is not None else '\n',
         'col2': col2 if col2 is not None else '\n',
         'col3': col3 if col3 is not None else '\n',
         'col4': col4 if col4 is not None else '\n',
         'lineType': None if label is None else lineType}

    def __resultLabel(self, label):
        return i18n.makeString(RESULT_LINE_STR.format(label))

    def __makeCreditsLabel(self, value, canBeFaded = False, isDiff = False):
        valStr = BigWorld.wg_getGoldFormat(int(value))
        if value < 0:
            valStr = self.__makeRedLabel(valStr)
        if isDiff:
            valStr = '+ %s' % valStr
        templateName = 'credits_small_inactive_label' if canBeFaded and value == 0 else 'credits_small_label'
        return makeHtmlString('html_templates:lobby/battle_results', templateName, {'value': valStr})

    def __makeXpLabel(self, value, canBeFaded = False, isDiff = False):
        valStr = BigWorld.wg_getIntegralFormat(int(value))
        if value < 0:
            valStr = self.__makeRedLabel(valStr)
        if isDiff:
            valStr = '+ %s' % valStr
        templateName = 'xp_small_inactive_label' if canBeFaded and value == 0 else 'xp_small_label'
        return makeHtmlString('html_templates:lobby/battle_results', templateName, {'value': valStr})

    def __makeResourceLabel(self, value, canBeFaded = False):
        valStr = BigWorld.wg_getIntegralFormat(int(value))
        if value < 0:
            valStr = self.__makeRedLabel(valStr)
        templateName = 'resource_small_inactive_label' if canBeFaded and value == 0 else 'resource_small_label'
        return makeHtmlString('html_templates:lobby/battle_results', templateName, {'value': valStr})

    def __makeFreeXpLabel(self, value, canBeFaded = False):
        valStr = BigWorld.wg_getIntegralFormat(int(value))
        templateName = 'free_xp_small_inactive_label' if canBeFaded and value == 0 else 'free_xp_small_label'
        return makeHtmlString('html_templates:lobby/battle_results', templateName, {'value': valStr})

    def __makeGoldLabel(self, value, canBeFaded = False):
        valStr = BigWorld.wg_getGoldFormat(value)
        templateName = 'gold_small_inactive_label' if canBeFaded and value == 0 else 'gold_small_label'
        return makeHtmlString('html_templates:lobby/battle_results', templateName, {'value': valStr})

    def __makePercentLabel(self, value):
        valStr = BigWorld.wg_getGoldFormat(int(value))
        templateName = 'percent'
        if value < 0:
            valStr = self.__makeRedLabel(valStr)
            templateName = 'negative_percent'
        return makeHtmlString('html_templates:lobby/battle_results', templateName, {'value': valStr})

    def __makeRedLabel(self, value):
        return makeHtmlString('html_templates:lobby/battle_results', 'negative_value', {'value': value})

    def __populateStatValues(self, node, isFallout, isSelf = False):
        node = node.copy()
        if not isFallout:
            node['damagedKilled'] = self.__makeSlashedValuesStr(node, 'damaged', 'kills')
            node['capturePointsVal'] = self.__makeSlashedValuesStr(node, 'capturePoints', 'droppedCapturePoints')
        else:
            node['killed'] = node['kills']
        node['teamHitsDamage'] = self.__makeTeamDamageStr(node)
        node['hits'] = self.__makeSlashedValuesStr(node, 'directHits', 'piercings')
        node['mileage'] = self.__makeMileageStr(node.get('mileage', 0))
        flagActions = node.get('flagActions', [0] * len(FLAG_ACTION.RANGE))
        node['flags'] = flagActions[FLAG_ACTION.CAPTURED]
        node['deaths'] = node.get('deathCount', 0)
        node['victoryScore'] = node.get('winPoints', 0)
        result = []
        for key, isInt, selfKey in STATS_KEYS:
            if not isFallout and key in FALLOUT_ONLY_STATS:
                continue
            if isFallout and key in FALLOUT_EXCLUDE_VEHICLE_STATS:
                continue
            if key in FALLOUT_ORDER_STATS and key not in node:
                continue
            if isInt:
                value = node.get(key, 0)
                valueFormatted = BigWorld.wg_getIntegralFormat(value)
                if not value:
                    valueFormatted = makeHtmlString('html_templates:lobby/battle_results', 'empty_stat_value', {'value': valueFormatted})
            else:
                valueFormatted = node.get(key, '')
            if isSelf and selfKey is not None:
                key = selfKey
            result.append({'label': i18n.makeString(STATS_KEY_BASE.format(key)),
             'value': valueFormatted})

        return result

    def __populateAccounting(self, commonData, personalCommonData, personalData, playersData, personalDataOutput, isFallout):
        if self.dataProvider.getArenaUniqueID() in self.__buyPremiumCache:
            isPostBattlePremium = True
        else:
            isPostBattlePremium = personalCommonData.get('isPremium', False)
        isPremium = personalCommonData.get('isPremium', False)
        premCreditsFactor = personalCommonData.get('premiumCreditsFactor10', 10) / 10.0
        igrXpFactor = personalCommonData.get('igrXPFactor10', 10) / 10.0
        premXpFactor = personalCommonData.get('premiumXPFactor10', 10) / 10.0
        aogasFactor = personalCommonData.get('aogasFactor10', 10) / 10.0
        refSystemFactor = personalCommonData.get('refSystemXPFactor10', 10) / 10.0
        aogasValStr = ''
        personalDataOutput['xpTitleStrings'] = xpTitleStrings = []
        personalDataOutput['isPremium'] = isPostBattlePremium
        personalDataOutput['creditsNoPremValues'] = creditsNoPremValues = []
        personalDataOutput['creditsPremValues'] = creditsPremValues = []
        personalDataOutput['xpNoPremValues'] = xpNoPremValues = []
        personalDataOutput['xpPremValues'] = xpPremValues = []
        personalDataOutput['resValues'] = resValues = []
        personalDataOutput['resPremValues'] = resPremValues = []
        showIntermediateTotal = False
        fairPlayViolationName = self.__getFairPlayViolationName(personalCommonData)
        hasViolation = fairPlayViolationName is not None
        playerData = playersData.get(personalCommonData.get('accountDBID', 0), {'igrType': 0,
         'clanDBID': 0,
         'clanAbbrev': ''})
        personalDataOutput['isLegionnaire'] = False if playerData.get('clanDBID') else True
        igrType = playerData.get('igrType', 0)
        vehsCreditsData = []
        vehsXPData = []
        for vehIntCD, sourceData in self.__buildPersonalDataSource(personalData, isFallout):
            dailyXpFactor = sourceData['dailyXPFactor10'] / 10.0
            creditsData = []
            creditsToDraw = self.__calculateBaseParam('creditsToDraw', sourceData, premCreditsFactor, isPremium)
            achievementCredits = sourceData['achievementCredits']
            creditsPenalty = self.__calculateBaseCreditsPenalty(personalCommonData, isPremium)
            creditsCompensation = self.__calculateBaseParam('creditsContributionIn', sourceData, premCreditsFactor, isPremium)
            isNoPenalty = achievementCredits > 0
            creditsBase = sourceData['originalCredits']
            creditsCell = creditsBase - achievementCredits - creditsToDraw
            creditsCellPrem = int(round(creditsBase * premCreditsFactor)) - int(round(achievementCredits * premCreditsFactor)) - int(round(creditsToDraw * premCreditsFactor))
            creditsCellStr = self.__makeCreditsLabel(creditsCell, not isPostBattlePremium)
            creditsCellPremStr = self.__makeCreditsLabel(creditsCellPrem, isPostBattlePremium)
            creditsData.append(self.__getStatsLine(self.__resultLabel('base'), creditsCellStr, None, creditsCellPremStr, None))
            achievementCreditsPrem = 0
            if isNoPenalty:
                showIntermediateTotal = True
                achievementCreditsPrem = int(round(achievementCredits * premCreditsFactor))
                creditsData.append(self.__getStatsLine(self.__resultLabel('noPenalty'), self.__makeCreditsLabel(achievementCredits, not isPostBattlePremium), None, self.__makeCreditsLabel(achievementCreditsPrem, isPostBattlePremium), None))
            boosterCredits = self.__calculateBaseParam('boosterCredits', sourceData, premCreditsFactor, isPremium)
            boosterCreditsPrem = int(round(boosterCredits * premCreditsFactor))
            if boosterCredits > 0 or boosterCreditsPrem > 0:
                showIntermediateTotal = True
                boosterCreditsStr = self.__makeCreditsLabel(boosterCredits, not isPostBattlePremium) if boosterCredits else None
                boosterCreditsPremStr = self.__makeCreditsLabel(boosterCreditsPrem, isPostBattlePremium) if boosterCreditsPrem else None
                creditsData.append(self.__getStatsLine(self.__resultLabel('boosters'), boosterCreditsStr, None, boosterCreditsPremStr, None))
            orderCredits = self.__calculateBaseParam('orderCredits', sourceData, premCreditsFactor, isPremium)
            orderCreditsPrem = int(round(orderCredits * premCreditsFactor))
            if orderCredits > 0 or orderCreditsPrem > 0:
                showIntermediateTotal = True
                orderCreditsStr = self.__makeCreditsLabel(orderCredits, not isPostBattlePremium) if orderCredits else None
                orderCreditsPremStr = self.__makeCreditsLabel(orderCreditsPrem, isPostBattlePremium) if orderCreditsPrem else None
                creditsData.append(self.__getStatsLine(self.__resultLabel('battlePayments'), orderCreditsStr, None, orderCreditsPremStr, None))
            eventCredits = self.__calculateBaseParam('eventCredits', sourceData, premXpFactor, isPremium)
            creditsEventStr = self.__makeCreditsLabel(eventCredits, not isPostBattlePremium) if eventCredits else None
            eventCreditsPrem = self.__calculateParamWithPrem('eventCredits', sourceData, premXpFactor, isPremium)
            creditsEventPremStr = self.__makeCreditsLabel(eventCreditsPrem, isPostBattlePremium) if eventCreditsPrem else None
            eventGold = sourceData['eventGold']
            goldEventStr = self.__makeGoldLabel(eventGold, not isPostBattlePremium) if eventGold else None
            goldEventPremStr = self.__makeGoldLabel(eventGold, isPostBattlePremium) if eventGold else None
            if eventCredits > 0 or eventGold > 0:
                showIntermediateTotal = True
                creditsData.append(self.__getStatsLine(self.__resultLabel('event'), creditsEventStr, goldEventStr, creditsEventPremStr, goldEventPremStr))
            creditsData.append(self.__getStatsLine())
            if hasViolation:
                penaltyValue = self.__makePercentLabel(int(-100))
                creditsData.append(self.__getStatsLine(self.__resultLabel('fairPlayViolation/' + fairPlayViolationName), penaltyValue, None, penaltyValue, None))
            creditsPenaltyStr = self.__makeCreditsLabel(int(-creditsPenalty), not isPostBattlePremium)
            creditsPenaltyPremStr = self.__makeCreditsLabel(int(-creditsPenalty * premCreditsFactor), isPostBattlePremium)
            creditsData.append(self.__getStatsLine(self.__resultLabel('friendlyFirePenalty'), creditsPenaltyStr, None, creditsPenaltyPremStr, None))
            creditsCompensationStr = self.__makeCreditsLabel(int(creditsCompensation), not isPostBattlePremium)
            creditsCompensationPremStr = self.__makeCreditsLabel(int(creditsCompensation * premCreditsFactor), isPostBattlePremium)
            creditsData.append(self.__getStatsLine(self.__resultLabel('friendlyFireCompensation'), creditsCompensationStr, None, creditsCompensationPremStr, None))
            creditsData.append(self.__getStatsLine())
            if creditsPenalty or creditsCompensation:
                showIntermediateTotal = True
            if aogasFactor < 1:
                showIntermediateTotal = True
                aogasValStr = ''.join([i18n.makeString(XP_MULTIPLIER_SIGN_KEY), BigWorld.wg_getFractionalFormat(aogasFactor)])
                aogasValStr = self.__makeRedLabel(aogasValStr)
                creditsData.append(self.__getStatsLine(self.__resultLabel('aogasFactor'), aogasValStr, None, aogasValStr, None))
                creditsData.append(self.__getStatsLine())
            creditsWithoutPremTotal = self.__calculateTotalCredits(sourceData, eventCredits, premCreditsFactor, isPremium, aogasFactor, creditsBase, orderCredits, boosterCredits, creditsToDraw, creditsPenalty, creditsCompensation, hasViolation, False)
            creditsNoPremValues.append(self.__makeCreditsLabel(creditsCell, not isPostBattlePremium))
            xpTitleString = i18n.makeString(XP_TITLE)
            if dailyXpFactor > 1:
                xpTitleString = ' '.join((xpTitleString, i18n.makeString(XP_TITLE_DAILY, dailyXpFactor)))
            xpTitleStrings.append(xpTitleString)
            creditsWithPremTotal = self.__calculateTotalCredits(sourceData, eventCredits, premCreditsFactor, isPremium, aogasFactor, creditsBase, orderCredits, boosterCredits, creditsToDraw, creditsPenalty, creditsCompensation, hasViolation, True)
            if showIntermediateTotal:
                creditsData.append(self.__getStatsLine(self.__resultLabel('intermediateTotal'), self.__makeCreditsLabel(creditsWithoutPremTotal, not isPostBattlePremium), goldEventStr, self.__makeCreditsLabel(creditsWithPremTotal, isPostBattlePremium), goldEventPremStr))
                creditsData.append(self.__getStatsLine())
            creditsAutoRepair = sourceData['autoRepairCost']
            if creditsAutoRepair is None:
                creditsAutoRepair = 0
            creditsAutoRepairStr = self.__makeCreditsLabel(-creditsAutoRepair, not isPostBattlePremium)
            creditsAutoRepairPremStr = self.__makeCreditsLabel(-creditsAutoRepair, isPostBattlePremium)
            creditsData.append(self.__getStatsLine(self.__resultLabel('autoRepair'), creditsAutoRepairStr, None, creditsAutoRepairPremStr, None))
            autoLoadCost = sourceData['autoLoadCost']
            if autoLoadCost is None:
                autoLoadCost = (0, 0)
            creditsAutoLoad, goldAutoLoad = autoLoadCost
            creditsAutoLoadStr = self.__makeCreditsLabel(-creditsAutoLoad, not isPostBattlePremium)
            creditsAutoLoadPremStr = self.__makeCreditsLabel(-creditsAutoLoad, isPostBattlePremium)
            goldAutoLoadStr = self.__makeGoldLabel(-goldAutoLoad, not isPostBattlePremium) if goldAutoLoad else None
            goldAutoLoadPremStr = self.__makeGoldLabel(-goldAutoLoad, isPostBattlePremium) if goldAutoLoad else None
            creditsData.append(self.__getStatsLine(self.__resultLabel('autoLoad'), creditsAutoLoadStr, goldAutoLoadStr, creditsAutoLoadPremStr, goldAutoLoadPremStr))
            autoEquipCost = sourceData['autoEquipCost']
            if autoEquipCost is None:
                autoEquipCost = (0, 0)
            creditsAutoEquip, goldAutoEquip = autoEquipCost
            creditsAutoEquipStr = self.__makeCreditsLabel(-creditsAutoEquip, not isPostBattlePremium)
            creditsAutoEquipPremStr = self.__makeCreditsLabel(-creditsAutoEquip, isPostBattlePremium)
            goldAutoEquipStr = self.__makeGoldLabel(-goldAutoEquip, not isPostBattlePremium)
            goldAutoEquipPremStr = self.__makeGoldLabel(-goldAutoEquip, isPostBattlePremium)
            creditsData.append(self.__getStatsLine(self.__resultLabel('autoEquip'), creditsAutoEquipStr, goldAutoEquipStr, creditsAutoEquipPremStr, goldAutoEquipPremStr))
            creditsData.append(self.__getStatsLine())
            creditsWithoutPremTotalStr = self.__makeCreditsLabel(creditsWithoutPremTotal - creditsAutoRepair - creditsAutoEquip - creditsAutoLoad, not isPostBattlePremium and not hasViolation)
            creditsWithPremTotalStr = self.__makeCreditsLabel(creditsWithPremTotal - creditsAutoRepair - creditsAutoEquip - creditsAutoLoad, isPostBattlePremium and not hasViolation)
            if vehIntCD is not None:
                _, personalDataRecord = findFirst(lambda (vId, d): vId == vehIntCD, personalData, (None, None))
                if personalDataRecord is not None:
                    personalDataRecord['pureCreditsReceived'] = (creditsWithPremTotal if isPremium else creditsWithoutPremTotal) - creditsAutoRepair - creditsAutoEquip - creditsAutoLoad
            goldTotalStr = self.__makeGoldLabel(eventGold - goldAutoEquip - goldAutoLoad, not isPostBattlePremium and not hasViolation)
            goldTotalPremStr = self.__makeGoldLabel(eventGold - goldAutoEquip - goldAutoLoad, isPostBattlePremium and not hasViolation)
            totalLbl = makeHtmlString('html_templates:lobby/battle_results', 'lightText', {'value': self.__resultLabel('total')})
            creditsData.append(self.__getStatsLine(totalLbl, creditsWithoutPremTotalStr, goldTotalStr, creditsWithPremTotalStr, goldTotalPremStr))
            vehsCreditsData.append(creditsData)
            xpData = []
            achievementXP = int(sourceData['achievementXP'])
            achievementFreeXP = sourceData['achievementFreeXP']
            xpPenalty = int(sourceData.get('xpPenaltyBase', 0))
            xpBase = int(sourceData['originalXP'])
            xpCell = xpBase - achievementXP
            xpCellPrem = int(round(xpCell * premXpFactor))
            dailyXP = sourceData['dailyXP']
            dailyXPCell = dailyXP - achievementXP
            dailyXPCellPrem = int(round(dailyXPCell * premXpFactor))
            xpCellStr = self.__makeXpLabel(xpCell, not isPostBattlePremium)
            xpCellPremStr = self.__makeXpLabel(xpCellPrem, isPostBattlePremium)
            freeXpBase = sourceData['originalFreeXP']
            dailyFreeXP = sourceData['dailyFreeXP']
            freeXpBaseStr = self.__makeFreeXpLabel(freeXpBase - achievementFreeXP, not isPostBattlePremium)
            freeXpBasePremStr = self.__makeFreeXpLabel(int(round((freeXpBase - achievementFreeXP) * premXpFactor)), isPostBattlePremium)
            medals = sourceData['dossierPopUps']
            if RECORD_DB_IDS[('max15x15', 'maxXP')] in map(lambda (id, value): id, medals):
                label = makeHtmlString('html_templates:lobby/battle_results', 'xpRecord', {})
            else:
                label = self.__resultLabel('base')
            xpData.append(self.__getStatsLine(label, xpCellStr, freeXpBaseStr, xpCellPremStr, freeXpBasePremStr))
            if isNoPenalty:
                xpData.append(self.__getStatsLine(self.__resultLabel('noPenalty'), self.__makeXpLabel(achievementXP, not isPostBattlePremium), self.__makeFreeXpLabel(achievementFreeXP, not isPostBattlePremium), self.__makeXpLabel(int(round(achievementXP * premXpFactor)), isPostBattlePremium), self.__makeFreeXpLabel(int(round(achievementFreeXP * premXpFactor)), isPostBattlePremium)))
            if fairPlayViolationName is not None:
                penaltyXPVal = self.__makePercentLabel(int(-100))
                xpData.append(self.__getStatsLine(self.__resultLabel('fairPlayViolation/' + fairPlayViolationName), penaltyXPVal, penaltyXPVal, penaltyXPVal, penaltyXPVal))
            xpPenaltyStr = self.__makeXpLabel(-xpPenalty, not isPostBattlePremium)
            xpPenaltyPremStr = self.__makeXpLabel(int(round(-xpPenalty * premXpFactor)), isPostBattlePremium)
            xpData.append(self.__getStatsLine(self.__resultLabel('friendlyFirePenalty'), xpPenaltyStr, None, xpPenaltyPremStr, None))
            if igrXpFactor > 1:
                icon = makeHtmlString('html_templates:igr/iconSmall', 'premium' if igrType == IGR_TYPE.PREMIUM else 'basic')
                igrBonusLabelStr = i18n.makeString(BATTLE_RESULTS.DETAILS_CALCULATIONS_IGRBONUS, igrIcon=icon)
                igrBonusStr = makeHtmlString('html_templates:lobby/battle_results', 'igr_bonus', {'value': BigWorld.wg_getNiceNumberFormat(igrXpFactor)})
                xpData.append(self.__getStatsLine(igrBonusLabelStr, igrBonusStr, igrBonusStr, igrBonusStr, igrBonusStr))
            if dailyXpFactor > 1:
                dailyXpStr = makeHtmlString('html_templates:lobby/battle_results', 'multy_xp_small_label', {'value': int(dailyXpFactor)})
                xpData.append(self.__getStatsLine(self.__resultLabel('firstWin'), dailyXpStr, dailyXpStr, dailyXpStr, dailyXpStr))
            boosterXP = self.__calculateBaseParam('boosterXP', sourceData, premXpFactor, isPremium)
            boosterXPPrem = self.__calculateParamWithPrem('boosterXP', sourceData, premXpFactor, isPremium)
            boosterFreeXP = self.__calculateBaseParam('boosterFreeXP', sourceData, premXpFactor, isPremium)
            boosterFreeXPPrem = self.__calculateParamWithPrem('boosterFreeXP', sourceData, premXpFactor, isPremium)
            if boosterXP > 0 or boosterFreeXP > 0:
                boosterXPStr = self.__makeXpLabel(boosterXP, not isPostBattlePremium) if boosterXP else None
                boosterXPPremStr = self.__makeXpLabel(boosterXPPrem, isPostBattlePremium) if boosterXPPrem else None
                boosterFreeXPStr = self.__makeFreeXpLabel(boosterFreeXP, not isPostBattlePremium) if boosterFreeXP else None
                boosterFreeXPPremStr = self.__makeFreeXpLabel(boosterFreeXPPrem, isPostBattlePremium) if boosterFreeXPPrem else None
                xpData.append(self.__getStatsLine(self.__resultLabel('boosters'), boosterXPStr, boosterFreeXPStr, boosterXPPremStr, boosterFreeXPPremStr))
            orderXP = self.__calculateBaseParam('orderXP', sourceData, premXpFactor, isPremium)
            orderXPPrem = self.__calculateParamWithPrem('orderXP', sourceData, premXpFactor, isPremium)
            if orderXP > 0:
                orderXPStr = self.__makeXpLabel(orderXP, not isPostBattlePremium) if orderXP else None
                orderXPPremStr = self.__makeXpLabel(orderXPPrem, isPostBattlePremium) if orderXPPrem else None
                xpData.append(self.__getStatsLine(self.__resultLabel('tacticalTraining'), orderXPStr, None, orderXPPremStr, None))
            orderFreeXP = self.__calculateBaseParam('orderFreeXP', sourceData, premXpFactor, isPremium)
            orderFreeXPPrem = self.__calculateParamWithPrem('orderFreeXP', sourceData, premXpFactor, isPremium)
            if orderFreeXP > 0:
                orderFreeXPStr = self.__makeFreeXpLabel(orderFreeXP, not isPostBattlePremium) if orderFreeXP else None
                orderFreeXPPremStr = self.__makeFreeXpLabel(orderFreeXPPrem, isPostBattlePremium) if orderFreeXPPrem else None
                xpData.append(self.__getStatsLine(self.__resultLabel('militaryManeuvers'), None, orderFreeXPStr, None, orderFreeXPPremStr))
            eventXP = self.__calculateBaseParam('eventXP', sourceData, premXpFactor, isPremium)
            eventXPPrem = self.__calculateParamWithPrem('eventXP', sourceData, premXpFactor, isPremium)
            eventFreeXP = self.__calculateBaseParam('eventFreeXP', sourceData, premXpFactor, isPremium)
            eventFreeXPPrem = self.__calculateParamWithPrem('eventFreeXP', sourceData, premXpFactor, isPremium)
            if eventXP > 0 or eventFreeXP > 0:
                eventXPStr = self.__makeXpLabel(eventXP, not isPostBattlePremium)
                eventXPPremStr = self.__makeXpLabel(eventXPPrem, isPostBattlePremium)
                eventFreeXPStr = self.__makeFreeXpLabel(eventFreeXP, not isPostBattlePremium)
                eventFreeXPPremStr = self.__makeFreeXpLabel(eventFreeXPPrem, isPostBattlePremium)
                xpData.append(self.__getStatsLine(self.__resultLabel('event'), eventXPStr, eventFreeXPStr, eventXPPremStr, eventFreeXPPremStr))
            if refSystemFactor > 1:
                refSysXpValue = xpBase * igrXpFactor * refSystemFactor
                refSysFreeXpValue = freeXpBase * refSystemFactor
                refSysXPStr = self.__makeXpLabel(refSysXpValue, not isPostBattlePremium)
                refSysFreeXPStr = self.__makeFreeXpLabel(refSysFreeXpValue, not isPostBattlePremium)
                refSysXPPremStr = self.__makeXpLabel(round(refSysXpValue * premXpFactor), isPostBattlePremium)
                refSysFreeXPPremStr = self.__makeFreeXpLabel(round(refSysFreeXpValue * premXpFactor), isPostBattlePremium)
                xpData.append(self.__getStatsLine(self.__resultLabel('referralBonus'), refSysXPStr, refSysFreeXPStr, refSysXPPremStr, refSysFreeXPPremStr))
            premiumVehicleXP = sourceData['premiumVehicleXP']
            if premiumVehicleXP > 0:
                xpData.append(self.__getPremiumVehicleXP(premiumVehicleXP, isPremium, premXpFactor))
            if aogasFactor < 1:
                xpData.append(self.__getStatsLine(self.__resultLabel('aogasFactor'), aogasValStr, aogasValStr, aogasValStr, aogasValStr))
            if len(xpData) < 3:
                xpData.append(self.__getStatsLine())
            if len(xpData) < 7:
                xpData.append(self.__getStatsLine())
            xpWithoutPremTotal = self.__calculateTotalXp(sourceData, aogasFactor, premXpFactor, igrXpFactor, refSystemFactor, isPremium, xpBase, dailyXP, xpPenalty, orderXP, boosterXP, eventXP, hasViolation, False)
            xpTotal = self.__makeXpLabel(xpWithoutPremTotal, not isPostBattlePremium and not hasViolation)
            xpWithPremTotal = self.__calculateTotalXp(sourceData, aogasFactor, premXpFactor, igrXpFactor, refSystemFactor, isPremium, xpBase, dailyXP, xpPenalty, orderXP, boosterXP, eventXP, hasViolation, True)
            xpPremTotal = self.__makeXpLabel(xpWithPremTotal, isPostBattlePremium and not hasViolation)
            freeXpTotal = self.__makeFreeXpLabel(self.__calculateTotalFreeXp(sourceData, aogasFactor, premXpFactor, igrXpFactor, refSystemFactor, isPremium, freeXpBase, dailyFreeXP, orderFreeXP, boosterFreeXP, eventFreeXP, hasViolation, False), not isPostBattlePremium and not hasViolation)
            freeXpPremTotal = self.__makeFreeXpLabel(self.__calculateTotalFreeXp(sourceData, aogasFactor, premXpFactor, igrXpFactor, refSystemFactor, isPremium, freeXpBase, dailyFreeXP, orderFreeXP, boosterFreeXP, eventFreeXP, hasViolation, True), isPostBattlePremium and not hasViolation)
            xpData.append(self.__getStatsLine(totalLbl, xpTotal, freeXpTotal, xpPremTotal, freeXpPremTotal))
            vehsXPData.append(xpData)
            if 'xpStr' not in personalDataOutput and 'creditsStr' not in personalDataOutput:
                if fairPlayViolationName is not None:
                    personalDataOutput['xpStr'] = 0
                    personalDataOutput['creditsStr'] = 0
                else:
                    showPremium = isPremium or isPostBattlePremium
                    personalDataOutput['xpStr'] = BigWorld.wg_getIntegralFormat(xpWithPremTotal if showPremium else xpWithoutPremTotal)
                    personalDataOutput['creditsStr'] = BigWorld.wg_getIntegralFormat(creditsCellPrem if showPremium else creditsCell)
            showDiffs = False
            personalDataOutput['hasGetPremBtn'] = False
            creditsDiff = creditsWithPremTotal - creditsWithoutPremTotal
            xpDiff = xpWithPremTotal - xpWithoutPremTotal
            self.__premiumBonusesDiff = {'xpDiff': xpDiff,
             'creditDiff': creditsDiff}
            if g_lobbyContext.getServerSettings().isPremiumInPostBattleEnabled() and not isPremium and not g_itemsCache.items.stats.isPremium and commonData.get('bonusType', 0) == ARENA_BONUS_TYPE.REGULAR and xpDiff > 0 and creditsDiff > 0:
                personalDataOutput['getPremVO'] = {'arenaUniqueID': self.dataProvider.getArenaUniqueID(),
                 'creditsDiff': creditsDiff,
                 'xpDiff': xpDiff}
                showDiffs = True
                personalDataOutput['hasGetPremBtn'] = True
            valString = xpWithPremTotal if not showDiffs else xpDiff
            xpNoPremValues.append(self.__makeXpLabel(xpWithoutPremTotal, not isPostBattlePremium))
            xpPremValues.append(self.__makeXpLabel(valString, isPostBattlePremium, showDiffs))
            valString = creditsCellPrem if not showDiffs else creditsDiff
            creditsPremValues.append(self.__makeCreditsLabel(valString, isPostBattlePremium, showDiffs))

        personalDataOutput['creditsData'] = vehsCreditsData
        personalDataOutput['xpData'] = vehsXPData
        if commonData.get('bonusType', 0) == ARENA_BONUS_TYPE.SORTIE:
            clanDBID = playerData.get('clanDBID')
            resValue = personalCommonData.get('fortResource', 0) if clanDBID else 0
            resValue = 0 if resValue is None else resValue
            orderFortResource = personalCommonData.get('orderFortResource', 0) if clanDBID else 0
            baseResValue = resValue - orderFortResource
            personalDataOutput['fortResourceTotal'] = baseResValue
            resValues.append(self.__makeResourceLabel(baseResValue, not isPostBattlePremium) if clanDBID else '-')
            resPremValues.append(self.__makeResourceLabel(baseResValue, isPostBattlePremium) if clanDBID else '-')
            resData = []
            resData.append(self.__getStatsLine(self.__resultLabel('base'), None, self.__makeResourceLabel(baseResValue, not isPostBattlePremium), None, self.__makeResourceLabel(baseResValue, isPostBattlePremium)))
            if orderFortResource:
                resData.append(self.__getStatsLine(self.__resultLabel('heavyTrucks'), None, self.__makeResourceLabel(orderFortResource, not isPostBattlePremium), None, self.__makeResourceLabel(orderFortResource, isPostBattlePremium)))
            if len(resData) > 1:
                resData.append(self.__getStatsLine())
            resData.append(self.__getStatsLine(self.__resultLabel('total'), None, self.__makeResourceLabel(resValue, not isPostBattlePremium), None, self.__makeResourceLabel(resValue, isPostBattlePremium)))
            personalDataOutput['resourceData'] = resData
        return

    def __buildPersonalDataSource(self, personalData, isFallout):
        totalData = {}
        personaDataSource = [(None, totalData)]
        for vehIntCD, pData in personalData:
            data = {}
            for k, (d, func) in CUMULATIVE_ACCOUNT_DATA:
                if k in RELATED_ACCOUNT_DATA:
                    v = RELATED_ACCOUNT_DATA[k](pData, data)
                else:
                    v = pData.get(k, d)
                data[k] = v
                if func is not None:
                    totalData.setdefault(k, d)
                    totalData[k] = func(totalData[k], v)
                else:
                    totalData[k] = d

            personaDataSource.append((vehIntCD, data))

        return personaDataSource

    def __buildEfficiencyDataSource(self, pData, pCommonData, playersData, commonData):
        totalEnemies = []
        totalTechniquesGroup = []
        totalBasesGroup = []
        efficiencyDataSource = [(totalTechniquesGroup, totalEnemies, totalBasesGroup)]
        playerTeam = pCommonData.get('team')
        playerDBID = pCommonData.get('accountDBID')
        totalVehsData = {}
        for vehIntCD, data in pData:
            enemiesGroup = []
            for (vId, vIntCD), iInfo in data.get('details', dict()).iteritems():
                accountDBID = self.dataProvider.getAccountDBID(vId)
                pInfo = playersData.get(accountDBID, dict())
                if accountDBID == playerDBID:
                    continue
                team = pInfo.get('team', data.get('team') % 2 + 1)
                if team == playerTeam:
                    continue
                if (vId, vIntCD) not in totalVehsData:
                    totalVehsData[vId, vIntCD] = iInfo.copy()
                else:
                    totalVehData = totalVehsData[vId, vIntCD]
                    for k, v in iInfo.iteritems():
                        if k == 'deathReason':
                            currentValue = totalVehData[k]
                            if v > currentValue:
                                totalVehData[k] = v
                        else:
                            totalVehData[k] += v

                enemiesGroup.append(((vId, vIntCD), iInfo))

            techniquesGroup, basesGroup = self.__getBasesInfo(data, commonData, enemiesGroup)
            totalTechniquesGroup += techniquesGroup
            totalBasesGroup += basesGroup
            efficiencyDataSource.append((techniquesGroup, enemiesGroup, totalBasesGroup))

        for (vId, vIntCD), iInfo in totalVehsData.iteritems():
            totalEnemies.append(((vId, vIntCD), iInfo))

        return efficiencyDataSource

    def __getPremiumVehicleXP(self, premiumVehicleXP, isPremiumAccount, premAccFactor):
        if isPremiumAccount:
            xpWithPremium, xpWithoutPremium = premiumVehicleXP, premiumVehicleXP / premAccFactor
        else:
            xpWithPremium, xpWithoutPremium = premiumVehicleXP * premAccFactor, premiumVehicleXP
        freeXpWithoutPremium = 0
        freeXpWithPremium = 0
        xpWithoutPremiumColumn = self.__makeXpLabel(xpWithoutPremium, not isPremiumAccount)
        xpWithPremiumColumn = self.__makeXpLabel(xpWithPremium, isPremiumAccount)
        freeXpWithoutPremiumColumn = self.__makeFreeXpLabel(freeXpWithoutPremium, not isPremiumAccount)
        freeXpWithPremiumColumn = self.__makeFreeXpLabel(freeXpWithPremium, isPremiumAccount)
        return self.__getStatsLine(self.__resultLabel('premiumVehicleXP'), xpWithoutPremiumColumn, freeXpWithoutPremiumColumn, xpWithPremiumColumn, freeXpWithPremiumColumn)

    @classmethod
    def _packAchievement(cls, achieve, isUnique = False):
        rank, i18nValue = (None, None)
        if achieve.getType() != ACHIEVEMENT_TYPE.SERIES:
            rank, i18nValue = achieve.getValue(), achieve.getI18nValue()
        icons = achieve.getIcons()
        specialIcon = icons.get(MarkOnGunAchievement.IT_95X85, None)
        customData = []
        recordName = achieve.getRecordName()
        if recordName == MARK_ON_GUN_RECORD:
            customData.extend([achieve.getDamageRating(), achieve.getVehicleNationID()])
        if recordName == MARK_OF_MASTERY_RECORD:
            customData.extend([achieve.getPrevMarkOfMastery(), achieve.getCompDescr()])
        return {'type': recordName[1],
         'block': achieve.getBlock(),
         'inactive': False,
         'icon': achieve.getSmallIcon() if specialIcon is None else '',
         'rank': rank,
         'localizedValue': i18nValue,
         'unic': isUnique,
         'rare': False,
         'title': achieve.getUserName(),
         'description': achieve.getUserDescription(),
         'rareIconId': None,
         'isEpic': achieve.hasRibbon(),
         'specialIcon': specialIcon,
         'customData': customData}

    def __populatePersonalMedals(self, pData, personalDataOutput):
        personalDataOutput['dossierType'] = None
        personalDataOutput['dossierCompDescr'] = None
        personalDataOutput['achievementsLeft'] = []
        personalDataOutput['achievementsRight'] = []
        for _, data in pData:
            achievementsData = data.get('dossierPopUps', [])
            for achievementId, achieveValue in achievementsData:
                record = DB_ID_TO_RECORD[achievementId]
                if record in IGNORED_BY_BATTLE_RESULTS or not isAchievementRegistered(record):
                    continue
                factory = getAchievementFactory(record)
                if factory is not None:
                    achieve = factory.create(value=achieveValue)
                    isMarkOnGun = record == MARK_ON_GUN_RECORD
                    if isMarkOnGun:
                        if 'typeCompDescr' in data:
                            achieve.setVehicleNationID(vehicles_core.parseIntCompactDescr(data['typeCompDescr'])[1])
                        if 'damageRating' in data:
                            achieve.setDamageRating(data['damageRating'])
                    achieveData = self._packAchievement(achieve, isUnique=True)
                    if achieve.getName() in achievements.BATTLE_ACHIEVES_RIGHT:
                        personalDataOutput['achievementsRight'].append(achieveData)
                    else:
                        personalDataOutput['achievementsLeft'].append(achieveData)

            markOfMastery = data.get('markOfMastery', 0)
            factory = getAchievementFactory(('achievements', 'markOfMastery'))
            if markOfMastery > 0 and factory is not None:
                from gui.shared import g_itemsCache
                achieve = factory.create(value=markOfMastery)
                achieve.setPrevMarkOfMastery(data.get('prevMarkOfMastery', 0))
                achieve.setCompDescr(data.get('typeCompDescr'))
                personalDataOutput['achievementsLeft'].append(self._packAchievement(achieve))
            personalDataOutput['achievementsRight'].sort(key=lambda k: k['isEpic'], reverse=True)

        return

    def __populateEfficiency(self, pData, pCommonData, playersData, commonData, personalDataOutput):
        valsStr = makeHtmlString('html_templates:lobby/battle_results', 'tooltip_params_style', {'text': i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_PARAMS_VAL)})
        details = []
        for techniquesGroup, enemiesGroup, basesGroup in self.__buildEfficiencyDataSource(pData, pCommonData, playersData, commonData):
            enemies = []
            for (vId, vIntCD), iInfo in enemiesGroup:
                result = {}
                accountDBID = self.dataProvider.getAccountDBID(vId)
                vehsData = self.dataProvider.getVehiclesData(accountDBID)
                deathReason = iInfo.get('deathReason', -1)
                if vehsData:
                    vInfo = vehsData[0]
                    deathReason = vInfo.get('deathReason', -1)
                _, result['vehicleName'], _, result['tankIcon'], result['balanceWeight'], _ = self.__getVehicleData(vIntCD)
                result['deathReason'] = deathReason
                result['spotted'] = iInfo.get('spotted', 0)
                result['piercings'] = iInfo.get('piercings', 0)
                result['damageDealt'] = iInfo.get('damageDealt', 0)
                playerNameData = self.__getPlayerName(accountDBID)
                result['playerFullName'] = playerNameData[0]
                result['playerName'], result['playerClan'], result['playerRegion'], _ = playerNameData[1]
                result['vehicleId'] = vId
                result['typeCompDescr'] = vIntCD
                result['killCount'] = iInfo.get('targetKills', 0)
                result['isAlly'] = False
                result['isFake'] = False
                result.update(self.__getDamageInfo(iInfo, valsStr))
                result.update(self.__getArmorUsingInfo(iInfo, valsStr))
                result.update(self.__getAssistInfo(iInfo, valsStr))
                result.update(self.__getCritsInfo(iInfo))
                enemies.append(result)

            enemies = sorted(enemies, cmp=self.__vehiclesComparator)
            details.append(techniquesGroup + enemies + basesGroup)

        personalDataOutput['details'] = details

    def __getDamageInfo(self, iInfo, valsStr):
        piercings = iInfo['piercings']
        damageInfo = {'damageTotalItems': piercings}
        if int(iInfo['damageDealt']) > 0:
            damageInfo['damageDealtVals'] = makeHtmlString('html_templates:lobby/battle_results', 'tooltip_two_liner', {'line1': BigWorld.wg_getIntegralFormat(iInfo['damageDealt']),
             'line2': BigWorld.wg_getIntegralFormat(piercings)})
            damageInfo['damageDealtNames'] = makeHtmlString('html_templates:lobby/battle_results', 'tooltip_two_liner', {'line1': i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_DAMAGE_PART1, vals=valsStr),
             'line2': i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_DAMAGE_PART2)})
        return damageInfo

    def __getArmorUsingInfo(self, iInfo, valsStr):
        usedArmorCount = iInfo.get('noDamageDirectHitsReceived', 0)
        damageBlocked = iInfo.get('damageBlockedByArmor', 0)
        armorUsingInfo = {'armorTotalItems': usedArmorCount}
        if usedArmorCount > 0 or damageBlocked > 0:
            armorUsingInfo['armorVals'] = makeHtmlString('html_templates:lobby/battle_results', 'tooltip_three_liner', {'line1': BigWorld.wg_getIntegralFormat(iInfo['rickochetsReceived']),
             'line2': BigWorld.wg_getIntegralFormat(iInfo['noDamageDirectHitsReceived']),
             'line3': BigWorld.wg_getIntegralFormat(damageBlocked)})
            armorUsingInfo['armorNames'] = makeHtmlString('html_templates:lobby/battle_results', 'tooltip_three_liner', {'line1': i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ARMOR_PART1),
             'line2': i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ARMOR_PART2),
             'line3': i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ARMOR_PART3, vals=valsStr)})
        return armorUsingInfo

    def __getAssistInfo(self, iInfo, valsStr):
        damageAssisted = iInfo.get('damageAssistedTrack', 0) + iInfo.get('damageAssistedRadio', 0)
        assistInfo = {'damageAssisted': damageAssisted}
        if damageAssisted > 0:
            assistInfo['damageAssistedVals'] = makeHtmlString('html_templates:lobby/battle_results', 'tooltip_three_liner', {'line1': BigWorld.wg_getIntegralFormat(iInfo['damageAssistedRadio']),
             'line2': BigWorld.wg_getIntegralFormat(iInfo['damageAssistedTrack']),
             'line3': BigWorld.wg_getIntegralFormat(damageAssisted)})
            assistInfo['damageAssistedNames'] = makeHtmlString('html_templates:lobby/battle_results', 'tooltip_three_liner', {'line1': i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ASSIST_PART1, vals=valsStr),
             'line2': i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ASSIST_PART2, vals=valsStr),
             'line3': i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ASSIST_TOTAL, vals=valsStr)})
        return assistInfo

    def __getCritsInfo(self, iInfo):
        destroyedTankmen = iInfo['crits'] >> 24 & 255
        destroyedDevices = iInfo['crits'] >> 12 & 4095
        criticalDevices = iInfo['crits'] & 4095
        critsCount = 0
        criticalDevicesList = []
        destroyedDevicesList = []
        destroyedTankmenList = []
        for shift in range(len(vehicles.VEHICLE_DEVICE_TYPE_NAMES)):
            if 1 << shift & criticalDevices:
                critsCount += 1
                criticalDevicesList.append(self.__makeTooltipModuleLabel(vehicles.VEHICLE_DEVICE_TYPE_NAMES[shift], 'Critical'))
            if 1 << shift & destroyedDevices:
                critsCount += 1
                destroyedDevicesList.append(self.__makeTooltipModuleLabel(vehicles.VEHICLE_DEVICE_TYPE_NAMES[shift], 'Destroyed'))

        for shift in range(len(vehicles.VEHICLE_TANKMAN_TYPE_NAMES)):
            if 1 << shift & destroyedTankmen:
                critsCount += 1
                destroyedTankmenList.append(self.__makeTooltipTankmenLabel(vehicles.VEHICLE_TANKMAN_TYPE_NAMES[shift]))

        return {'critsCount': BigWorld.wg_getIntegralFormat(critsCount),
         'criticalDevices': LINE_BRAKE_STR.join(criticalDevicesList),
         'destroyedDevices': LINE_BRAKE_STR.join(destroyedDevicesList),
         'destroyedTankmen': LINE_BRAKE_STR.join(destroyedTankmenList)}

    def __getBasesInfo(self, pData, commonData, enemies):
        capturePoints = pData.get('capturePoints', 0)
        defencePoints = pData.get('droppedCapturePoints', 0)
        techniquesGroup = []
        basesGroup = []
        if capturePoints > 0 or defencePoints > 0:
            arenaTypeID = commonData.get('arenaTypeID', None)
            arenaSubType = ''
            if arenaTypeID is not None:
                arenaSubType = getArenaSubTypeName(arenaTypeID)
            if len(enemies):
                techniqueLabelStr = BATTLE_RESULTS.COMMON_BATTLEEFFICIENCY_TECHNIQUE
                techniquesGroup = [{'groupLabel': text_styles.middleTitle(techniqueLabelStr)}]
            basesGroupLabelStr = BATTLE_RESULTS.COMMON_BATTLEEFFICIENCY_BASES
            basesGroup = [{'groupLabel': text_styles.middleTitle(basesGroupLabelStr)}]
            if arenaSubType == 'domination':
                label = i18n.makeString(BATTLE_RESULTS.COMMON_BATTLEEFFICIENCY_NEUTRALBASE)
                basesGroup.append(self.__makeBaseVO(label, capturePoints, defencePoints))
            else:
                if capturePoints > 0:
                    label = i18n.makeString(BATTLE_RESULTS.COMMON_BATTLEEFFICIENCY_ENEMYBASE)
                    basesGroup.append(self.__makeBaseVO(label, capturePoints, 0))
                if defencePoints > 0:
                    label = i18n.makeString(BATTLE_RESULTS.COMMON_BATTLEEFFICIENCY_ALLYBASE)
                    basesGroup.append(self.__makeBaseVO(label, 0, defencePoints))
        return (techniquesGroup, basesGroup)

    def __makeBaseVO(self, label, capturePoints, defencePoints):
        data = {'baseLabel': text_styles.standard(label),
         'captureTotalItems': capturePoints,
         'defenceTotalItems': defencePoints}
        if capturePoints > 0:
            data['captureVals'] = BigWorld.wg_getIntegralFormat(capturePoints)
            data['captureNames'] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_CAPTURE_TOTALPOINTS)
        if defencePoints > 0:
            data['defenceVals'] = BigWorld.wg_getIntegralFormat(defencePoints)
            data['defenceNames'] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_DEFENCE_TOTALPOINTS)
        return data

    def __makeTooltipModuleLabel(self, key, suffix):
        return makeHtmlString('html_templates:lobby/battle_results', 'tooltip_crit_label', {'image': '{0}{1}'.format(key, suffix),
         'value': i18n.makeString('#item_types:{0}/name'.format(key))})

    def __makeTooltipTankmenLabel(self, key):
        return makeHtmlString('html_templates:lobby/battle_results', 'tooltip_crit_label', {'image': '{0}Destroyed'.format(key),
         'value': i18n.makeString('#item_types:tankman/roles/{0}'.format(key))})

    @classmethod
    def __populateResultStrings(cls, commonData, pData, commonDataOutput, isFallout, isMultiTeamMode):
        bonusType = commonData.get('bonusType', 0)
        winnerTeam = commonData.get('winnerTeam', 0)
        finishReason = commonData.get('finishReason', 0)
        if not winnerTeam:
            status = 'tie'
            if isMultiTeamMode and isFallout:
                status = 'ended'
        elif winnerTeam == pData.get('team'):
            status = 'win'
        else:
            status = 'lose'
            if isMultiTeamMode and isFallout:
                status = 'ended'

        def _finishReasonFormatter(formatter, **kwargs):
            if finishReason == 1:
                return i18n.makeString(formatter.format(''.join([str(finishReason), str(status)])), **kwargs)
            return i18n.makeString(formatter.format(finishReason))

        if bonusType == ARENA_BONUS_TYPE.FORT_BATTLE:
            fortBuilding = pData.get('fortBuilding', {})
            buildTypeID, buildTeam = fortBuilding.get('buildTypeID'), fortBuilding.get('buildTeam')
            if status == 'tie':
                status = 'win' if buildTeam == pData.get('team') else 'lose'
            commonDataOutput['resultShortStr'] = 'clanBattle_%s' % status
            if buildTypeID is not None:
                buildingName = FortBuilding(typeID=buildTypeID).userName
            else:
                buildingName = ''
            if buildTeam == pData.get('team'):
                _frFormatter = lambda : i18n.makeString(CLAN_BATTLE_FINISH_REASON_DEF.format(''.join([str(1), str(status)])), buildingName=buildingName)
            else:
                _frFormatter = lambda : i18n.makeString(CLAN_BATTLE_FINISH_REASON_ATTACK.format(''.join([str(1), str(status)])), buildingName=buildingName)
        else:
            commonDataOutput['resultShortStr'] = status
            _frFormatter = lambda : _finishReasonFormatter(FINISH_REASON)
        if not isFallout:
            commonDataOutput['finishReasonStr'] = _frFormatter()
        else:
            falloutSubMode = 'multiteam' if isMultiTeamMode else 'classic'
            resultTemplate = '#battle_results:fallout/{submode}/{status}'.format(submode=falloutSubMode, status=status)
            if status != 'tie' and status != 'ended':
                finishReasonStr = 'points'
                if finishReason == FR.WIN_POINTS_CAP:
                    finishReasonStr = 'cap'
                elif finishReason == FR.EXTERMINATION:
                    finishReasonStr = 'extermination'
                resultTemplate += '/' + finishReasonStr
            commonDataOutput['finishReasonStr'] = i18n.makeString(resultTemplate)
        commonDataOutput['resultStr'] = RESULT_.format(status)
        return

    def __populateTankSlot(self, commonDataOutput, pData, pCommonData, isFallout):
        vehsData = []
        playerNameData = self.__getPlayerName(pCommonData.get('accountDBID', None))
        commonDataOutput['playerNameStr'], commonDataOutput['clanNameStr'], commonDataOutput['regionNameStr'], _ = playerNameData[1]
        commonDataOutput['playerFullNameStr'] = playerNameData[0]
        if len(pData) > 1 or isFallout:
            vehsData.append({'vehicleName': i18n.makeString(BATTLE_RESULTS.ALLVEHICLES),
             'tankIcon': RES_ICONS.MAPS_ICONS_LIBRARY_FALLOUTVEHICLESALL})
        for vehTypeCompDescr, data in pData:
            curVeh = {}
            curVeh['vehicleName'], _, curVeh['tankIcon'], _, _, nation = self.__getVehicleData(vehTypeCompDescr)
            killerID = data.get('killerID', 0)
            curVeh['killerID'] = killerID
            deathReason = data.get('deathReason', -1)
            curVeh['deathReason'] = deathReason
            isPrematureLeave = data.get('isPrematureLeave', False)
            curVeh['isPrematureLeave'] = isPrematureLeave
            curVeh['flag'] = nations.NAMES[nation]
            if isPrematureLeave:
                curVeh['vehicleStateStr'] = i18n.makeString(BATTLE_RESULTS.COMMON_VEHICLESTATE_PREMATURELEAVE)
            elif deathReason > -1:
                if vehTypeCompDescr and not isVehicleObserver(vehTypeCompDescr) and killerID:
                    curVeh['vehicleStateStr'] = i18n.makeString('#battle_results:common/vehicleState/dead{0}'.format(deathReason))
                    killerPlayerId = self.dataProvider.getAccountDBID(killerID)
                    curVeh['vehicleStatePrefixStr'] = '{0} ('.format(curVeh['vehicleStateStr'])
                    curVeh['vehicleStateSuffixStr'] = ')'
                    playerNameData = self.__getPlayerName(killerPlayerId)
                    curVeh['killerFullNameStr'] = playerNameData[0]
                    curVeh['killerNameStr'], curVeh['killerClanNameStr'], curVeh['killerRegionNameStr'], _ = playerNameData[1]
                else:
                    curVeh['vehicleStateStr'] = ''
                    curVeh['vehicleStatePrefixStr'], curVeh['vehicleStateSuffixStr'] = ('', '')
                    curVeh['killerFullNameStr'], curVeh['killerNameStr'] = ('', '')
                    curVeh['killerClanNameStr'], curVeh['killerRegionNameStr'] = ('', '')
            else:
                curVeh['vehicleStateStr'] = BATTLE_RESULTS.COMMON_VEHICLESTATE_ALIVE
            vehsData.append(curVeh)

        commonDataOutput['playerVehicles'] = vehsData
        return

    def __populateArenaData(self, commonData, pData, commonDataOutput, isFallout, isMultiTeamMode, isResource):
        arenaGuiType = self.dataProvider.getArenaGuiType()
        arenaType = self.dataProvider.getArenaType()
        if arenaGuiType == ARENA_GUI_TYPE.SORTIE:
            arenaGuiName = i18n.makeString(BATTLE_RESULTS.COMMON_BATTLETYPE_SORTIE)
        elif arenaGuiType == ARENA_GUI_TYPE.RANDOM:
            arenaGuiName = ARENA_TYPE.format(arenaType.gameplayName)
        elif arenaGuiType == ARENA_GUI_TYPE.EVENT_BATTLES:
            arenaGuiName = ARENA_SPECIAL_TYPE.format(arenaGuiType)
            if isResource:
                arenaGuiName += '/resource'
            elif isMultiTeamMode:
                arenaGuiName += '/multiteam'
        else:
            arenaGuiName = ARENA_SPECIAL_TYPE.format(arenaGuiType)
        commonDataOutput['arenaStr'] = ARENA_NAME_PATTERN.format(i18n.makeString(arenaType.name), i18n.makeString(arenaGuiName))
        createTime = commonData.get('arenaCreateTime')
        createTime = time_utils.makeLocalServerTime(createTime)
        commonDataOutput['arenaCreateTimeStr'] = BigWorld.wg_getShortDateFormat(createTime) + ' ' + BigWorld.wg_getShortTimeFormat(createTime)
        commonDataOutput['arenaCreateTimeOnlyStr'] = BigWorld.wg_getShortTimeFormat(createTime)
        commonDataOutput['arenaIcon'] = getArenaIcon(ARENA_SCREEN_FILE, arenaType, arenaGuiType)
        duration = commonData.get('duration', 0)
        minutes = int(duration / 60)
        seconds = int(duration % 60)
        commonDataOutput['duration'] = i18n.makeString(TIME_DURATION_STR, minutes, seconds)
        commonDataOutput['playerKilled'] = '-'
        if pData.get('killerID', 0):
            lifeTime = pData.get('lifeTime', 0)
            minutes = int(lifeTime / 60)
            seconds = int(lifeTime % 60)
            commonDataOutput['playerKilled'] = i18n.makeString(TIME_DURATION_STR, minutes, seconds)
        commonDataOutput['timeStats'] = []
        for key in TIME_STATS_KEYS:
            commonDataOutput['timeStats'].append({'label': i18n.makeString(TIME_STATS_KEY_BASE.format(key)),
             'value': commonDataOutput[key]})

    def __makeTeamDamageStr(self, data):
        tkills = data.get('tkills', 0)
        tdamageDealt = data.get('tdamageDealt', 0)
        tDamageStr = '/'.join([str(tkills), str(tdamageDealt)])
        if tkills > 0 or tdamageDealt > 0:
            tDamageStr = self.__makeRedLabel(tDamageStr)
        else:
            tDamageStr = makeHtmlString('html_templates:lobby/battle_results', 'empty_stat_value', {'value': tDamageStr})
        return tDamageStr

    def __makeSlashedValuesStr(self, data, firstKey, secondKey):
        val1 = data.get(firstKey, 0)
        val1Str = str(val1) if val1 else makeHtmlString('html_templates:lobby/battle_results', 'empty_stat_value', {'value': val1})
        val2 = data.get(secondKey, 0)
        val2Str = str(val2) if val2 else makeHtmlString('html_templates:lobby/battle_results', 'empty_stat_value', {'value': val2})
        if not val1 and not val2:
            slash = makeHtmlString('html_templates:lobby/battle_results', 'empty_stat_value', {'value': '/'})
        else:
            slash = '/'
        return slash.join([val1Str, val2Str])

    def __makeMileageStr(self, mileage):
        km = float(mileage) / 1000
        val = BigWorld.wg_getFractionalFormat(km) + i18n.makeString(MILEAGE_STR_KEY)
        if not mileage:
            val = makeHtmlString('html_templates:lobby/battle_results', 'empty_stat_value', {'value': val})
        return val

    def __populateTeamsData(self, pCommonData, playersData, commonData, commonDataOutput, avatarsData, isFallout, isMultiTeamMode):
        squads = defaultdict(dict)
        stat = defaultdict(list)
        teamsScore = defaultdict(int)
        lastSquadId = 0
        squadManCount = 0
        playerSquadId = 0
        arenaType = self.dataProvider.getArenaType()
        playerDBID = pCommonData.get('accountDBID')
        playerTeam = pCommonData.get('team')
        allTeams = set(range(1, arenaType.maxTeamsInArena + 1))
        enemyTeams = allTeams - {playerTeam}
        bonusType = self.dataProvider.getArenaBonusType()
        winnerTeam = commonData.get('winnerTeam', 0)
        finishReason = commonData.get('finishReason', 0)
        playerNamePosition = bonusType in (ARENA_BONUS_TYPE.FORT_BATTLE, ARENA_BONUS_TYPE.CYBERSPORT, ARENA_BONUS_TYPE.RATED_CYBERSPORT)
        isPlayerObserver = isVehicleObserver(pCommonData.get('typeCompDescr', 0))
        fairPlayViolationName = self.__getFairPlayViolationName(pCommonData)
        if isFallout and not isMultiTeamMode:
            isSolo = findFirst(lambda pData: pData['team'] == playerTeam, playersData.itervalues()) is None
            pointsKill, pointsFlags = getCosts(arenaType, isSolo)
            formatter = BigWorld.wg_getNiceNumberFormat
            scorePatterns = []
            if pointsKill > 0:
                costKillText = i18n.makeString(TOOLTIPS.BATTLERESULTS_VICTORYSCOREDESCRIPTION_COST, cost=formatter(pointsKill))
                scorePatterns.append(i18n.makeString(TOOLTIPS.BATTLERESULTS_VICTORYSCOREDESCRIPTION_KILLSPATTERN, pointsKill=costKillText))
            if pointsFlags:
                costFlagTextPatterns = []
                for c in pointsFlags:
                    costFlagTextPatterns.append(i18n.makeString(TOOLTIPS.BATTLERESULTS_VICTORYSCOREDESCRIPTION_COST, cost=formatter(c)))

                scorePatterns.append(i18n.makeString(TOOLTIPS.BATTLERESULTS_VICTORYSCOREDESCRIPTION_POINTSPATTERN, pointsFlag=', '.join(costFlagTextPatterns)))
            tooltipText = i18n.makeString(TOOLTIPS.BATTLERESULTS_VICTORYSCOREDESCRIPTION_BODY, scorePattern=';\n'.join(scorePatterns))
            isExtermination = finishReason == FR.EXTERMINATION
            playerVictory = playerTeam == winnerTeam
            enemyVictory = winnerTeam in enemyTeams
            alliesSpecialStatus = BATTLE_RESULTS.EXTERMINATIONVICTORY_ALLIES if playerVictory and isExtermination else ''
            enemiesSpecialStatus = BATTLE_RESULTS.EXTERMINATIONVICTORY_ENEMIES if enemyVictory and isExtermination else ''
            commonDataOutput['victoryScore'] = [{'score': 0,
              'victory': playerVictory,
              'tooltip': tooltipText,
              'specialStatusStr': alliesSpecialStatus}, {'score': 0,
              'victory': enemyVictory,
              'tooltip': tooltipText,
              'specialStatusStr': enemiesSpecialStatus}]
        isInfluencePointsAvailable = True
        teamResource = 0
        teamInfluence = 0
        for pId, pInfo in playersData.iteritems():
            vehsData = self.dataProvider.getVehiclesData(pId)
            vId = self.dataProvider.getVehicleID(pId)
            row = {'vehicleId': vId}
            isSelf = playerDBID == pId
            damageAssisted = []
            totalDamageAssisted = 0
            statValues = []
            totalStatValues = defaultdict(int)
            xp = 0
            damageDealt = 0
            achievementsData = []
            for data in vehsData:
                assisted = data.get('damageAssistedTrack', 0) + data.get('damageAssistedRadio', 0)
                damageAssisted.append(assisted)
                totalDamageAssisted += assisted
                xp += data.get('xp', 0) - data.get('achievementXP', 0)
                damageDealt += data.get('damageDealt', 0)
                statValues.append(self.__populateStatValues(data, isFallout, isSelf))
                achievementsData += data.get('achievements', [])
                for k, (d, func) in CUMULATIVE_STATS_DATA.iteritems():
                    if isFallout and k in FALLOUT_EXCLUDE_VEHICLE_STATS:
                        continue
                    if not isFallout and k in FALLOUT_ONLY_STATS:
                        continue
                    v = data.get(k, d)
                    totalStatValues.setdefault(k, d)
                    totalStatValues[k] = func(totalStatValues[k], v)

            damageAssisted.insert(0, totalDamageAssisted)
            totalStatValues['damageAssisted'] = totalDamageAssisted
            row['kills'] = kills = totalStatValues['kills']
            row['tkills'] = teamKills = totalStatValues['tkills']
            row['realKills'] = kills - teamKills
            row['xp'] = xp
            row['damageDealt'] = damageDealt
            if pId in avatarsData:
                curAvatarData = avatarsData[pId]
                self.__addOrderDataToTotalValue(avatarsData[pId], totalStatValues)
                row['damageDealt'] += curAvatarData['damageDealt']
                row['kills'] += curAvatarData['kills']
                row['realKills'] += curAvatarData['kills']
            statValues.insert(0, self.__populateStatValues(totalStatValues, isFallout, isSelf))
            row['statValues'] = statValues
            vehs = []
            vInfo = vehsData[0]
            team = pInfo['team']
            if len(vehsData) > 1 or isFallout:
                vehs.append({'label': i18n.makeString(BATTLE_RESULTS.ALLVEHICLES),
                 'icon': RES_ICONS.MAPS_ICONS_LIBRARY_FALLOUTVEHICLESALL})
                for vInfo in vehsData:
                    _, vehicleName, tankIcon, _, _, nation = self.__getVehicleData(vInfo.get('typeCompDescr', None))
                    vehs.append({'label': vehicleName,
                     'icon': tankIcon,
                     'flag': nations.NAMES[nation]})

            else:
                row['vehicleFullName'], row['vehicleName'], tankIcon, row['tankIcon'], _, _ = self.__getVehicleData(vInfo.get('typeCompDescr', None))
                vehs.append({'icon': tankIcon})
            row['vehicles'] = vehs
            if bonusType == ARENA_BONUS_TYPE.SORTIE:
                row['showResources'] = True
                if pInfo.get('clanDBID'):
                    resourceCount = vInfo.get('fortResource', 0)
                    row['resourceCount'] = resourceCount
                    if team == playerTeam:
                        teamResource += resourceCount
                else:
                    row['resourceCount'] = None
            else:
                row['showResources'] = False
            if team == playerTeam:
                influencePoints = vInfo.get('influencePoints')
                if influencePoints is not None and isInfluencePointsAvailable:
                    teamInfluence += influencePoints
                elif isInfluencePointsAvailable:
                    isInfluencePointsAvailable = False
            achievementsList = []
            if not (pId == playerDBID and fairPlayViolationName is not None):
                for achievementId in achievementsData:
                    record = DB_ID_TO_RECORD[achievementId]
                    factory = getAchievementFactory(record)
                    if factory is not None and isAchievementRegistered(record):
                        achive = factory.create(value=0)
                        if not achive.isApproachable():
                            achievementsList.append(self._packAchievement(achive, isUnique=True))

                achievementsList.sort(key=lambda k: k['isEpic'], reverse=True)
            row['achievements'] = achievementsList
            row['medalsCount'] = len(achievementsList)
            isVehObserver = isVehicleObserver(vInfo.get('typeCompDescr', 0))
            isPrematureLeave = vInfo.get('isPrematureLeave', False)
            isDead = findFirst(operator.itemgetter('stopRespawn'), vehsData) is not None and not isPrematureLeave
            row['isPrematureLeave'] = isPrematureLeave
            row['vehicleStateStr'] = ''
            row['killerID'] = 0
            if isFallout:
                row['deathReason'] = 0 if isDead else -1
                if isPrematureLeave:
                    row['vehicleStateStr'] = i18n.makeString(BATTLE_RESULTS.COMMON_VEHICLESTATE_PREMATURELEAVE)
            elif not isVehObserver:
                killerID = vInfo.get('killerID', 0)
                row['killerID'] = killerID
                deathReason = vInfo.get('deathReason', -1)
                row['deathReason'] = deathReason
                row['isPrematureLeave'] = isPrematureLeave
                if isPrematureLeave:
                    row['vehicleStateStr'] = i18n.makeString(BATTLE_RESULTS.COMMON_VEHICLESTATE_PREMATURELEAVE)
                elif deathReason > -1:
                    row['vehicleStateStr'] = ''
                    if killerID:
                        row['vehicleStateStr'] = i18n.makeString('#battle_results:common/vehicleState/dead{0}'.format(deathReason))
                        killerPlayerId = self.dataProvider.getAccountDBID(killerID)
                        row['vehicleStatePrefixStr'] = '{0} ('.format(row['vehicleStateStr'])
                        row['vehicleStateSuffixStr'] = ')'
                        playerNameData = self.__getPlayerName(killerPlayerId)
                        row['killerFullNameStr'] = playerNameData[0]
                        row['killerNameStr'], row['killerClanNameStr'], row['killerRegionNameStr'], _ = playerNameData[1]
                else:
                    row['vehicleStateStr'] = BATTLE_RESULTS.COMMON_VEHICLESTATE_ALIVE
            row['playerId'] = pId
            row['userName'] = pInfo.get('name')
            playerNameData = self.__getPlayerName(pId)
            playerName, playerClan, playerRegion, playerIgrType = playerNameData[1]
            row['playerName'] = playerName
            row['userVO'] = {'fullName': playerNameData[0],
             'userName': playerName,
             'clanAbbrev': playerClan,
             'region': playerRegion,
             'igrType': playerIgrType}
            row['playerNamePosition'] = playerNamePosition
            if isFallout:
                flagActions = totalStatValues['flagActions']
                row['falloutResourcePoints'] = totalStatValues['resourceAbsorbed']
                row['flags'] = flagActions[FLAG_ACTION.CAPTURED]
                row['deaths'] = totalStatValues['deathCount']
                row['deathsStr'] = self.__formatDeathsString(totalStatValues['deathCount'], isDead)
                playerScore = totalStatValues['winPoints']
                row['victoryScore'] = playerScore
                if isMultiTeamMode:
                    teamsScore[team] += playerScore
                else:
                    teamIdx = 0 if team == playerTeam else 1
                    commonDataOutput['victoryScore'][teamIdx]['score'] += playerScore
            row['isSelf'] = isSelf
            prebattleID = pInfo.get('prebattleID', 0)
            row['prebattleID'] = prebattleID
            if playerDBID == pId:
                playerSquadId = prebattleID
            if bonusType in (ARENA_BONUS_TYPE.REGULAR, ARENA_BONUS_TYPE.EVENT_BATTLES) and prebattleID:
                if not lastSquadId or lastSquadId != prebattleID:
                    squadManCount = 1
                    lastSquadId = prebattleID
                else:
                    squadManCount += 1
                if prebattleID not in squads[team].keys():
                    squads[team][prebattleID] = 1
                else:
                    squads[team][prebattleID] += 1
            if not (isPlayerObserver and isVehObserver):
                stat[team].append(row)

        processSquads = bonusType in (ARENA_BONUS_TYPE.REGULAR, ARENA_BONUS_TYPE.EVENT_BATTLES) and not (IS_DEVELOPMENT and squadManCount == len(playersData))
        for team, data in stat.iteritems():
            data = sorted(data, cmp=self.__vehiclesComparator)
            sortIdx = len(data)
            if processSquads:
                squadsSorted = sorted(squads[team].iteritems(), cmp=lambda x, y: cmp(x[0], y[0]))
                teamSquads = [ id for id, num in squadsSorted if 1 < num < 4 ]
            for item in data:
                item['vehicleSort'] = sortIdx
                item['xpSort'] = item.get('xp', 0)
                sortIdx -= 1
                if processSquads:
                    prbID = item.get('prebattleID')
                    item['isOwnSquad'] = playerSquadId == prbID if playerSquadId != 0 else False
                    item['squadID'] = teamSquads.index(prbID) + 1 if prbID in teamSquads else 0
                else:
                    item['squadID'] = 0
                    item['isOwnSquad'] = False

            if team == playerTeam:
                commonDataOutput['totalFortResourceStr'] = makeHtmlString('html_templates:lobby/battle_results', 'teamResourceTotal', {'resourceValue': teamResource})
                if isInfluencePointsAvailable:
                    commonDataOutput['totalInfluenceStr'] = makeHtmlString('html_templates:lobby/battle_results', 'teamInfluenceTotal', {'resourceValue': teamInfluence})

        team1 = []
        team2 = []
        if isMultiTeamMode:
            squadIdx = 0
            for t in allTeams:
                teamData = stat.get(t, [])
                squadIdxIsSet = False
                for playerData in teamData:
                    if playerData['squadID'] > 0:
                        if not squadIdxIsSet:
                            squadIdx += 1
                            squadIdxIsSet = True
                        playerData['squadID'] = squadIdx
                    playerData['teamScore'] = teamsScore[t]

                team1.extend(teamData)

        else:
            team1 = stat[playerTeam]
            map(lambda teamID: team2.extend(stat[teamID]), enemyTeams)
        return (team1, team2)

    def __addOrderDataToTotalValue(self, avatarData, resultDict):
        if 'damageDealt' in avatarData and 'kills' in avatarData:
            damageByOrder = avatarData['damageDealt']
            killsByOrder = avatarData['kills']
            resultDict['damageDealt'] += damageByOrder
            resultDict['kills'] += killsByOrder
            resultDict['damaged'] = avatarData['totalDamaged']
            resultDict['damagedByOrder'] = avatarData['damaged']
            resultDict['damageDealtByOrder'] = damageByOrder
            resultDict['killsByOrder'] = killsByOrder

    def __formatDeathsString(self, deathCount, isDead):
        if isDead:
            result = text_styles.critical(str(deathCount))
        else:
            result = text_styles.standard(str(deathCount))
        return result

    def __calculateTotalCredits(self, pData, eventCredits, premCreditsFactor, isPremium, aogasFactor, baseCredits, baseOrderCredits, baseBoosterCredits, creditsToDraw, creditsPenalty, creditsCompensation, hasViolation, usePremFactor = False):
        premFactor = premCreditsFactor if usePremFactor else 1.0
        givenCredits = pData['credits']
        credits = int(givenCredits - round(creditsToDraw * premFactor))
        if isPremium != usePremFactor:
            givenCredits = 0
            if not hasViolation:
                givenCredits = (int(round(baseCredits * premFactor)) + int(round(baseOrderCredits * premFactor)) + int(round(baseBoosterCredits * premFactor)) + int(round(eventCredits * premFactor))) * aogasFactor
            credits = int(givenCredits - round(creditsToDraw * premFactor * aogasFactor) - int(round(creditsPenalty * premFactor * aogasFactor)) + int(round(creditsCompensation * premFactor * aogasFactor)))
        return credits

    def __calculateTotalFreeXp(self, pData, aogasFactor, premXpFactor, igrXpFactor, refSystemFactor, isPremium, baseFreeXp, dailyFreeXp, baseOrderFreeXp, baseBoosterFreeXP, eventFreeXP, hasViolation, usePremFactor = False):
        if hasViolation:
            return 0
        freeXP = float(pData['freeXP'])
        if isPremium != usePremFactor:
            premXpFactor = premXpFactor if usePremFactor else 1.0
            subtotalXp = int(round(int(round(baseFreeXp * premXpFactor)) * igrXpFactor))
            resultXp = int(round(int(round(dailyFreeXp * premXpFactor)) * igrXpFactor))
            if abs(refSystemFactor - 1.0) > 0.001:
                resultXp += int(round(subtotalXp * refSystemFactor))
            freeXP = int(round((resultXp + int(round(baseOrderFreeXp * premXpFactor)) + int(round(baseBoosterFreeXP * premXpFactor)) + int(round(eventFreeXP * premXpFactor))) * aogasFactor))
        return freeXP

    def __calculateTotalXp(self, pData, aogasFactor, premXpFactor, igrXpFactor, refSystemFactor, isPremium, baseXp, dailyXP, xpPenalty, baseOrderXp, baseBoosterXP, eventXP, hasViolation, usePremFactor = False):
        if hasViolation:
            return 0
        xp = pData['xp']
        if isPremium != usePremFactor:
            premFactor = premXpFactor if usePremFactor else 1.0
            if isPremium:
                premiumVehicleXP = pData['premiumVehicleXP'] / premFactor
            else:
                premiumVehicleXP = pData['premiumVehicleXP'] * premFactor
            subtotalXp = int(round(int(round((baseXp - xpPenalty) * premFactor)) * igrXpFactor))
            resultXp = int(round(int(round(dailyXP * premFactor)) * igrXpFactor))
            if abs(refSystemFactor - 1.0) > 0.001:
                resultXp += int(round(subtotalXp * refSystemFactor))
            xp = int(round(resultXp + int(round(baseOrderXp * premFactor)) + int(round(baseBoosterXP * premFactor)) + int(round(eventXP * premFactor)) + int(round(premiumVehicleXP * aogasFactor))))
        return xp

    def __calculateBaseCreditsPenalty(self, pData, isPremium):
        creditsPenalty = pData.get('creditsPenalty', 0) + pData.get('creditsContributionOut', 0)
        if isPremium:
            premFactor = pData.get('premiumCreditsFactor10', 10) / 10.0
            creditsPenalty = math.ceil(creditsPenalty / premFactor)
        return creditsPenalty

    def __calculateBaseParam(self, paramKey, pData, premFactor, isPremium):
        paramValue = pData.get(paramKey, 0)
        if isPremium:
            paramValue = int(paramValue / premFactor)
        return paramValue

    def __calculateParamWithPrem(self, paramKey, pData, premFactor, isPremium):
        paramValue = pData.get(paramKey, 0)
        if not isPremium:
            paramValue = int(round(paramValue * premFactor))
        return paramValue

    def selectVehicle(self, inventoryId):
        g_currentVehicle.selectVehicle(inventoryId)
        return g_currentVehicle.invID == inventoryId

    @classmethod
    def __parseQuestsProgress(cls, personalData):
        questsProgress = {}
        for _, data in personalData:
            questsProgress.update(data.get('questsProgress', {}))

        if not questsProgress:
            return
        else:

            def _isFortQuest(q):
                return q.getType() == EVENT_TYPE.FORT_QUEST

            def _sortCommonQuestsFunc(aData, bData):
                aQuest, aCurProg, aPrevProg, _, _ = aData
                bQuest, bCurProg, bPrevProg, _, _ = bData
                res = cmp(aQuest.isCompleted(aCurProg), bQuest.isCompleted(bCurProg))
                if res:
                    return -res
                res = cmp(_isFortQuest(aQuest), _isFortQuest(bQuest))
                if res:
                    return -res
                if aQuest.isCompleted() and bQuest.isCompleted(bCurProg):
                    res = aQuest.getBonusCount(aCurProg) - aPrevProg.get('bonusCount', 0) - (bQuest.getBonusCount(bCurProg) - bPrevProg.get('bonusCount', 0))
                    if not res:
                        return res
                return cmp(aQuest.getID(), bQuest.getID())

            from gui.Scaleform.daapi.view.lobby.server_events import events_helpers
            quests = g_eventsCache.getQuests()
            commonQuests, potapovQuests = [], {}
            for qID, qProgress in questsProgress.iteritems():
                pGroupBy, pPrev, pCur = qProgress
                isCompleted = pCur.get('bonusCount', 0) - pPrev.get('bonusCount', 0) > 0
                if qID in quests:
                    quest = quests[qID]
                    isProgressReset = not isCompleted and quest.bonusCond.isInRow() and pCur.get('battlesCount', 0) == 0
                    if pPrev or max(pCur.itervalues()) != 0:
                        commonQuests.append((quest,
                         {pGroupBy: pCur},
                         {pGroupBy: pPrev},
                         isProgressReset,
                         isCompleted))
                elif potapov_quests.g_cache.isPotapovQuest(qID):
                    pqID = potapov_quests.g_cache.getPotapovQuestIDByUniqueID(qID)
                    quest = g_eventsCache.potapov.getQuests()[pqID]
                    progress = potapovQuests.setdefault(quest, {})
                    progress.update({qID: isCompleted})

            formatted = []
            for e, data in sorted(potapovQuests.items(), key=operator.itemgetter(0)):
                if data.get(e.getAddQuestID(), False):
                    complete = (True, True)
                elif data.get(e.getMainQuestID(), False):
                    complete = (True, False)
                else:
                    complete = (False, False)
                info = events_helpers.getEventPostBattleInfo(e, quests, None, None, False, complete)
                if info is not None:
                    formatted.append(info)

            for e, pCur, pPrev, reset, complete in sorted(commonQuests, cmp=_sortCommonQuestsFunc):
                info = events_helpers.getEventPostBattleInfo(e, quests, pCur, pPrev, reset, complete)
                if info is not None:
                    formatted.append(info)

            return formatted

    @async
    @process
    def __getCommonData(self, callback):
        provider = yield self.dataProvider.request()
        if provider.isSynced():
            results = provider.getResults()
        else:
            results = None
        LOG_DEBUG('Player got battle results', self.dataProvider, results)
        if results:
            personalDataSource = results.get('personal', {}).copy()
            avatarsData = results.pop('avatars', {})
            personalCommonData = personalDataSource.values()[0]
            playerID = personalCommonData['accountDBID']
            personalData = []
            for vehicleData in self.dataProvider.getVehiclesData(playerID):
                vehTypeCD = vehicleData['typeCompDescr']
                personalData.append((vehTypeCD, personalDataSource[vehTypeCD]))

            playersData = results.get('players', {}).copy()
            commonData = results.get('common', {}).copy()
            bonusType = commonData.get('bonusType', 0)
            personalDataOutput = {}
            commonDataOutput = {}
            commonDataOutput['bonusType'] = bonusType
            if bonusType == ARENA_BONUS_TYPE.SORTIE or bonusType == ARENA_BONUS_TYPE.FORT_BATTLE:
                commonDataOutput['clans'] = self.__processClanData(personalCommonData, playersData)
            else:
                commonDataOutput['clans'] = {'allies': {'clanDBID': -1,
                            'clanAbbrev': ''},
                 'enemies': {'clanDBID': -1,
                             'clanAbbrev': ''}}
            commonDataOutput['battleResultsSharingIsAvailable'] = self._isSharingBtnEnabled()
            arenaType = self.dataProvider.getArenaType()
            arenaBonusType = self.dataProvider.getArenaBonusType()
            isFallout = self.dataProvider.getArenaGuiType() == ARENA_GUI_TYPE.EVENT_BATTLES
            teams = {}
            for pInfo in playersData.itervalues():
                team = pInfo['team']
                if team not in teams:
                    teams[team] = pInfo['prebattleID']

            isMultiTeamMode = arenaType.maxTeamsInArena > TEAMS_IN_ARENA.MIN_TEAMS
            isFFA = findFirst(lambda prbID: prbID > 0, teams.itervalues()) is None
            isResource = hasResourcePoints(arenaType, arenaBonusType)
            statsSorting = AccountSettings.getSettings('statsSorting' if bonusType != ARENA_BONUS_TYPE.SORTIE else 'statsSortingSortie')
            if isFallout:
                commonDataOutput['iconType'] = 'victoryScore'
                commonDataOutput['sortDirection'] = 'descending'
            else:
                commonDataOutput['iconType'] = statsSorting.get('iconType')
                commonDataOutput['sortDirection'] = statsSorting.get('sortDirection')
            damageAssisted = []
            totalDamageAssisted = 0
            statValues = []
            totalStatValues = defaultdict(int)
            for _, data in personalData:
                assisted = data.get('damageAssistedTrack', 0) + data.get('damageAssistedRadio', 0)
                damageAssisted.append(assisted)
                totalDamageAssisted += assisted
                statValues.append(self.__populateStatValues(data, isFallout, True))
                for k, (d, func) in CUMULATIVE_STATS_DATA.iteritems():
                    if isFallout and k in FALLOUT_EXCLUDE_VEHICLE_STATS:
                        continue
                    if not isFallout and k in FALLOUT_ONLY_STATS:
                        continue
                    v = data.get(k, d)
                    totalStatValues.setdefault(k, d)
                    totalStatValues[k] = func(totalStatValues[k], v)

            damageAssisted.insert(0, totalDamageAssisted)
            personalDataOutput['damageAssisted'] = damageAssisted
            totalStatValues['damageAssisted'] = totalDamageAssisted
            if playerID in avatarsData:
                self.__addOrderDataToTotalValue(avatarsData[playerID], totalStatValues)
            statValues.insert(0, self.__populateStatValues(totalStatValues, isFallout, True))
            personalDataOutput['statValues'] = statValues
            self.__populateResultStrings(commonData, personalCommonData, commonDataOutput, isFallout, isMultiTeamMode)
            self.__populatePersonalMedals(personalData, personalDataOutput)
            self.__populateArenaData(commonData, personalCommonData, commonDataOutput, isFallout, isMultiTeamMode, isResource)
            self.__populateAccounting(commonData, personalCommonData, personalData, playersData, personalDataOutput, isFallout)
            self.__populateTankSlot(commonDataOutput, personalData, personalCommonData, isFallout)
            self.__populateEfficiency(personalData, personalCommonData, playersData, commonData, personalDataOutput)
            team1, team2 = self.__populateTeamsData(personalCommonData, playersData, commonData, commonDataOutput, avatarsData, isFallout, isMultiTeamMode)
            resultingVehicles = []
            falloutMode = ''
            if isFallout:
                if isResource:
                    falloutMode = 'points'
                else:
                    falloutMode = 'flags'
            commonDataOutput['falloutMode'] = falloutMode
            commonDataOutput['wasInBattle'] = self.dataProvider.wasInBattle(getAccountDatabaseID())
            if isMultiTeamMode:
                tabInfo = [{'label': MENU.FINALSTATISTIC_TABS_COMMONSTATS,
                  'linkage': 'CommonStats',
                  'showWndBg': False}, {'label': MENU.FINALSTATISTIC_TABS_TEAMSTATS,
                  'linkage': 'MultiteamStatsUI',
                  'showWndBg': False}, {'label': MENU.FINALSTATISTIC_TABS_DETAILSSTATS,
                  'linkage': 'detailsStatsScrollPane',
                  'showWndBg': True}]
            else:
                tabInfo = [{'label': MENU.FINALSTATISTIC_TABS_COMMONSTATS,
                  'linkage': 'CommonStats',
                  'showWndBg': False}, {'label': MENU.FINALSTATISTIC_TABS_TEAMSTATS,
                  'linkage': 'TeamStatsUI',
                  'showWndBg': False}, {'label': MENU.FINALSTATISTIC_TABS_DETAILSSTATS,
                  'linkage': 'detailsStatsScrollPane',
                  'showWndBg': True}]
            textData = {'windowTitle': i18n.makeString(MENU.FINALSTATISTIC_WINDOW_TITLE),
             'shareButtonLabel': i18n.makeString(BATTLE_RESULTS.COMMON_RESULTSSHAREBTN),
             'shareButtonTooltip': i18n.makeString(TOOLTIPS.BATTLERESULTS_FORTRESOURCE_RESULTSSHAREBTN)}
            results = {'personal': personalDataOutput,
             'common': commonDataOutput,
             'team1': team1,
             'team2': team2,
             'textData': textData,
             'vehicles': resultingVehicles,
             'quests': self.__parseQuestsProgress(personalData),
             'unlocks': self.__getVehicleProgress(self.dataProvider.getArenaUniqueID(), personalData),
             'tabInfo': tabInfo,
             'isFreeForAll': isFFA}
            if self.dataProvider.results:
                self.dataProvider.results.updateViewData(results)
            callback(results)
        else:
            callback(None)
        return

    def getTeamEmblem(self, uid, clubDbID, isUseHtmlWrap):
        if self._isRated7x7Battle():
            results = self.dataProvider.results
            results.requestTeamInfo(clubDbID == results.getOwnClubDbID(), partial(self._onTeamInfoReceived, uid, isUseHtmlWrap))

    def _onTeamInfoReceived(self, uid, useWrap, teamInfo):
        if not self.isDisposed() and teamInfo:
            teamInfo.requestEmblemID(partial(self._onTeamEmblemReceived, uid, useWrap, teamInfo))

    def _onTeamEmblemReceived(self, uid, useWrap, teamInfo, emblemID):
        if not self.isDisposed() and emblemID:
            self.as_setTeamInfoS(uid, _wrapEmblemUrl(emblemID) if useWrap else emblemID, teamInfo.getUserName())

    @process
    def getClanEmblem(self, uid, clanDBID):
        clanEmblem = yield g_clanCache.getClanEmblemTextureID(clanDBID, False, uid)
        if not self.isDisposed():
            self.as_setClanEmblemS(uid, _wrapEmblemUrl(clanEmblem))

    def onTeamCardClick(self, teamDBID):
        club_events.showClubProfile(long(teamDBID))

    def onResultsSharingBtnPress(self):
        raise NotImplemented

    def _isSharingBtnEnabled(self):
        results = self.dataProvider.getResults()
        if results is not None:
            isSubUrlAvailable = 'uniqueSubUrl' in results and results['uniqueSubUrl'] is not None
            return GUI_SETTINGS.postBattleExchange.enabled and isSubUrlAvailable and results['common']['guiType'] not in (ARENA_GUI_TYPE.FORT_BATTLE,)
        else:
            return False

    def __processClanData(self, personalData, playersData):
        clans = []
        resClans = {'allies': {'clanDBID': -1,
                    'clanAbbrev': ''},
         'enemies': {'clanDBID': -1,
                     'clanAbbrev': ''}}
        for pId, pInfo in playersData.iteritems():
            clanDBID = pInfo.get('clanDBID')
            if clanDBID and clanDBID not in clans:
                clans.append(clanDBID)
                resClans['allies' if pInfo.get('team') == personalData.get('team') else 'enemies'] = {'clanDBID': clanDBID,
                 'clanAbbrev': i18n.makeString(BATTLE_RESULTS.COMMON_CLANABBREV, clanAbbrev=pInfo.get('clanAbbrev'))}

        return resClans

    def __getFairPlayViolationName(self, pData):
        fairPlayViolationData = pData.get('fairplayViolations')
        if fairPlayViolationData is not None:
            return getFairPlayViolationName(fairPlayViolationData[1])
        else:
            return

    def __showDivisionAnimation(self, curDivision, prevDivision):
        uniqueKey = (self.dataProvider.getArenaUniqueID(), curDivision, prevDivision)
        if uniqueKey in self.__rated7x7Animations:
            return
        self.__rated7x7Animations.add(uniqueKey)
        curLeague, prevLeague = getLeagueByDivision(curDivision), getLeagueByDivision(prevDivision)
        if curLeague < prevLeague:
            animationType = CYBER_SPORT_ALIASES.CS_ANIMATION_LEAGUE_UP
        elif curDivision > prevDivision:
            if getDivisionWithinLeague(curDivision) == 0:
                animationType = CYBER_SPORT_ALIASES.CS_ANIMATION_LEAGUE_DIVISION_UP_ALT
            else:
                animationType = CYBER_SPORT_ALIASES.CS_ANIMATION_LEAGUE_DIVISION_UP_ALT
        else:
            animationType = CYBER_SPORT_ALIASES.CS_ANIMATION_LEAGUE_DIVISION_DOWN
        if animationType != CYBER_SPORT_ALIASES.CS_ANIMATION_LEAGUE_DIVISION_DOWN:
            divAddSource = battle_res_fmts.getAnimationDivisionIcon(curLeague, curDivision)
        else:
            divAddSource = ''
        if curDivision > prevDivision:
            description = i18n.makeString(CYBERSPORT.CSANIMATION_DESCRIPTION)
        else:
            description = ''
        self.as_setAnimationS({'headerText': i18n.makeString(CYBERSPORT.CSANIMATION_HEADER),
         'descriptionText': description,
         'applyBtnLabel': CYBERSPORT.CSANIMATION_APPLYBTN_LABEL,
         'animationType': animationType,
         'leavesOldSource': battle_res_fmts.getAnimationLeavesIcon(prevLeague, prevDivision),
         'leavesNewSource': battle_res_fmts.getAnimationLeavesIcon(curLeague, curDivision),
         'ribbonOldSource': battle_res_fmts.getAnimationRibbonIcon(prevLeague, prevDivision),
         'ribbonNewSource': battle_res_fmts.getAnimationRibbonIcon(curLeague, curDivision),
         'divisionOldSource': battle_res_fmts.getAnimationDivisionIcon(prevLeague, prevDivision),
         'divisionNewSource': battle_res_fmts.getAnimationDivisionIcon(curLeague, curDivision),
         'logoOldSource': battle_res_fmts.getAnimationLogoIcon(prevLeague, prevDivision),
         'logoNewSource': battle_res_fmts.getAnimationLogoIcon(curLeague, curDivision),
         'divisionAdditionalSource': divAddSource})

    def startCSAnimationSound(self, soundEffectID = 'cs_animation_league_up'):
        self.app.soundManager.playEffectSound(soundEffectID)

    def _isRated7x7Battle(self):
        return self.dataProvider.getArenaBonusType() == ARENA_BONUS_TYPE.RATED_CYBERSPORT

    def __getVehicleProgress(self, arenaUniqueID, personalData):
        progressList = g_vehicleProgressCache.getVehicleProgressList(arenaUniqueID)
        if progressList is None:
            for _, data in personalData:
                vehTypeCompDescr = data.get('typeCompDescr')
                vehicleBattleXp = data.get('xp', 0)
                pureCreditsReceived = data.get('pureCreditsReceived', 0)
                tmenXps = dict(data.get('xpByTmen', []))
                progressHelper = VehicleProgressHelper(vehTypeCompDescr)
                progressList = progressHelper.getProgressList(vehicleBattleXp, pureCreditsReceived, tmenXps)
                progressHelper.clear()
                g_vehicleProgressCache.saveVehicleProgress(arenaUniqueID, progressList)

        return progressList

    def showUnlockWindow(self, itemId, unlockType):
        if unlockType in (PROGRESS_ACTION.RESEARCH_UNLOCK_TYPE, PROGRESS_ACTION.PURCHASE_UNLOCK_TYPE):
            showResearchView(itemId)
            self.onWindowClose()
        elif unlockType == PROGRESS_ACTION.NEW_SKILL_UNLOCK_TYPE:
            showPersonalCase(itemId, 2)

    def __onPremiumBought(self, event):
        arenaUniqueID = event.ctx.get('arenaUniqueID')
        if arenaUniqueID and arenaUniqueID not in self.__buyPremiumCache:
            self.__buyPremiumCache.add(arenaUniqueID)
            if arenaUniqueID == self.dataProvider.getArenaUniqueID():
                SystemMessages.g_instance.pushI18nMessage('#system_messages:premium/post_battle_premium', type=SystemMessages.SM_TYPE.Information, priority=NotificationPriorityLevel.MEDIUM, **self.__premiumBonusesDiff)
                self.__showStats()
        elif event.ctx.get('becomePremium', False):
            self.__showStats()

    def __showStats(self):
        results = self.dataProvider.getResults()
        self.onWindowClose()
        showBattleResultsFromData(results)
# okay decompyling c:\Users\PC\wotsources\files\originals\res\scripts\client\gui\scaleform\daapi\view\battleresultswindow.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:26:16 St�edn� Evropa (b�n� �as)
