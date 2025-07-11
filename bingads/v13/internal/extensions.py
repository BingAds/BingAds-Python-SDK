from datetime import datetime

from bingads.v13.internal.bulk.string_table import _StringTable
import re
import json
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

target_setting_detail_pattern=r'^(Age|Audience|CompanyName|Gender|Industry|JobFunction)$'

DELETE_VALUE = "delete_value"
_BULK_DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'
_BULK_DATETIME_FORMAT_2 = '%m/%d/%Y %H:%M:%S.%f'
_BULK_DATE_FORMAT = "%m/%d/%Y"

url_splitter = r';\s*(?=https?://)'
custom_param_splitter = r'(?<!\\);\s*'
custom_param_pattern = r'^\{_(.*?)\}=(.*$)'
combine_rule_pattern = r'^(And|Or|Not)\(([\d|\s|,]*?)\)$'

AdEditorialStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('AdEditorialStatus')
AdStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('AdStatus')
AssetGroupStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('AssetGroupStatus')
AdGroupStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('AdGroupStatus')
AssetGroupEditorialStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('AssetGroupEditorialStatus')
AdExtensionStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('AdExtensionStatus')
EntityScope = _CAMPAIGN_OBJECT_FACTORY_V13.create('EntityScope')
Network = _CAMPAIGN_OBJECT_FACTORY_V13.create('Network')
Minute = _CAMPAIGN_OBJECT_FACTORY_V13.create('Minute')
Day = _CAMPAIGN_OBJECT_FACTORY_V13.create('Day')
BusinessGeoCodeStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('BusinessGeoCodeStatus')
BidOption = _CAMPAIGN_OBJECT_FACTORY_V13.create('BidOption')
CallToAction = _CAMPAIGN_OBJECT_FACTORY_V13.create('CallToAction')
MatchType = _CAMPAIGN_OBJECT_FACTORY_V13.create('MatchType')
KeywordEditorialStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('KeywordEditorialStatus')
KeywordStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('KeywordStatus')
BudgetLimitType = _CAMPAIGN_OBJECT_FACTORY_V13.create('BudgetLimitType')
CampaignStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('CampaignStatus')
DynamicSearchAdsSetting = _CAMPAIGN_OBJECT_FACTORY_V13.create('DynamicSearchAdsSetting')
Webpage = _CAMPAIGN_OBJECT_FACTORY_V13.create('Webpage')
WebpageConditionOperand = _CAMPAIGN_OBJECT_FACTORY_V13.create('WebpageConditionOperand')

RemarketingRule = _CAMPAIGN_OBJECT_FACTORY_V13.create('RemarketingRule')
PageVisitorsRule = _CAMPAIGN_OBJECT_FACTORY_V13.create('PageVisitorsRule')
PageVisitorsWhoVisitedAnotherPageRule = _CAMPAIGN_OBJECT_FACTORY_V13.create('PageVisitorsWhoVisitedAnotherPageRule')
PageVisitorsWhoDidNotVisitAnotherPageRule = _CAMPAIGN_OBJECT_FACTORY_V13.create('PageVisitorsWhoDidNotVisitAnotherPageRule')
CustomEventsRule = _CAMPAIGN_OBJECT_FACTORY_V13.create('CustomEventsRule')
StringOperator = _CAMPAIGN_OBJECT_FACTORY_V13.create('StringOperator')
NumberOperator = _CAMPAIGN_OBJECT_FACTORY_V13.create('NumberOperator')
NormalForm = _CAMPAIGN_OBJECT_FACTORY_V13.create('NormalForm')

AudienceCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('AudienceCriterion')
BidMultiplier = _CAMPAIGN_OBJECT_FACTORY_V13.create('BidMultiplier')
CashbackAdjustment = _CAMPAIGN_OBJECT_FACTORY_V13.create('CashbackAdjustment')

AgeCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('AgeCriterion')
DayTimeCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('DayTimeCriterion')
DeviceCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('DeviceCriterion')
GenderCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('GenderCriterion')
HotelAdvanceBookingWindowCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('HotelAdvanceBookingWindowCriterion')
HotelCheckInDateCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('HotelCheckInDateCriterion')
GenreCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('GenreCriterion')
HotelCheckInDayCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('HotelCheckInDayCriterion')
HotelDateSelectionTypeCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('HotelDateSelectionTypeCriterion')
HotelLengthOfStayCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('HotelLengthOfStayCriterion')
LocationCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('LocationCriterion')
LocationIntentCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('LocationIntentCriterion')
RadiusCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('RadiusCriterion')
DealCriterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('DealCriterion')
TargetSetting_Type = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('TargetSetting'))
HotelSetting_Type = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('HotelSetting'))
CoOpSetting_Type = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('CoOpSetting'))
TextAsset_Type = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('TextAsset'))
ImageAsset_Type = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('ImageAsset'))
VideoAsset_Type = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('VideoAsset'))
CampaignAssociation = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('CampaignAssociation'))


def bulk_str(value):
    if value is None or (hasattr(value, 'value') and value.value is None):
        return None
    if isinstance(value, str):
        return value
    return str(value)


def bulk_upper_str(value):
    s = bulk_str(value)
    if s is None:
        return None
    return s.upper()

def to_verified_tracking_setting_string(value):
    if value is None:
        return None

    result = []
    for s in value:
        contracts = []
        for setting in s:
            if setting is not None and setting.__contains__('key') and setting.__contains__('value'):
                contract = {}
                contract['key'] = setting['key']
                contract['value'] = setting['value']
            contracts.append(contract)
        result.append(contracts)

    return json.dumps(result)

def parse_verified_tracking_setting(str):
    if str is None or str == '':
        return

    two_dims_array = []
    results = json.loads(str)
    for result in results:
        array = []
        for res in result:
            if res is not None and res.__contains__('key') and res.__contains__('value'):
                kv = _CAMPAIGN_OBJECT_FACTORY_V13.create('ns1:KeyValuePairOfstringstring')
                kv['key'] = res['key']
                kv['value'] = res['value']
                array.append(kv)
        two_dims_array.append(array)

    return two_dims_array

def bulk_date_str(value):
    if value is None or (value.Day is None and value.Month is None and value.Year is None):
        return None
    return '{0!s}/{1!s}/{2!s}'.format(value.Month, value.Day, value.Year)


def bulk_datetime_str(value):
    if value is None:
        return None
    return value.strftime(_BULK_DATETIME_FORMAT)


def csv_to_field_Date(entity, property_name, value):
    date = parse_date(value)
    if date is not None:
        setattr(entity, property_name, date)

def _is_daily_budget(budget_type):
    if budget_type.lower() == 'DailyBudgetAccelerated'.lower() \
            or budget_type.lower() == 'DailyBudgetStandard'.lower():
        return True
    else:
        return False

def csv_to_budget(row_values, bulk_campaign):
    success, budget_type = row_values.try_get_value(_StringTable.BudgetType)
    if not success or not budget_type:
        return

    success, budget_row_value = row_values.try_get_value(_StringTable.Budget)
    if not success:
        return
    budget_value = float(budget_row_value) if budget_row_value else None

    bulk_campaign.campaign.BudgetType = budget_type
    bulk_campaign.campaign.DailyBudget = budget_value


def budget_to_csv(bulk_campaign, row_values):
    budget_type = bulk_campaign.campaign.BudgetType
    if not budget_type:
        return
    row_values[_StringTable.Budget] = bulk_str(bulk_campaign.campaign.DailyBudget)

def csv_to_bid_strategy_biddingscheme(row_values, bulk_bid_strategy):
    entity_csv_to_biddingscheme(row_values, bulk_bid_strategy.bid_strategy)

def csv_to_campaign_biddingscheme(row_values, bulk_campaign):
    entity_csv_to_biddingscheme(row_values, bulk_campaign.campaign)

def entity_csv_to_biddingscheme(row_values, entity):

    success, bid_strategy_type = row_values.try_get_value(_StringTable.BidStrategyType)
    if not success or not bid_strategy_type:
        return

    csv_to_field_BidStrategyType(entity, bid_strategy_type)

    success, max_cpc_row_value = row_values.try_get_value(_StringTable.BidStrategyMaxCpc)
    max_cpc_value = parse_bid(max_cpc_row_value)

    success, target_cpa_row_value = row_values.try_get_value(_StringTable.BidStrategyTargetCpa)
    target_cpa_value = float(target_cpa_row_value) if target_cpa_row_value else None


    success, target_roas_row_value = row_values.try_get_value(_StringTable.BidStrategyTargetRoas)
    target_roas_value = float(target_roas_row_value) if target_roas_row_value else None


    success, target_impression_share_row_value = row_values.try_get_value(_StringTable.BidStrategyTargetImpressionShare)
    target_impression_share_value = float(target_impression_share_row_value) if target_impression_share_row_value else None

    success, commission_rate_row_value = row_values.try_get_value(_StringTable.BidStrategyCommissionRate)
    commission_rate_value = float(commission_rate_row_value) if commission_rate_row_value else None

    success, max_percent_cpc_row_value = row_values.try_get_value(_StringTable.BidStrategyPercentMaxCpc)
    max_percent_cpc_value = float(max_percent_cpc_row_value) if max_percent_cpc_row_value else None

    success, target_ad_position_value = row_values.try_get_value(_StringTable.BidStrategyTargetAdPosition)

    success, target_cost_per_sale_row_value = row_values.try_get_value(_StringTable.BidStrategyTargetCostPerSale)
    target_cost_per_sale_value = float(target_cost_per_sale_row_value) if target_cost_per_sale_row_value else None

    if  bid_strategy_type == 'MaxConversions':
        entity.BiddingScheme.MaxCpc = max_cpc_value
        entity.BiddingScheme.TargetCpa = target_cpa_value
        entity.BiddingScheme.Type = "MaxConversions"
    elif bid_strategy_type == 'MaxClicks':
        entity.BiddingScheme.MaxCpc = max_cpc_value
        entity.BiddingScheme.Type = "MaxClicks"
    elif bid_strategy_type == 'TargetCpa':
        entity.BiddingScheme.MaxCpc = max_cpc_value
        entity.BiddingScheme.Type = "TargetCpa"
        entity.BiddingScheme.TargetCpa = target_cpa_value
    elif bid_strategy_type == 'TargetRoas':
        entity.BiddingScheme.MaxCpc = max_cpc_value
        entity.BiddingScheme.Type = "TargetRoas"
        entity.BiddingScheme.TargetRoas = target_roas_value
    elif bid_strategy_type == 'MaxConversionValue':
        entity.BiddingScheme.Type = "MaxConversionValue"
        entity.BiddingScheme.TargetRoas = target_roas_value
    elif bid_strategy_type == 'TargetImpressionShare':
        entity.BiddingScheme.Type = "TargetImpressionShare"
        entity.BiddingScheme.MaxCpc = max_cpc_value
        entity.BiddingScheme.TargetImpressionShare = target_impression_share_value
        entity.BiddingScheme.TargetAdPosition = target_ad_position_value
    elif bid_strategy_type == "PercentCpc":
        entity.BiddingScheme.MaxPercentCpc = max_percent_cpc_value
        entity.BiddingScheme.Type = "PercentCpc"
    elif bid_strategy_type == "Commission":
        entity.BiddingScheme.MaxPercentCpc = commission_rate_value
        entity.BiddingScheme.Type = "Commission"
    elif bid_strategy_type == "CostPerSale":
        entity.BiddingScheme.TargetCostPerSale = target_cost_per_sale_value
        entity.BiddingScheme.Type = "CostPerSale"

def bid_strategy_biddingscheme_to_csv(bulk_bid_strategy, row_values):
    entity_biddingscheme_to_csv(bulk_bid_strategy.bid_strategy, row_values)

def campaign_biddingscheme_to_csv(bulk_campaign, row_values):
    entity_biddingscheme_to_csv(bulk_campaign.campaign, row_values)

def entity_biddingscheme_to_csv(entity, row_values):
    if not entity:
        return

    bid_strategy_type = field_to_csv_BidStrategyType(entity)

    if not bid_strategy_type:
        return

    row_values[_StringTable.BidStrategyType] = bid_strategy_type

    if  bid_strategy_type == 'MaxConversions':
        row_values[_StringTable.BidStrategyMaxCpc] = bid_bulk_str(entity.BiddingScheme.MaxCpc, entity.Id)
        row_values[_StringTable.BidStrategyTargetCpa] = bulk_str(entity.BiddingScheme.TargetCpa)
    elif bid_strategy_type == 'MaxClicks':
        row_values[_StringTable.BidStrategyMaxCpc] = bid_bulk_str(entity.BiddingScheme.MaxCpc, entity.Id)
    elif bid_strategy_type == 'TargetCpa':
        row_values[_StringTable.BidStrategyMaxCpc] = bid_bulk_str(entity.BiddingScheme.MaxCpc, entity.Id)
        row_values[_StringTable.BidStrategyTargetCpa] = bulk_str(entity.BiddingScheme.TargetCpa)
    elif bid_strategy_type == 'MaxConversionValue':
        row_values[_StringTable.BidStrategyTargetRoas] = bulk_str(entity.BiddingScheme.TargetRoas)
    elif bid_strategy_type == 'TargetRoas':
        row_values[_StringTable.BidStrategyTargetRoas] = bulk_str(entity.BiddingScheme.TargetRoas)
        row_values[_StringTable.BidStrategyMaxCpc] = bid_bulk_str(entity.BiddingScheme.MaxCpc, entity.Id)
    elif bid_strategy_type == 'TargetImpressionShare':
        row_values[_StringTable.BidStrategyMaxCpc] = bid_bulk_str(entity.BiddingScheme.MaxCpc, entity.Id)
        row_values[_StringTable.BidStrategyTargetAdPosition] = bulk_optional_str(entity.BiddingScheme.TargetAdPosition, entity.Id)
        row_values[_StringTable.BidStrategyTargetImpressionShare] = bulk_str(entity.BiddingScheme.TargetImpressionShare)
    elif bid_strategy_type == 'PercentCpc':
        row_values[_StringTable.BidStrategyPercentMaxCpc] = bulk_str(entity.BiddingScheme.MaxPercentCpc)
    elif bid_strategy_type == 'Commission':
        row_values[_StringTable.BidStrategyCommissionRate] = bulk_str(entity.BiddingScheme.CommissionRate)
    elif bid_strategy_type == 'CostPerSale':
        row_values[_StringTable.BidStrategyTargetCostPerSale] = bulk_str(entity.BiddingScheme.TargetCostPerSale)


def bulk_optional_str(value, id):
    if value is None:
        return None
    if not value and id is not None and id > 0:
        return DELETE_VALUE
    return value


def csv_to_status(c, v):
    if v == 'Expired':
        c.ad_group.Status = AdGroupStatus.Expired
        c._is_expired = True
    elif v == 'Active':
        c.ad_group.Status = AdGroupStatus.Active
    elif v == 'Paused':
        c.ad_group.Status = AdGroupStatus.Paused
    elif v == 'Deleted':
        c.ad_group.Status = AdGroupStatus.Deleted
    else:
        c.ad_group.Status = None
        
def parse_bid_option(str):
    if str == "BidValue":
        return BidOption.BidValue
    elif str == "BidBoost":
        return BidOption.BidBoost
    else:
        return None

def bulk_device_preference_str(value):
    if value is None:
        return None
    elif value == 0:
        return "All"
    elif value == 30001:
        return "Mobile"
    else:
        raise ValueError("Unknown device preference")


def parse_datetime(dt_str):
    """ Convert the datetime str to datetime object.

    :param dt_str: The string representing a datetime object.
    :type dt_str: str
    :return: The datetime object parsed from the string.
    :rtype: datetime | None
    """

    if not dt_str or dt_str == DELETE_VALUE:
        return None
    try:
        return datetime.strptime(dt_str, _BULK_DATETIME_FORMAT)
    except Exception:
        return datetime.strptime(dt_str, _BULK_DATETIME_FORMAT_2)


def parse_date(d_str):
    if not d_str or d_str == DELETE_VALUE:
        return None
    parsed_date = datetime.strptime(d_str, _BULK_DATE_FORMAT)
    bing_ads_date = _CAMPAIGN_OBJECT_FACTORY_V13.create('Date')
    bing_ads_date.Day = parsed_date.day
    bing_ads_date.Month = parsed_date.month
    bing_ads_date.Year = parsed_date.year

    return bing_ads_date


def parse_device_preference(value):
    if not value:
        return None

    if value.lower() == 'all':
        return 0
    elif value.lower() == "mobile":
        return 30001
    else:
        return None

def field_to_csv_AudienceIds(entity):
    audience_ids = entity.audience_ids
    if audience_ids is None or len(audience_ids) == 0:
        return None
    return ';'.join(str(audience_id) for audience_id in audience_ids)

def csv_to_field_AudienceIds(entity, value):
    if value is None or value.strip() == '':
        return
    entity.audience_ids = [None if i == 'None' else int(i) for i in value.split(';')]

def field_to_csv_AgeRanges(entity):
    age_ranges = entity.age_ranges
    if age_ranges is None or len(age_ranges) == 0:
        return None
    return ';'.join(age_range for age_range in age_ranges)

def csv_to_field_AgeRanges(entity, value):
    if value is None or value.strip() == '':
        return
    entity.age_ranges = [None if i == 'None' else i for i in value.split(';')]

def field_to_csv_GenderTypes(entity):
    gender_types = entity.gender_types
    if gender_types is None or len(gender_types) == 0:
        return None
    return ';'.join(gender_type for gender_type in gender_types)

def csv_to_field_GenderTypes(entity, value):
    if value is None or value.strip() == '':
        return
    entity.gender_types = [None if i == 'None' else i for i in value.split(';')]

def field_to_csv_CampaignType(entity):
    campaign_type = entity.CampaignTypeFilter
    if campaign_type is None or len(campaign_type) == 0:
        return None
    return ','.join(type for type in campaign_type)

def csv_to_field_CampaignType(entity, value):
    if value is None or value.strip() == '':
        return
    entity.CampaignTypeFilter = [None if i == 'None' else i for i in value.split(',')]

def field_to_csv_DeviceType(entity):
    device_type = entity.DeviceTypeFilter
    if device_type is None or len(device_type) == 0:
        return None
    return ','.join(type for type in device_type)

def csv_to_field_DeviceType(entity, value):
    if value is None or value.strip() == '':
        return
    entity.DeviceTypeFilter = [None if i == 'None' else i for i in value.split(',')]

def field_to_csv_CampaignAssociations(entity):
    associations = entity.CampaignAssociations
    if associations is None or len(associations.CampaignAssociation) == 0:
        return None
    result = ""
    for association in associations.CampaignAssociation:
        result += str(association.CampaignId) + ";"
    return result[:-1]

def csv_to_field_CampaignAssociations(entity, value):
    if value is None or value.strip() == '':
        return
    result = []
    strs = value.split(';')
    for str in strs:
        association = CampaignAssociation()
        association.CampaignId = int(str)
        result.append(association)
    entity.CampaignAssociations = result

def field_to_csv_MediaIds(entity):
    """
    MediaIds field to csv content
    :param entity: entity which has MediaIds attribute
    :return:
    """
    # media_ids? "ns4:ArrayOflong"
    media_ids = entity.ImageMediaIds
    if media_ids is None or len(media_ids) == 0:
        return None
    return ';'.join(str(media_id) for media_id in media_ids)


def csv_to_field_MediaIds(entity, value):
    """
    MediaIds csv to entity
    :param entity:
    :return:
    """
    if value is None or value.strip() == '':
        return
    entity.ImageMediaIds = [None if i == 'None' else int(i) for i in value.split(';')]


# None and empty string will set to empty string
def escape_parameter_text(s):
    return '' if not s else s.replace('\\', '\\\\').replace(';', '\\;')


def unescape_parameter_text(s):
    return '' if not s else s.replace('\\\\', '\\').replace('\\;', ';')


def field_to_csv_UrlCustomParameters(entity):
    """
    transfer the CustomParameters of a entity to csv content (string)
    :param entity: the entity which contains UrlCustomparameters attribute
    :return: csv string content
    """
    if entity is None or entity.UrlCustomParameters is None:
        return None
    if entity.UrlCustomParameters.Parameters is None or entity.UrlCustomParameters.Parameters.CustomParameter is None:
        return DELETE_VALUE if entity.Id and entity.Id > 0 else None
    # The default case when entity created
    if len(entity.UrlCustomParameters.Parameters.CustomParameter) == 0:
        return None
    params = []
    for parameter in entity.UrlCustomParameters.Parameters.CustomParameter:
        params.append('{{_{0}}}={1}'.format(parameter.Key, escape_parameter_text(parameter.Value)))
    return '; '.join(params)

def dict_bulk_str(parameters, separator):
    if parameters is None or len(parameters) == 0:
        return None
    return separator.join(["{0}={1}".format(key, parameters[key]) for key in parameters])

def parse_dict(value):
    if value is None or value.strip() == '':
        return

    return dict([s.split('=') for s in value.split(';') if len(s) > 0])
    pass

def multi_bulk_str(parameters, separator):
    if parameters is None or len(parameters) == 0:
        return None
    return separator.join(parameters)

def parse_multi(value):
    if value is None or value.strip() == '':
        return

    return value.split(';')

def csv_to_field_UrlCustomParameters(entity, value):
    if value is None or value.strip() == '':
        return
    splitter = re.compile(custom_param_splitter)
    pattern = re.compile(custom_param_pattern)
    params = []
    param_strs = splitter.split(value)
    for param_str in param_strs:
        match = pattern.match(param_str)
        if match:
            custom_parameter = _CAMPAIGN_OBJECT_FACTORY_V13.create("CustomParameter")
            custom_parameter.Key = match.group(1)
            custom_parameter.Value = unescape_parameter_text(match.group(2))
            params.append(custom_parameter)
    if len(params) > 0:
        entity.UrlCustomParameters.Parameters.CustomParameter = params


def csv_to_field_Urls(entity, value):
    """
    set FinalUrls / FinalMobileUrls string field
    :param entity: FinalUrls / FinalMobileUrls
    :param value: the content in csv
    :return:set field values
    """
    if value is None or value == '':
        return
    splitter = re.compile(url_splitter)
    entity.string = splitter.split(value)


def field_to_csv_Urls(entity, id):
    """
    parse entity to csv content
    :param entity: FinalUrls / FinalMobileUrls
    :return: csv content
    """
    if entity is None:
        return None
    if entity.string is None:
        return DELETE_VALUE if id and id > 0 else None
    if len(entity.string) == 0:
        return None
    return '; '.join(entity.string)

def csv_to_field_CampaignLanguages(entity, value):
    """
    set Languages string field
    :param entity: Languages
    :param value: the content in csv
    :return:set field values
    """
    if value is None or value == '':
        return
    splitter = re.compile(r';')
    entity.string = splitter.split(value)


def field_to_csv_CampaignLanguages(entity):
    """
    parse entity to csv content
    :param entity: Languages
    :return: csv content
    """
    if entity is None or entity.string is None:
        return None
    if len(entity.string) == 0:
        return None
    return ';'.join(entity.string)

def field_to_csv_BidStrategyType(entity):
    """
    parse entity to csv content
    :param entity: entity which has BiddingScheme attribute
    :return: csv content
    """
    if entity.BiddingScheme is None or type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('BiddingScheme')):
        return None
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('EnhancedCpcBiddingScheme')):
        return 'EnhancedCpc'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('InheritFromParentBiddingScheme')):
        return 'InheritFromParent'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('MaxConversionsBiddingScheme')):
        return 'MaxConversions'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('ManualCpcBiddingScheme')):
        return 'ManualCpc'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('ManualCpmBiddingScheme')):
        return 'ManualCpcm'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('ManualCpvBiddingScheme')):
        return 'ManualCpv'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('TargetCpaBiddingScheme')):
        return 'TargetCpa'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('MaxClicksBiddingScheme')):
        return 'MaxClicks'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('MaxConversionValueBiddingScheme')):
        return 'MaxConversionValue'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('TargetRoasBiddingScheme')):
        return 'TargetRoas'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('TargetImpressionShareBiddingScheme')):
        return 'TargetImpressionShare'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('MaxRoasBiddingScheme')):
        return 'MaxRoas'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('PercentCpcBiddingScheme')):
        return 'PercentCpc'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('CommissionBiddingScheme')):
        return 'Commission'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('ManualCpaBiddingScheme')):
        return 'ManualCpa'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V13.create('CostPerSaleBiddingScheme')):
        return 'CostPerSale'
    else:
        raise TypeError('Unsupported Bid Strategy Type')


def csv_to_field_BidStrategyType(entity, value):
    """
    set BiddingScheme
    :param entity: entity which has BiddingScheme attribute
    :param value: the content in csv
    :return:
    """
    if value is None or value == '':
        return
    elif value == 'EnhancedCpc':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('EnhancedCpcBiddingScheme')
    elif value == 'InheritFromParent':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('InheritFromParentBiddingScheme')
    elif value == 'MaxConversions':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('MaxConversionsBiddingScheme')
    elif value == 'ManualCpc':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('ManualCpcBiddingScheme')
    elif value == 'ManualCpm':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('ManualCpmBiddingScheme')
    elif value == 'ManualCpv':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('ManualCpvBiddingScheme')
    elif value == 'TargetCpa':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('TargetCpaBiddingScheme')
    elif value == 'MaxClicks':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('MaxClicksBiddingScheme')
    elif value == 'MaxConversionValue':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('MaxConversionValueBiddingScheme')
    elif value == 'TargetRoas':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('TargetRoasBiddingScheme')
    elif value == 'TargetImpressionShare':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('TargetImpressionShareBiddingScheme')
    elif value == 'MaxRoas':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('MaxRoasBiddingScheme')
    elif value == 'PercentCpc':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('PercentCpcBiddingScheme')
    elif value == 'Commission':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('CommissionBiddingScheme')
    elif value == 'ManualCpa':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('ManualCpaBiddingScheme')
    elif value == 'CostPerSale':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V13.create('CostPerSaleBiddingScheme')
    else:
        return None
    entity.BiddingScheme.Type = value


def csv_to_field_delimited_strings(entity, value):
    if value is not None and value != '':
        entity.string = value.split(';')

def field_to_csv_delimited_strings(entity):
    if entity is not None and entity.string is not None and len(entity.string) > 0:
        return ';'.join(entity.string)
    return None

def field_to_csv_VideoAssetLinks(assetLinks):
    if assetLinks is None or assetLinks.AssetLink is None:
        return None
    assetLinkContracts = []
    for assetLink in assetLinks.AssetLink:
        if assetLink.Asset is not None and isinstance(assetLink.Asset, VideoAsset_Type):
            contract = {}
            contract['assetPerformanceLabel'] = assetLink.AssetPerformanceLabel if hasattr(assetLink, 'AssetPerformanceLabel') else None
            contract['editorialStatus'] = assetLink.EditorialStatus if hasattr(assetLink, 'EditorialStatus') else None
            contract['id'] = assetLink.Asset.Id if hasattr(assetLink.Asset, 'Id') else None
            contract['name'] = assetLink.Asset.Name if hasattr(assetLink.Asset, 'Name') else None
            contract['pinnedField'] = assetLink.PinnedField if hasattr(assetLink, 'PinnedField') else None
            contract['subType'] = assetLink.Asset.SubType if hasattr(assetLink.Asset, 'SubType') else None
            thumbnailImage = assetLink.Asset.ThumbnailImage if hasattr(assetLink.Asset, 'ThumbnailImage') else None
            if thumbnailImage != None:
                contract['thumbnailImage'] = {}
                contract['thumbnailImage']['id'] = thumbnailImage.Id
                contract['thumbnailImage']['name'] = thumbnailImage.Name
                contract['thumbnailImage']['type'] = thumbnailImage.Type
                contract['thumbnailImage']['subType'] = thumbnailImage.SubType
                contract['thumbnailImage']['cropX'] = thumbnailImage.CropX
                contract['thumbnailImage']['cropY'] = thumbnailImage.CropY
                contract['thumbnailImage']['cropWidth'] = thumbnailImage.CropWidth
                contract['thumbnailImage']['cropHeight'] = thumbnailImage.CropHeight
                contract['thumbnailImage']['targetWidth'] = thumbnailImage.TargetWidth
                contract['thumbnailImage']['targetHeight'] = thumbnailImage.TargetHeight
            assetLinkContracts.append(contract)
    if len(assetLinkContracts) > 0:
        return json.dumps(assetLinkContracts, sort_keys = True)
    return None

    pass

def csv_to_field_VideoAssetLinks(assetLinks, value):
    if value is None or value == '':
        return
    assetLinkContracts = json.loads(value)
    for assetLinkContract in assetLinkContracts:
        asset_link = _CAMPAIGN_OBJECT_FACTORY_V13.create('AssetLink')
        asset_link.Asset = _CAMPAIGN_OBJECT_FACTORY_V13.create('VideoAsset')
        asset_link.Asset.Type = 'VideoAsset'
        asset_link.Asset.Id = assetLinkContract.get('id')
        asset_link.Asset.Name = assetLinkContract.get('name')
        asset_link.Asset.SubType = assetLinkContract.get('subType')
        asset_link.AssetPerformanceLabel = assetLinkContract.get('assetPerformanceLabel')
        asset_link.PinnedField = assetLinkContract.get('pinnedField')
        asset_link.EditorialStatus = assetLinkContract.get('editorialStatus')
        thumbnailImageContract = assetLinkContract.get('thumbnailImage')

        if thumbnailImageContract != None :
            asset_link.Asset.ThumbnailImage = _CAMPAIGN_OBJECT_FACTORY_V13.create('ImageAsset')
            asset_link.Asset.ThumbnailImage.Type = 'ImageAsset'
            asset_link.Asset.ThumbnailImage.Id = thumbnailImageContract.get('id')
            asset_link.Asset.ThumbnailImage.Name = thumbnailImageContract.get('name')
            asset_link.Asset.ThumbnailImage.SubType = thumbnailImageContract.get('subType')
            asset_link.Asset.ThumbnailImage.CropX = thumbnailImageContract.get('cropX')
            asset_link.Asset.ThumbnailImage.CropY = thumbnailImageContract.get('cropY')
            asset_link.Asset.ThumbnailImage.CropWidth = thumbnailImageContract.get('cropWidth')
            asset_link.Asset.ThumbnailImage.CropHeight = thumbnailImageContract.get('cropHeight')
            asset_link.Asset.ThumbnailImage.TargetWidth = thumbnailImageContract.get('targetWidth')
            asset_link.Asset.ThumbnailImage.TargetHeight = thumbnailImageContract.get('targetHeight')

        assetLinks.AssetLink.append(asset_link)



def csv_to_field_TextAssetLinks(assetLinks, value):
    if value is None or value == '':
        return
    assetLinkContracts = json.loads(value)

    for assetLinkContract in assetLinkContracts:
        asset_link = _CAMPAIGN_OBJECT_FACTORY_V13.create('AssetLink')
        asset_link.Asset = _CAMPAIGN_OBJECT_FACTORY_V13.create('TextAsset')
        asset_link.Asset.Type = 'TextAsset'
        asset_link.Asset.Id = assetLinkContract.get('id')
        asset_link.Asset.Text = assetLinkContract.get('text')
        asset_link.Asset.Name = assetLinkContract.get('name')
        asset_link.AssetPerformanceLabel = assetLinkContract.get('assetPerformanceLabel')
        asset_link.PinnedField = assetLinkContract.get('pinnedField')
        asset_link.EditorialStatus = assetLinkContract.get('editorialStatus')
        assetLinks.AssetLink.append(asset_link)

def field_to_csv_ImageAssetLinks(entity):
    if entity is None or entity.AssetLink is None:
        return None
    assetLinkContracts = []
    for assetLink in entity.AssetLink:
        if assetLink.Asset is not None and isinstance(assetLink.Asset, ImageAsset_Type):
            contract = {}
            contract['cropHeight'] = assetLink.Asset.CropHeight if hasattr(assetLink.Asset, 'CropHeight') else None
            contract['cropWidth'] = assetLink.Asset.CropWidth if hasattr(assetLink.Asset, 'CropWidth') else None
            contract['cropX'] = assetLink.Asset.CropX if hasattr(assetLink.Asset, 'CropX') else None
            contract['cropY'] = assetLink.Asset.CropY if hasattr(assetLink.Asset, 'CropY') else None
            contract['id'] = assetLink.Asset.Id if hasattr(assetLink.Asset, 'Id') else None
            contract['name'] = assetLink.Asset.Name if hasattr(assetLink.Asset, 'Name') else None
            contract['assetPerformanceLabel'] = assetLink.AssetPerformanceLabel if hasattr(assetLink, 'AssetPerformanceLabel') else None
            contract['editorialStatus'] = assetLink.EditorialStatus if hasattr(assetLink, 'EditorialStatus') else None
            contract['pinnedField'] = assetLink.PinnedField if hasattr(assetLink, 'PinnedField') else None
            contract['targetWidth'] = assetLink.Asset.TargetWidth if hasattr(assetLink.Asset, 'TargetWidth') else None
            contract['targetHeight'] = assetLink.Asset.TargetHeight if hasattr(assetLink.Asset, 'TargetHeight') else None
            contract['subType'] = assetLink.Asset.SubType if hasattr(assetLink.Asset, 'SubType') else None
            assetLinkContracts.append(contract)
    if len(assetLinkContracts) > 0:
        return json.dumps(assetLinkContracts)
    return None

def csv_to_field_ImageAssetLinks(assetLinks, value):
    if value is None or value == '':
        return
    assetLinkContracts = json.loads(value)

    for assetLinkContract in assetLinkContracts:
        asset_link = _CAMPAIGN_OBJECT_FACTORY_V13.create('AssetLink')
        asset_link.Asset = _CAMPAIGN_OBJECT_FACTORY_V13.create('ImageAsset')
        asset_link.Asset.Type = 'ImageAsset'
        asset_link.Asset.CropHeight = assetLinkContract.get('cropHeight')
        asset_link.Asset.CropWidth = assetLinkContract.get('cropWidth')
        asset_link.Asset.CropX = assetLinkContract.get('cropX')
        asset_link.Asset.CropY = assetLinkContract.get('cropY')
        asset_link.Asset.Id = assetLinkContract.get('id')
        asset_link.Asset.Name = assetLinkContract.get('name')
        asset_link.AssetPerformanceLabel = assetLinkContract.get('assetPerformanceLabel')
        asset_link.PinnedField = assetLinkContract.get('pinnedField')
        asset_link.EditorialStatus = assetLinkContract.get('editorialStatus')
        asset_link.Asset.TargetWidth = assetLinkContract.get('targetWidth')
        asset_link.Asset.TargetHeight = assetLinkContract.get('targetHeight')
        asset_link.Asset.SubType = assetLinkContract.get('subType')
        assetLinks.AssetLink.append(asset_link)

def field_to_csv_TextAssetLinks(entity):
    if entity is None or entity.AssetLink is None:
        return None
    assetLinkContracts = []
    for assetLink in entity.AssetLink:
        if assetLink.Asset is not None and isinstance(assetLink.Asset, TextAsset_Type):
            contract = {}
            contract['id'] = assetLink.Asset.Id if hasattr(assetLink.Asset, 'Id') else None
            contract['name'] = assetLink.Asset.Name if hasattr(assetLink.Asset, 'Name') else None
            contract['text'] = assetLink.Asset.Text if hasattr(assetLink.Asset, 'Text') else None
            contract['assetPerformanceLabel'] = assetLink.AssetPerformanceLabel if hasattr(assetLink, 'AssetPerformanceLabel') else None
            contract['editorialStatus'] = assetLink.EditorialStatus if hasattr(assetLink, 'EditorialStatus') else None
            contract['pinnedField'] = assetLink.PinnedField if hasattr(assetLink, 'PinnedField') else None
            assetLinkContracts.append(contract)
    if len(assetLinkContracts) > 0:
        return json.dumps(assetLinkContracts, sort_keys = True)
    return None


def ad_rotation_bulk_str(value, id):
    if value is None:
        return None
    elif value.Type is None:
        return DELETE_VALUE if id and id > 0 else None
    else:
        return bulk_str(value.Type)


def parse_ad_rotation(value):
    if not value:
        return None
    ad_rotation = _CAMPAIGN_OBJECT_FACTORY_V13.create('AdRotation')
    ad_rotation.Type = None if value == DELETE_VALUE else value
    return ad_rotation


def parse_ad_group_bid(value):
    if not value:
        return None
    bid = _CAMPAIGN_OBJECT_FACTORY_V13.create('Bid')
    bid.Amount = float(value)
    return bid


def ad_group_bid_bulk_str(value):
    if value is None or value.Amount is None:
        return None
    return bulk_str(value.Amount)


def keyword_bid_bulk_str(value, id):
    if value is None:
        return DELETE_VALUE if id and id > 0 else None
    if value.Amount is None:
        return None
    return bulk_str(value.Amount)


def parse_keyword_bid(value):
    bid = _CAMPAIGN_OBJECT_FACTORY_V13.create('Bid')
    if not value or value == DELETE_VALUE:
        bid.Amount = None
    else:
        bid.Amount = float(value)
    return bid


def bid_bulk_str(value, id):
    if value is None:
        return DELETE_VALUE if id and id > 0 else None
    if value.Amount is None:
        return None
    return bulk_str(value.Amount)


def parse_bid(value):
    bid = _CAMPAIGN_OBJECT_FACTORY_V13.create('Bid')
    if not value:
        bid.Amount = None
    else:
        bid.Amount = float(value)
    return bid

def minute_bulk_str(value):
    if value == 'Zero':
        return '0'
    elif value == 'Fifteen':
        return '15'
    elif value == 'Thirty':
        return '30'
    elif value == 'FortyFive':
        return '45'
    else:
        raise ValueError('Unknown minute')

def parse_fixed_bid(value):
    if not value:
        return None
    fixed_bid = _CAMPAIGN_OBJECT_FACTORY_V13.create('FixedBid')
    fixed_bid.Amount = float(value)
    return fixed_bid

def fixed_bid_bulk_str(value):
    if value is None or not hasattr(value, 'Amount') or value.Amount is None:
        return None
    return bulk_str(value.Amount)

def bid_multiplier_bulk_str(value):
    if value is None or not hasattr(value, 'Multiplier') or value.Multiplier is None:
        return None
    return bulk_str(value.Multiplier)

def parse_minute(value):
    Minute = _CAMPAIGN_OBJECT_FACTORY_V13.create('Minute')
    minute_number = int(value)
    if minute_number == 0:
        return Minute.Zero
    elif minute_number == 15:
        return Minute.Fifteen
    elif minute_number == 30:
        return Minute.Thirty
    elif minute_number == 45:
        return Minute.FortyFive
    raise ValueError('Unknown minute')


def format_Day(value):
    Day = _CAMPAIGN_OBJECT_FACTORY_V13.create('Day')
    if value.lower() == 'monday':
        return Day.Monday
    elif value.lower() == 'tuesday':
        return Day.Tuesday
    elif value.lower() == 'wednesday':
        return Day.Wednesday
    elif value.lower() == 'thursday':
        return Day.Thursday
    elif value.lower() == 'friday':
        return Day.Friday
    elif value.lower() == 'saturday':
        return Day.Saturday
    elif value.lower() == 'sunday':
        return Day.Sunday
    raise ValueError('Unable to parse day: {0}'.format(value))

def parse_location_target_type(value):
    if value == 'Metro Area':
        return 'MetroArea'
    elif value == 'Postal Code':
        return 'PostalCode'
    else:
        return value


def location_target_type_bulk_str(value):
    if value == 'MetroArea':
        return 'Metro Area'
    elif value == 'PostalCode':
        return 'Postal Code'
    else:
        return value


def field_to_csv_AdSchedule(entity, id):
    """
    get the bulk string for Scheduling DayTimeRanges
    :param entity: Scheduling entity
    :return: bulk str
    """
    if entity is None:
        return None
    if entity.DayTimeRanges is None:
        return DELETE_VALUE if id and id > 0 else None
    return ';'.join('({0}[{1:02d}:{2:02d}-{3:02d}:{4:02d}])'
                    .format(d.Day, d.StartHour, int(minute_bulk_str(d.StartMinute)), d.EndHour, int(minute_bulk_str(d.EndMinute)))
                    for d in entity.DayTimeRanges.DayTime
                    )


def csv_to_field_AdSchedule(entity, value):
    if value is None or value.strip() == '' or value == DELETE_VALUE:
        return
    daytime_strs = value.split(';')
    ad_schedule_pattern = r'\((Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\[(\d\d?):(\d\d)-(\d\d?):(\d\d)\]\)'
    pattern = re.compile(ad_schedule_pattern, re.IGNORECASE)
    daytimes = []
    for daytime_str in daytime_strs:
        match = pattern.match(daytime_str)
        if match:
            daytime = _CAMPAIGN_OBJECT_FACTORY_V13.create('DayTime')
            daytime.Day = format_Day(match.group(1))
            daytime.StartHour = int(match.group(2))
            daytime.StartMinute = parse_minute(match.group(3))
            daytime.EndHour = int(match.group(4))
            daytime.EndMinute = parse_minute(match.group(5))
            daytimes.append(daytime)
        else:
            raise ValueError('Unable to parse DayTime: {0}'.format(daytime_str))
    entity.DayTimeRanges.DayTime = daytimes


def field_to_csv_FeedItemAdSchedule(entity, id):
    """
    get the bulk string for FeedItem DayTimeRanges
    :param entity: Scheduling entity
    :return: bulk str
    """
    if entity is None:
        return None
    if entity.daytime_ranges is None:
        return DELETE_VALUE if id and id > 0 else None
    return ';'.join('({0}[{1:02d}:{2:02d}-{3:02d}:{4:02d}])'
                    .format(d.Day, d.StartHour, int(minute_bulk_str(d.StartMinute)), d.EndHour, int(minute_bulk_str(d.EndMinute)))
                    for d in entity.daytime_ranges
                    )


def csv_to_field_FeedItemAdSchedule(entity, value):
    if value is None or value.strip() == '' or value == DELETE_VALUE:
        return
    daytime_strs = value.split(';')
    ad_schedule_pattern = r'\((Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\[(\d\d?):(\d\d)-(\d\d?):(\d\d)\]\)'
    pattern = re.compile(ad_schedule_pattern, re.IGNORECASE)
    daytimes = []
    for daytime_str in daytime_strs:
        match = pattern.match(daytime_str)
        if match:
            daytime = _CAMPAIGN_OBJECT_FACTORY_V13.create('DayTime')
            daytime.Day = format_Day(match.group(1))
            daytime.StartHour = int(match.group(2))
            daytime.StartMinute = parse_minute(match.group(3))
            daytime.EndHour = int(match.group(4))
            daytime.EndMinute = parse_minute(match.group(5))
            daytimes.append(daytime)
        else:
            raise ValueError('Unable to parse DayTime: {0}'.format(daytime_str))
    entity.daytime_ranges = daytimes


def field_to_csv_SchedulingDate(theDate, id):
    """
    write scheduling StartDate to bulk string
    :param theDate: Date obj to convert
    :return: date bulk string
    """
    if theDate is None or (theDate.Day == 0 and theDate.Month == 0 and theDate.Year == 0):
        return DELETE_VALUE if id and id > 0 else None
    # this case is what the suds creates by default. return None instead of a delete value
    elif theDate.Day is None and theDate.Month is None and theDate.Year is None:
        return None
    return '{0!s}/{1!s}/{2!s}'.format(theDate.Month, theDate.Day, theDate.Year)

def field_to_csv_SchedulingStartDate(entity, id):
    """
    write scheduling StartDate to bulk string
    :param entity: Scheduling entity
    :return: date bulk string
    """
    if entity is None:
        return None
    elif entity.StartDate is None:
        return DELETE_VALUE if id and id > 0 else None
    # this case is what the suds creates by default. return None instead of a delete value
    elif entity.StartDate.Day is None and entity.StartDate.Month is None and entity.StartDate.Year is None:
        return None
    return '{0!s}/{1!s}/{2!s}'.format(entity.StartDate.Month, entity.StartDate.Day, entity.StartDate.Year)


def field_to_csv_SchedulingEndDate(entity, id):
    """
    write scheduling EndDate to bulk string
    :param entity: Scheduling entity
    :return: date bulk string
    """
    if entity is None:
        return None
    elif entity.EndDate is None:
        return DELETE_VALUE if id and id > 0 else None
    # this case is what the suds creates by default. return None instead of a delete value
    elif entity.EndDate.Day is None and entity.EndDate.Month is None and entity.EndDate.Year is None:
        return None
    return '{0!s}/{1!s}/{2!s}'.format(entity.EndDate.Month, entity.EndDate.Day, entity.EndDate.Year)

def field_to_csv_UseSearcherTimeZone(bool_value, id):
    if bool_value is None:
        return DELETE_VALUE if id and id > 0 else None
    else:
        return str(bool_value)
    
def csv_to_field_enum(entity, value, attr_name, enum_class):
    """
    Generic method to convert CSV string values to enum fields on an entity.

    Args:
        entity: The entity object to set the attribute on
        value: The string value from CSV
        attr_name: The name of the attribute to set on the entity
        enum_class: The enum class to convert the value to
    """
    if value is None or value == '':
        setattr(entity, attr_name, None)
        return

    try:
        enum_value = getattr(enum_class, value)
        setattr(entity, attr_name, enum_value)
    except (AttributeError, ValueError):
        # If the value doesn't match any enum value, set to None
        setattr(entity, attr_name, None)
    
def csv_to_field_CampaignStatus(entity, value):
    if value is None or value == '':
        entity.Status = None
    elif value == 'Active':
        entity.Status = CampaignStatus.Active
    elif value == 'Paused':
        entity.Status = CampaignStatus.Paused
    elif value == 'BudgetPaused':
        entity.Status = CampaignStatus.BudgetPaused
    elif value == 'BudgetAndManualPaused':
        entity.Status = CampaignStatus.BudgetAndManualPaused
    elif value == 'Deleted':
        entity.Status = CampaignStatus.Deleted
    elif value == 'Suspended':
        entity.Status = CampaignStatus.Suspended
    else:
        entity.Status = None 

def field_to_csv_bool(bool_value):
    if bool_value is None:
        return None
    else:
        return str(bool_value)

def csv_to_field_BudgetType(entity, value, version=13):
    if value is None or value == '':
        entity.BudgetType = None
    elif value == 'MonthlyBudgetSpendUntilDepleted' and version == 13:
        entity.BudgetType = BudgetLimitType.MonthlyBudgetSpendUntilDepleted
    elif value == 'DailyBudgetAccelerated':
        entity.BudgetType = BudgetLimitType.DailyBudgetAccelerated
    elif value == 'DailyBudgetStandard':
        entity.BudgetType = BudgetLimitType.DailyBudgetStandard
    else:
        entity.BudgetType = None

def field_to_csv_WebpageParameter_CriterionName(entity):
    if entity.Criterion is None or entity.Criterion.Parameter is None or entity.Criterion.Parameter.CriterionName is None:
        return None
    if not entity.Criterion.Parameter.CriterionName:
        return DELETE_VALUE if entity.Id and entity.Id > 0 else None
    return entity.Criterion.Parameter.CriterionName


def csv_to_field_WebpageParameter_CriterionName(entity, value):
    if value is None or value == '':
        return
    if entity.Criterion is not None and isinstance(entity.Criterion, type(Webpage)):
        entity.Criterion.Parameter.CriterionName = value
    else:
        webpage = _CAMPAIGN_OBJECT_FACTORY_V13.create('Webpage')
        webpage.Parameter.CriterionName = value
        entity.Criterion = webpage


def entity_to_csv_DSAWebpageParameter(entity, row_values):
    """
    Set Campaign/AdGroup Criterion (WebpagePage) Web page parameters from bulk values
    :param entity: campaign/ad group criterion entity
    :param row_values: bulk row values
    """
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion, type(Webpage)) and \
            entity.Criterion.Parameter is not None and entity.Criterion.Parameter.Conditions is not None and \
            entity.Criterion.Parameter.Conditions.WebpageCondition is not None:
        condition_prefix = _StringTable.DynamicAdTargetCondition1[:-1]
        value_prefix = _StringTable.DynamicAdTargetValue1[:-1]
        condition_operator_prefix = _StringTable.DynamicAdTargetConditionOperator1[:-1]

        conditions = entity.Criterion.Parameter.Conditions.WebpageCondition
        for i in range(0, len(conditions)):
            row_values[condition_prefix + str(i + 1)] = conditions[i].Operand
            row_values[value_prefix + str(i + 1)] = conditions[i].Argument
            row_values[condition_operator_prefix + str(i + 1)] = conditions[i].Operator


def csv_to_entity_DSAWebpageParameter(row_values, entity):
    """
    convert Campaign/Ad Group Criterion (WebpagePage) Web page parameters to bulk row values
    :param row_values: bulk row values
    :param entity: campaign/ad group criterion entity
    """
    MAX_NUMBER_OF_CONDITIONS = 3
    condition_prefix = _StringTable.DynamicAdTargetCondition1[:-1]
    value_prefix = _StringTable.DynamicAdTargetValue1[:-1]
    condition_operator_prefix = _StringTable.DynamicAdTargetConditionOperator1[:-1]

    conditions = []
    for i in range(0, MAX_NUMBER_OF_CONDITIONS):
        condition_success, webpage_condition = row_values.try_get_value(condition_prefix + str(i + 1))
        value_success, webpage_value = row_values.try_get_value(value_prefix + str(i + 1))
        condition_operator_success, webpage_condition_operator = row_values.try_get_value(condition_operator_prefix + str(i + 1))
        if condition_success and value_success and webpage_condition is not None and webpage_condition != '':
            condition = _CAMPAIGN_OBJECT_FACTORY_V13.create('WebpageCondition')
            if webpage_condition.lower() == 'url':
                condition.Operand = WebpageConditionOperand.Url
            elif webpage_condition.lower() == "category":
                condition.Operand = WebpageConditionOperand.Category
            elif webpage_condition.lower() == 'pagetitle':
                condition.Operand = WebpageConditionOperand.PageTitle
            elif webpage_condition.lower() == 'pagecontent':
                condition.Operand = WebpageConditionOperand.PageContent
            elif webpage_condition.lower() == 'customlabel':
                condition.Operand = WebpageConditionOperand.CustomLabel
            elif webpage_condition.lower() == 'unknown':
                condition.Operand = WebpageConditionOperand.Unknown
            else:
                # TODO wait bug 54825 to be fixed
                if webpage_condition.lower() == 'none':
                    continue
                return None
            if condition_operator_success:
                condition.Operator = webpage_condition_operator

            condition.Argument = webpage_value
            conditions.append(condition)

    if len(conditions) > 0:
        if entity.Criterion is not None and isinstance(entity.Criterion, type(Webpage)):
            entity.Criterion.Parameter.Conditions.WebpageCondition = conditions
        else:
            webpage = _CAMPAIGN_OBJECT_FACTORY_V13.create('Webpage')
            webpage.Parameter.Conditions.WebpageCondition = conditions
            entity.Criterion = webpage

def entity_to_csv_PriceTableRows(entity, row_values):
    """
    Set Price Ad Extension price table rows from bulk values
    :param entity: price ad extension entity
    :param row_values: bulk row values
    """
    if entity is not None and entity.TableRows is not None and \
            entity.TableRows.PriceTableRow is not None:
        currency_code_prefix = _StringTable.CurrencyCode1[:-1]
        price_description_prefix = _StringTable.PriceDescription1[:-1]
        header_prefix = _StringTable.Header1[:-1]
        final_mobile_url_prefix = _StringTable.FinalMobileUrl1[:-1]
        final_url_prefix = _StringTable.FinalUrl1[:-1]
        price_prefix = _StringTable.Price1[:-1]
        price_qualifier_prefix = _StringTable.PriceQualifier1[:-1]
        price_unit_prefix = _StringTable.PriceUnit1[:-1]

        price_table_rows = entity.TableRows.PriceTableRow
        for i in range(0, len(price_table_rows)):
            row_values[currency_code_prefix + str(i + 1)] = price_table_rows[i].CurrencyCode
            row_values[price_description_prefix + str(i + 1)] = price_table_rows[i].Description
            row_values[header_prefix + str(i + 1)] = price_table_rows[i].Header
            row_values[final_mobile_url_prefix + str(i + 1)] = field_to_csv_Urls(price_table_rows[i].FinalMobileUrls, entity.Id)
            row_values[final_url_prefix + str(i + 1)] = field_to_csv_Urls(price_table_rows[i].FinalUrls, entity.Id)
            row_values[price_prefix + str(i + 1)] = bulk_str(price_table_rows[i].Price)
            row_values[price_qualifier_prefix + str(i + 1)] = price_table_rows[i].PriceQualifier
            row_values[price_unit_prefix + str(i + 1)] = price_table_rows[i].PriceUnit


def csv_to_entity_PriceTableRows(row_values, entity):
    """
    convert Price Ad Extension price table rows to bulk row values
    :param row_values: bulk row values
    :param entity: price ad extension entity
    """
    MAX_NUMBER_OF_PRICE_TABLE_ROWS = 8
    currency_code_prefix = _StringTable.CurrencyCode1[:-1]
    price_description_prefix = _StringTable.PriceDescription1[:-1]
    header_prefix = _StringTable.Header1[:-1]
    final_mobile_url_prefix = _StringTable.FinalMobileUrl1[:-1]
    final_url_prefix = _StringTable.FinalUrl1[:-1]
    price_prefix = _StringTable.Price1[:-1]
    price_qualifier_prefix = _StringTable.PriceQualifier1[:-1]
    price_unit_prefix = _StringTable.PriceUnit1[:-1]

    price_table_rows = []
    for i in range(0, MAX_NUMBER_OF_PRICE_TABLE_ROWS):
        currency_code_success, currency_code = row_values.try_get_value(currency_code_prefix + str(i + 1))
        price_description_success, price_description = row_values.try_get_value(price_description_prefix + str(i + 1))
        header_success, header = row_values.try_get_value(header_prefix + str(i + 1))
        final_mobile_url_success, final_mobile_url = row_values.try_get_value(final_mobile_url_prefix + str(i + 1))
        final_url_success, final_url = row_values.try_get_value(final_url_prefix + str(i + 1))
        price_success, price = row_values.try_get_value(price_prefix + str(i + 1))
        price_qualifier_success, price_qualifier = row_values.try_get_value(price_qualifier_prefix + str(i + 1))
        price_unit_success, price_unit = row_values.try_get_value(price_unit_prefix + str(i + 1))

        if currency_code_success \
           or price_description_success \
           or header_success \
           or final_mobile_url_success \
           or final_url_success \
           or price_success \
           or price_qualifier_success \
           or price_unit_success:
            price_table_row = _CAMPAIGN_OBJECT_FACTORY_V13.create('PriceTableRow')
            price_table_row.CurrencyCode = currency_code
            price_table_row.Description = price_description
            price_table_row.Header = header
            csv_to_field_Urls(price_table_row.FinalMobileUrls, final_mobile_url)
            csv_to_field_Urls(price_table_row.FinalUrls, final_url)
            price_table_row.Price = price
            price_table_row.PriceQualifier = price_qualifier
            price_table_row.PriceUnit = price_unit

            price_table_rows.append(price_table_row)

    if len(price_table_rows) > 0:
        entity.TableRows.PriceTableRow = price_table_rows


def parse_bool(value):
    if value is None or value == '' or value == DELETE_VALUE:
        return None
    elif value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise ValueError('Unable to parse bool value: {0}.'.format(value))


def field_to_csv_RemarketingRule(entity):
    """
    convert remarketing rule to bulk string
    :param entity: remarketing list entity
    """
    if entity.Rule == None:
        return None

    rule = entity.Rule
    if (isinstance(rule, type(PageVisitorsRule))):
        return 'PageVisitors{0}'.format(rule_item_groups_str(rule.RuleItemGroups.RuleItemGroup, rule.NormalForm))
    elif (isinstance(rule, type(PageVisitorsWhoVisitedAnotherPageRule))):
        return 'PageVisitorsWhoVisitedAnotherPage({0}) and ({1})'.format(
            rule_item_groups_str(rule.RuleItemGroups.RuleItemGroup),
            rule_item_groups_str(rule.AnotherRuleItemGroups.RuleItemGroup))
    elif (isinstance(rule, type(PageVisitorsWhoDidNotVisitAnotherPageRule))):
        return 'PageVisitorsWhoDidNotVisitAnotherPage({0}) and not ({1})'.format(
            rule_item_groups_str(rule.IncludeRuleItemGroups.RuleItemGroup),
            rule_item_groups_str(rule.ExcludeRuleItemGroups.RuleItemGroup))
    elif (isinstance(rule, type(CustomEventsRule))):
        return 'CustomEvents{0}'.format(custom_event_rule_str(rule))
    elif (isinstance(rule, type(RemarketingRule))):
        return None
    else:
        raise ValueError('Unsupported Remarketing Rule type: {0}'.format(type(entity.RemarketingRule)))


def rule_item_groups_str(groups, nf = NormalForm.Disjunctive):
    outerOperator = ' or '
    innerOperator = ' and '
    if nf == NormalForm.Conjunctive:
        outerOperator = ' and '
        innerOperator = ' or '
    if groups is None or len(groups) == 0:
        raise ValueError('Remarketing RuleItemGroups is None or empty.')

    return outerOperator.join(['({0})'.format(rule_items_str(group.Items.RuleItem, innerOperator)) for group in groups])


def rule_items_str(items, innerOperator = ' and '):
    if items is None or len(items) == 0:
        raise ValueError('Remarketing RuleItem list is None or empty.')

    return innerOperator.join(['({0} {1} {2})'.format(item.Operand, item.Operator, item.Value) for item in items])


def custom_event_rule_str(rule):
    rule_items = []
    if rule.ActionOperator is not None and rule.Action is not None:
        rule_items.append('Action {0} {1}'.format(rule.ActionOperator, rule.Action))
    if rule.CategoryOperator is not None and rule.Category is not None:
        rule_items.append('Category {0} {1}'.format(rule.CategoryOperator, rule.Category))
    if rule.LabelOperator is not None and rule.Label is not None:
        rule_items.append('Label {0} {1}'.format(rule.LabelOperator, rule.Label))
    if rule.ValueOperator is not None and rule.Value is not None:
        rule_items.append('Value {0} {1}'.format(rule.ValueOperator, rule.Value))

    if len(rule_items) == 0:
        raise ValueError('Remarketing CustomEvents RuleItem list is empty')

    return ' and '.join('({0})'.format(item) for item in rule_items)


def csv_to_field_RemarketingRule(entity, value):
    """
    parse remarketing rule string and set remarketing rule attribute value
    :param entity: remarketing list entity
    :param value: bulk string value
    """
    if value is None or value == '':
        return

    type_end_pos = value.index('(')
    if type_end_pos <= 0:
        raise ValueError('Invalid Remarketing Rule: {0}'.format(value))

    rule_type = value[:type_end_pos]
    rule = value[type_end_pos:]

    if rule_type.lower() == 'pagevisitors':
        entity.Rule = parse_rule_PageVisitors(rule)
    elif rule_type.lower() == 'pagevisitorswhovisitedanotherpage':
        entity.Rule = parse_rule_PageVisitorsWhoVisitedAnotherPage(rule)
    elif rule_type.lower() == 'pagevisitorswhodidnotvisitanotherpage':
        entity.Rule = parse_rule_PageVisitorsWhoDidNotVisitAnotherPage(rule)
    elif rule_type.lower() == 'customevents':
        entity.Rule = parse_rule_CustomEvents(rule)
    else:
        entity.Rule = None


def field_to_csv_CriterionAudienceId(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.AudienceId is None:
        return None
    return bulk_str(entity.Criterion.AudienceId)


def csv_to_field_CriterionAudienceId(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion, type(AudienceCriterion)):
        entity.Criterion.AudienceId = value

def field_to_csv_CashbackAdjustment(entity):
    if entity is None or entity.CriterionCashback is None or  hasattr(entity.CriterionCashback, "CashbackPercent") == False or entity.CriterionCashback.CashbackPercent is None:
        return None
    return bulk_str(entity.CriterionCashback.CashbackPercent)


def csv_to_field_CashbackAdjustment(entity, value):
    if value is None or value == '':
        return
    if entity is not None:
        entity.CriterionCashback = _CAMPAIGN_OBJECT_FACTORY_V13.create('CashbackAdjustment')
        entity.CriterionCashback.Type = 'CashbackAdjustment'
        entity.CriterionCashback.CashbackPercent = value

def field_to_csv_BidAdjustment(entity):
    if entity is None or entity.CriterionBid is None or entity.CriterionBid.Multiplier is None:
        return None
    return bulk_str(entity.CriterionBid.Multiplier)


def csv_to_field_BidAdjustment(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.CriterionBid is not None and isinstance(entity.CriterionBid, type(BidMultiplier)):
        entity.CriterionBid.Multiplier = value

def field_to_csv_AgeTarget(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.AgeRange is None:
        return None
    return entity.Criterion.AgeRange

def csv_to_field_AgeTarget(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(AgeCriterion)):
        setattr(entity.Criterion, "AgeRange", value)

def field_to_csv_DayTimeTarget(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.Day is None:
        return None
    return entity.Criterion.Day

def csv_to_field_DayTimeTarget(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(DayTimeCriterion)):
        setattr(entity.Criterion, "Day", value)

def field_to_csv_FromHour(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.FromHour is None:
        return None
    return str(entity.Criterion.FromHour)

def csv_to_field_FromHour(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(DayTimeCriterion)):
        setattr(entity.Criterion, "FromHour", value)

def field_to_csv_FromMinute(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.FromMinute is None:
        return None
    return minute_bulk_str(entity.Criterion.FromMinute)

def csv_to_field_FromMinute(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(DayTimeCriterion)):
        setattr(entity.Criterion, "FromMinute", parse_minute(value))

def field_to_csv_ToHour(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.ToHour is None:
        return None
    return str(entity.Criterion.ToHour)

def csv_to_field_ToHour(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(DayTimeCriterion)):
        setattr(entity.Criterion, "ToHour", value)

def field_to_csv_ToMinute(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.ToMinute is None:
        return None
    return minute_bulk_str(entity.Criterion.ToMinute)

def csv_to_field_ToMinute(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(DayTimeCriterion)):
        setattr(entity.Criterion, "ToMinute", parse_minute(value))

def field_to_csv_DeviceTarget(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.DeviceName is None:
        return None
    return entity.Criterion.DeviceName

def csv_to_field_DeviceTarget(entity, value):
    if value is None:
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(DeviceCriterion)):
        setattr(entity.Criterion, "DeviceName", value)

def field_to_csv_OSName(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.OSName is None:
        return None
    return entity.Criterion.OSName

def csv_to_field_OSName(entity, value):
    if value is None:
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(DeviceCriterion)):
        setattr(entity.Criterion, "OSName", value)

def field_to_csv_GenderTarget(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.GenderType is None:
        return None
    return entity.Criterion.GenderType

def csv_to_field_GenderTarget(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(GenderCriterion)):
        setattr(entity.Criterion, "GenderType", value)

def field_to_csv_MaxDays(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.MaxDays is None:
        return None
    return bulk_str(entity.Criterion.MaxDays)

def csv_to_field_MaxDays(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(HotelAdvanceBookingWindowCriterion)):
        setattr(entity.Criterion, "MaxDays", int(value))

def field_to_csv_MinDays(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.MinDays is None:
        return None
    return bulk_str(entity.Criterion.MinDays)

def csv_to_field_MinDays(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(HotelAdvanceBookingWindowCriterion)):
        setattr(entity.Criterion, "MinDays", int(value))

def field_to_csv_StartDate(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.StartDate is None:
        return None
    return bulk_datetime_str(entity.Criterion.StartDate)

def csv_to_field_StartDate(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(HotelCheckInDateCriterion)):
        setattr(entity.Criterion, "StartDate", parse_datetime(value))

def field_to_csv_GenreId(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.GenreId is None:
        return None
    return bulk_str(entity.Criterion.GenreId)

def csv_to_field_GenreId(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(GenreCriterion)):
        setattr(entity.Criterion, "GenreId", int(value) if value else None)

def field_to_csv_EndDate(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.EndDate is None:
        return None
    return bulk_datetime_str(entity.Criterion.EndDate)

def csv_to_field_EndDate(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(HotelCheckInDateCriterion)):
        setattr(entity.Criterion, "EndDate", parse_datetime(value))

def field_to_csv_CheckInDay(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.CheckInDay is None:
        return None
    return entity.Criterion.CheckInDay

def csv_to_field_CheckInDay(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(HotelCheckInDayCriterion)):
        setattr(entity.Criterion, "CheckInDay", value)

def field_to_csv_HotelDateSelectionType(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.HotelDateSelectionType is None:
        return None
    return entity.Criterion.HotelDateSelectionType

def csv_to_field_HotelDateSelectionType(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(HotelDateSelectionTypeCriterion)):
        setattr(entity.Criterion, "HotelDateSelectionType", value)

def field_to_csv_MaxNights(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.MaxNights is None:
        return None
    return bulk_str(entity.Criterion.MaxNights)

def csv_to_field_MaxNights(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(HotelLengthOfStayCriterion)):
        setattr(entity.Criterion, "MaxNights", int(value))

def field_to_csv_MinNights(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.MinNights is None:
        return None
    return bulk_str(entity.Criterion.MinNights)

def csv_to_field_MinNights(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(HotelLengthOfStayCriterion)):
        setattr(entity.Criterion, "MinNights", int(value))

def field_to_csv_LocationTarget(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.LocationId is None:
        return None
    return str(entity.Criterion.LocationId)

def csv_to_field_LocationTarget(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(LocationCriterion)):
        setattr(entity.Criterion, "LocationId", value)

def field_to_csv_LocationType(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.LocationType is None:
        return None
    return entity.Criterion.LocationType

def csv_to_field_LocationType(entity, value):
    if value is None:
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(LocationCriterion)):
        setattr(entity.Criterion, "LocationType", value)

def field_to_csv_LocationName(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.DisplayName is None:
        return None
    return entity.Criterion.DisplayName

def csv_to_field_LocationName(entity, value):
    if value is None:
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(LocationCriterion)):
        setattr(entity.Criterion, "DisplayName", value)

def field_to_csv_LocationIntentTarget(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.IntentOption is None:
        return None
    return entity.Criterion.IntentOption

def csv_to_field_LocationIntentTarget(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(LocationIntentCriterion)):
        setattr(entity.Criterion, "IntentOption", value)

def field_to_csv_RadiusName(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.Name is None:
        return None
    return entity.Criterion.Name

def csv_to_field_RadiusName(entity, value):
    if value is None:
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(RadiusCriterion)):
        setattr(entity.Criterion, "Name", value)

def field_to_csv_Radius(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.Radius is None:
        return None
    return str(entity.Criterion.Radius)

def csv_to_field_Radius(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(RadiusCriterion)):
        setattr(entity.Criterion, "Radius", value)

def field_to_csv_DealTarget(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.DealId is None:
        return None
    return str(entity.Criterion.DealId)

def csv_to_field_DealTarget(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(DealCriterion)):
        setattr(entity.Criterion, "DealId", int(value))

def field_to_csv_RadiusUnit(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.RadiusUnit is None:
        return None
    return entity.Criterion.RadiusUnit

def csv_to_field_RadiusUnit(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(RadiusCriterion)):
        setattr(entity.Criterion, "RadiusUnit", value)

def field_to_csv_LatitudeDegrees(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.LatitudeDegrees is None:
        return None
    return  str(entity.Criterion.LatitudeDegrees)

def csv_to_field_LatitudeDegrees(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(RadiusCriterion)):
        setattr(entity.Criterion, "LatitudeDegrees", value)

def field_to_csv_LongitudeDegrees(entity):
    if entity is None or entity.Criterion is None or entity.Criterion.LongitudeDegrees is None:
        return None
    return  str(entity.Criterion.LongitudeDegrees)

def csv_to_field_LongitudeDegrees(entity, value):
    if value is None or value == '':
        return
    if entity is not None and entity.Criterion is not None and isinstance(entity.Criterion,type(RadiusCriterion)):
        setattr(entity.Criterion, "LongitudeDegrees", value)

def target_setting_to_csv(entity):
    if not entity.Settings or not entity.Settings.Setting:
        return None
    settings = [setting for setting in entity.Settings.Setting if isinstance(setting, TargetSetting_Type)]
    if len(settings) == 0:
        return None
    if len(settings) != 1:
        raise ValueError('Can only have 1 TargetSetting in Settings.')
    target_setting = settings[0]
    if not target_setting.Details.TargetSettingDetail:
        return DELETE_VALUE if entity.Id and entity.Id > 0 else None
    return ";".join([s.CriterionTypeGroup for s in target_setting.Details.TargetSettingDetail])
    pass

def hotel_setting_to_csv(entity):
    if not entity.Settings or not entity.Settings.Setting:
        return None
    settings = [setting for setting in entity.Settings.Setting if isinstance(setting, HotelSetting_Type)]
    if len(settings) == 0:
        return None
    if len(settings) != 1:
        raise ValueError('Can only have 1 HotelSetting in Settings.')
    hotel_setting = settings[0]
    if not hotel_setting.HotelAdGroupType:
        return DELETE_VALUE if entity.Id and entity.Id > 0 else None
    else:
        return bulk_str(hotel_setting.HotelAdGroupType).replace('|', ',')

def csv_to_target_setting(entity, value):
    target_setting = _CAMPAIGN_OBJECT_FACTORY_V13.create('TargetSetting')
    target_setting.Type = 'TargetSetting'
    if value is None:
        entity.Settings.Setting.append(target_setting)
        return
    tokens = [t.strip() for t in value.split(';')]
    target_setting_detail_list = []
    for token in tokens:
        m_token = match_target_setting(token)
        if m_token:
            target_setting_detail_list.append(create_target_setting_detail(m_token))
    target_setting.Details.TargetSettingDetail.extend(target_setting_detail_list)
    entity.Settings.Setting.append(target_setting)
    pass

def csv_to_hotel_setting(entity, value):
    hotel_setting = _CAMPAIGN_OBJECT_FACTORY_V13.create('HotelSetting')
    hotel_setting.Type = 'HotelSetting'
    if value is None:
        hotel_adgroup_type = None
    else:
        hotel_adgroup_type = value
    hotel_setting.HotelAdGroupType = hotel_adgroup_type
    entity.Settings.Setting.append(hotel_setting)
    pass

def csv_to_commission_rate(entity, value):
    if value is None:
        return
    rate_amount = _CAMPAIGN_OBJECT_FACTORY_V13.create('RateAmount')
    rate_bid = _CAMPAIGN_OBJECT_FACTORY_V13.create('RateBid')
    rate_amount.Amount = float(value) if value else None
    rate_bid.RateAmount = rate_amount
    entity.CommissionRate = rate_bid
    pass

def csv_to_percent_cpc_bid(entity, value):
    if value is None:
        return
    rate_amount = _CAMPAIGN_OBJECT_FACTORY_V13.create('RateAmount')
    rate_bid = _CAMPAIGN_OBJECT_FACTORY_V13.create('RateBid')
    rate_amount.Amount = float(value) if value else None
    rate_bid.RateAmount = rate_amount
    entity.PercentCpcBid = rate_bid
    pass

def match_target_setting(token):

    pattern = re.compile(target_setting_detail_pattern)
    m = pattern.match(token)
    if m:
        return m.group(1)
    return None

def create_target_setting_detail(token):
    target_setting_detail = _CAMPAIGN_OBJECT_FACTORY_V13.create('TargetSettingDetail')
    target_setting_detail.TargetAndBid = True
    target_setting_detail.CriterionTypeGroup = token
    return target_setting_detail
    pass

def parse_rule_PageVisitors(rule_str):
    patternDNF = ')) or (('
    patternCNF = ')) and (('
    patternAnd = ') and ('
    patternOr = ') or ('

    rule = _CAMPAIGN_OBJECT_FACTORY_V13.create('PageVisitorsRule')
    rule.Type = 'PageVisitors'
    rule.NormalForm = NormalForm.Disjunctive
    rule.RuleItemGroups = _CAMPAIGN_OBJECT_FACTORY_V13.create('ArrayOfRuleItemGroup')

    expressionGroups = rule_str.split(patternDNF)
    if len(expressionGroups) == 1:
        expressionGroups = rule_str.split(patternCNF)
        if len(expressionGroups) == 1:
            expressions = rule_str.split(patternOr)
            if len(expressions) == 1:
                expressions = rule_str.split(patternAnd)
                if len(expressions) == 1:
                    parse_rule_items(rule_str)
                else:
                    rule.NormalForm = NormalForm.Disjunctive
            else:
                rule.NormalForm = NormalForm.Conjunctive
        else:
            rule.NormalForm = NormalForm.Conjunctive

    pattern = patternAnd
    if rule.NormalForm == NormalForm.Conjunctive:
        pattern = patternOr

    for expressionGroup in expressionGroups:
        expressionGroup = expressionGroup.strip()
        if expressionGroup[0] == '(':
            expressionGroup = expressionGroup[1:]
        if expressionGroup[-1] == ')':
            expressionGroup = expressionGroup[:-1]

        expressions = expressionGroup.split(pattern)
        rule_item_group = _CAMPAIGN_OBJECT_FACTORY_V13.create('RuleItemGroup')
        for expression in expressions:
            item = parse_string_rule_item(expression)
            rule_item_group.Items.RuleItem.append(item)

        rule.RuleItemGroups.RuleItemGroup.append(rule_item_group)

    return rule


def parse_rule_PageVisitorsWhoVisitedAnotherPage(rule_str):
    rule = _CAMPAIGN_OBJECT_FACTORY_V13.create('PageVisitorsWhoVisitedAnotherPageRule')
    rule.Type = 'PageVisitorsWhoVisitedAnotherPage'

    groups_split = '))) and ((('
    groups_string_list = rule_str.split(groups_split)

    rule.RuleItemGroups = parse_rule_groups(groups_string_list[0])
    rule.AnotherRuleItemGroups = parse_rule_groups(groups_string_list[1])

    return rule


def parse_rule_PageVisitorsWhoDidNotVisitAnotherPage(rule_str):
    rule = _CAMPAIGN_OBJECT_FACTORY_V13.create('PageVisitorsWhoDidNotVisitAnotherPageRule')
    rule.Type = 'PageVisitorsWhoDidNotVisitAnotherPage'

    groups_split = '))) and not ((('
    groups_string_list = rule_str.split(groups_split)

    rule.IncludeRuleItemGroups = parse_rule_groups(groups_string_list[0])
    rule.ExcludeRuleItemGroups = parse_rule_groups(groups_string_list[1])

    return rule


def parse_rule_CustomEvents(rule_str):
    rule = _CAMPAIGN_OBJECT_FACTORY_V13.create('CustomEventsRule')
    rule.Type = 'CustomEvents'

    item_split = ') and ('
    pattern_for_operand_str = r'^(Category|Action|Label|Value) ([^()]*)$'
    pattern_for_operand = re.compile(pattern_for_operand_str)

    pattern_number_item_str = r'^(Equals|GreaterThan|LessThan|GreaterThanEqualTo|LessThanEqualTo) ([^()]*)$'
    pattern_number_item = re.compile(pattern_number_item_str)

    pattern_string_item_str = r'^(Equals|Contains|BeginsWith|EndsWith|NotEquals|DoesNotContain|DoesNotBeginWith|DoesNotEndWith) ([^()]*)$'
    pattern_string_item = re.compile(pattern_string_item_str)

    item_string_list = rule_str.split(item_split)
    for item_string in item_string_list:
        item_string = item_string.strip('(').strip(')')
        match_for_operand = pattern_for_operand.match(item_string)

        if not match_for_operand:
            raise ValueError('Invalid Custom Event rule item: {0}'.format(item_string))

        operand = match_for_operand.group(1)
        operater_and_value_string = match_for_operand.group(2)

        if operand.lower() == 'value':
            match_number_item = pattern_number_item.match(operater_and_value_string)

            if not match_number_item:
                raise ValueError('Invalid Custom Event number rule item: {0}'.format(item_string))

            rule.ValueOperator = parse_number_operator(match_number_item.group(1))
            rule.Value = float(match_number_item.group(2))
        else:
            match_string_item = pattern_string_item.match(operater_and_value_string)

            if not match_string_item:
                raise ValueError('Invalid Custom Event string rule item: {0}'.format(item_string))

            if operand.lower() == 'category':
                rule.CategoryOperator = parse_string_operator(match_string_item.group(1))
                rule.Category = match_string_item.group(2)
            elif operand.lower() == 'label':
                rule.LabelOperator = parse_string_operator(match_string_item.group(1))
                rule.Label = match_string_item.group(2)
            elif operand.lower() == 'action':
                rule.ActionOperator = parse_string_operator(match_string_item.group(1))
                rule.Action = match_string_item.group(2)
            else:
                raise ValueError('Invalid Custom Event string rule operator: {0}'.format(operand))

    return rule


def parse_rule_groups(groups_str):
    group_split = ')) or (('
    group_str_list = groups_str.split(group_split)

    rule_item_groups = _CAMPAIGN_OBJECT_FACTORY_V13.create('ArrayOfRuleItemGroup')
    for group_str in group_str_list:
        item_group = parse_rule_items(group_str)
        rule_item_groups.RuleItemGroup.append(item_group)

    return rule_item_groups


def parse_rule_items(items_str):
    item_split = ') and ('
    item_str_list = items_str.split(item_split)

    rule_item_group = _CAMPAIGN_OBJECT_FACTORY_V13.create('RuleItemGroup')
    for item_str in item_str_list:
        item = parse_string_rule_item(item_str)
        rule_item_group.Items.RuleItem.append(item)

    return rule_item_group


def parse_string_rule_item(item_str):
    item_str = item_str.strip('(').strip(')')
    pattern_str = r'^(Url|ReferrerUrl|EcommPageType|EcommCategory|EcommProdId|Action|None) (Equals|Contains|BeginsWith|EndsWith|NotEquals|DoesNotContain|DoesNotBeginWith|DoesNotEndWith) ([^()]*)$'
    number_pattern_str = r'^(EcommTotalValue) (Equals|GreaterThan|LessThan|GreaterThanEqualTo|LessThanEqualTo|NotEquals) ([^()]*)$'
    pattern = re.compile(pattern_str)
    number_pattern = re.compile(number_pattern_str)

    match = pattern.match(item_str)
    if match:
        item = _CAMPAIGN_OBJECT_FACTORY_V13.create('StringRuleItem')
        item.Type = 'String'
        item.Operand = match.group(1)
        item.Operator = parse_string_operator(match.group(2))
        item.Value = match.group(3)
    else:
        match = number_pattern.match(item_str)
        if match:
            item = _CAMPAIGN_OBJECT_FACTORY_V13.create('NumberRuleItem')
            item.Type = 'Number'
            item.Operand = match.group(1)
            item.Operator = parse_number_operator(match.group(2))
            item.Value = match.group(3)
        else:
            ValueError('Invalid Rule Item:{0}'.format(item_str))

    return item


def parse_number_operator(operator):
    oper = operator.lower()
    if oper == 'equals':
        return NumberOperator.Equals
    if oper == 'greaterthan':
        return NumberOperator.GreaterThan
    if oper == 'lessthan':
        return NumberOperator.LessThan
    if oper == 'greaterthanequalto':
        return NumberOperator.GreaterThanEqualTo
    if oper == 'lessthanequalto':
        return NumberOperator.LessThanEqualTo
    if oper == 'notequals':
        return NumberOperator.NotEquals

    return None


def parse_string_operator(operator):
    oper = operator.lower()
    if oper == 'equals':
        return StringOperator.Equals
    if oper == 'contains':
        return StringOperator.Contains
    if oper == 'beginswith':
        return StringOperator.BeginsWith
    if oper == 'endswith':
        return StringOperator.EndsWith
    if oper == 'notequals':
        return StringOperator.NotEquals
    if oper == 'doesnotcontain':
        return StringOperator.DoesNotContain
    if oper == 'doesnotbeginwith':
        return StringOperator.DoesNotBeginWith
    if oper == 'doesnotendwith':
        return StringOperator.DoesNotEndWith

    return None


def csv_to_field_SupportedCampaignTypes(entity, value):
    if value is None or value == '':
        return
    splitter = re.compile(r';')
    entity.string = splitter.split(value)


def field_to_csv_SupportedCampaignTypes(entity):
    if entity is None or entity.string is None:
        return None
    if len(entity.string) == 0:
        return None
    return ';'.join(entity.string)


def field_to_csv_CustomAttributes(custom_attributes):
    if custom_attributes is None:
        return None
    if len(custom_attributes) > 0:
        return json.dumps(custom_attributes)
    return None

def csv_to_field_CustomAttributes(feed, value):
    if value is None or value == '':
        return
    feed.custom_attributes = json.loads(value)

def field_to_csv_Ids(ids, entity_id):
    if ids is None and entity_id is not None and entity_id > 0:
        return DELETE_VALUE

    if ids is None or len(ids.long) == 0:
        return None
    return ';'.join(str(id) for id in ids.long)

def csv_to_field_PageFeedIds(value):
    if value is None or value == DELETE_VALUE:
        return None
    if len(value) == 0:
        return []
    return [int(i) for i in value.split(';')]

def combination_rules_to_bulkstring(combination_rules):
    if len(combination_rules.CombinationRule) == 0:
        return None

    return '&'.join([r.Operator + '(' + ','.join([str(id) for id in r.AudienceIds.long]) + ')' for r in combination_rules.CombinationRule])

def parse_combination_rules(combination_list, value):
    if value is None or len(value) == 0:
        return None

    rules = value.split('&')
    pattern = re.compile(combine_rule_pattern, re.IGNORECASE)
    for rule in rules:
        m = pattern.match(rule)
        if m:
            combination_rule = _CAMPAIGN_OBJECT_FACTORY_V13.create('CombinationRule')
            combination_rule.Operator = to_operation(m.group(1))
            combination_rule.AudienceIds.long.extend([int(id) for id in m.group(2).split(',') if len(id) > 0])
            combination_list.CombinationRules.CombinationRule.append(combination_rule)
def to_operation(op):
    if op.lower() == 'and': return 'And'
    if op.lower() == 'or': return 'Or'
    if op.lower() == 'not': return 'Not'
    return none

def bulk_datetime_str2(value):
        if value is None:
            return None

        return value.strftime('%Y/%m/%d %H:%M:%S')

def parse_datetime2(value):

        if not value:
            return None
        try:
            return datetime.strptime(value, '%Y/%m/%d %H:%M:%S')
        except Exception:
            return parse_datetime(value)
