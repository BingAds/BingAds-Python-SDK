from datetime import datetime

from bingads.v10.internal.bulk.string_table import _StringTable
from six import PY2
import re
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V10, _CAMPAIGN_MANAGEMENT_SERVICE_V10


DELETE_VALUE = "delete_value"
_BULK_DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'
_BULK_DATETIME_FORMAT_2 = '%m/%d/%Y %H:%M:%S.%f'
_BULK_DATE_FORMAT = "%m/%d/%Y"

url_splitter = ";\\s*(?=https?://)"
custom_param_splitter = "(?<!\\\\);\\s*"
custom_param_pattern = "^\\{_(.*?)\\}=(.*$)"

BudgetLimitType = _CAMPAIGN_OBJECT_FACTORY_V10.create('BudgetLimitType')
DynamicSearchAdsSetting = _CAMPAIGN_OBJECT_FACTORY_V10.create('DynamicSearchAdsSetting')
Webpage = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:Webpage')
WebpageConditionOperand = _CAMPAIGN_OBJECT_FACTORY_V10.create('WebpageConditionOperand')

def bulk_str(value):
    if value is None or (hasattr(value, 'value') and value.value is None):
        return None
    if isinstance(value, str):
        return value
    if PY2:
        if isinstance(value, unicode):
            return value
    return str(value)


def bulk_upper_str(value):
    s = bulk_str(value)
    if s is None:
        return None
    return s.upper()


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
    if _is_daily_budget(budget_type):
        bulk_campaign.campaign.DailyBudget = budget_value
    else:
        bulk_campaign.campaign.MonthlyBudget = budget_value


def budget_to_csv(bulk_campaign, row_values):
    budget_type = bulk_campaign.campaign.BudgetType
    if not budget_type:
        return

    if _is_daily_budget(str(budget_type)):
        row_values[_StringTable.Budget] = bulk_str(bulk_campaign.campaign.DailyBudget)
    else:
        row_values[_StringTable.Budget] = bulk_str(bulk_campaign.campaign.MonthlyBudget)


def bulk_optional_str(value):
    if value is None:
        return None
    if not value:
        return DELETE_VALUE
    return value


def csv_to_status(c, v):
    if v == 'Expired':
        c.ad_group.Status = 'Expired'
        c._is_expired = True
    else:
        c.ad_group.Status = v if v else None


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

    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, _BULK_DATETIME_FORMAT)
    except Exception:
        return datetime.strptime(dt_str, _BULK_DATETIME_FORMAT_2)


def parse_date(d_str):
    if not d_str:
        return None
    parsed_date = datetime.strptime(d_str, _BULK_DATE_FORMAT)
    bing_ads_date = _CAMPAIGN_OBJECT_FACTORY_V10.create('Date')
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
        raise ValueError("Unknown device preference")

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
    # media_ids? "ns4:ArrayOflong"
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
        return DELETE_VALUE
    # The default case when entity created
    if len(entity.UrlCustomParameters.Parameters.CustomParameter) == 0:
        return None
    params = []
    for parameter in entity.UrlCustomParameters.Parameters.CustomParameter:
        params.append('{{_{0}}}={1}'.format(parameter.Key, escape_parameter_text(parameter.Value)))
    return '; '.join(params)


def csv_to_field_UrlCustomParameters(entity, value):
    if value is None or value.strip() == '':
        return
    splitter = re.compile(custom_param_splitter)
    pattern = re.compile(custom_param_pattern)
    #params = _CAMPAIGN_OBJECT_FACTORY_V10.create("ns0:ArrayOfCustomParameter")
    params = []
    param_strs = splitter.split(value)
    for param_str in param_strs:
        match = pattern.match(param_str)
        if match:
            custom_parameter = _CAMPAIGN_OBJECT_FACTORY_V10.create("ns0:CustomParameter")
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


def field_to_csv_Urls(entity):
    """
    parse entity to csv content
    :param entity: FinalUrls / FinalMobileUrls
    :return: csv content
    """
    if entity is None:
        return None
    if entity.string is None:
        return DELETE_VALUE
    if len(entity.string) == 0:
        return None
    return '; '.join(entity.string)


def field_to_csv_BidStrategyType(entity):
    """
    parse entity to csv content
    :param entity: entity which has BiddingScheme attribute
    :return: csv content
    """
    if entity.BiddingScheme is None or type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:BiddingScheme')):
        return None
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:EnhancedCpcBiddingScheme')):
        return 'EnhancedCpc'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:InheritFromParentBiddingScheme')):
        return 'InheritFromParent'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:MaxConversionsBiddingScheme')):
        return 'MaxConversions'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:ManualCpcBiddingScheme')):
        return 'ManualCpc'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:TargetCpaBiddingScheme')):
        return 'TargetCpa'
    elif type(entity.BiddingScheme) == type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:MaxClicksBiddingScheme')):
        return 'MaxClicks'
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
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:EnhancedCpcBiddingScheme')
    elif value == 'InheritFromParent':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:InheritFromParentBiddingScheme')
    elif value == 'MaxConversions':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:MaxConversionsBiddingScheme')
    elif value == 'ManualCpc':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:ManualCpcBiddingScheme')
    elif value == 'TargetCpa':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:TargetCpaBiddingScheme')
    elif value == 'MaxClicks':
        entity.BiddingScheme = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:MaxClicksBiddingScheme')
    else:
        raise ValueError('Unknown Bid Strategy Type')
    entity.BiddingScheme.Type = value


def field_to_csv_AdFormatPreference(entity):
    """
    convert entity field to csv content
    :param entity: entity which has ForwardCompatibilityMap attribute
    :return:
    """
    if entity.ForwardCompatibilityMap is None or entity.ForwardCompatibilityMap.KeyValuePairOfstringstring is None \
        or len(entity.ForwardCompatibilityMap.KeyValuePairOfstringstring) == 0:
        return None
    for key_value_pair in entity.ForwardCompatibilityMap.KeyValuePairOfstringstring:
        if key_value_pair.key == 'NativePreference':
            if key_value_pair.value.lower() == 'true':
                return 'Native'
            elif key_value_pair.value.lower() == 'false':
                return 'All'
            else:
                raise ValueError('Unknown value for Native Preference: {0}'.format(key_value_pair.value))
    return None


def csv_to_field_AdFormatPreference(entity, value):
    """
    parse csv content and set entity attribute
    :param entity: entity which has ForwardCompatibilityMap attribute
    :param value: csv content value
    :return:
    """
    ad_format_preference = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns2:KeyValuePairOfstringstring')
    ad_format_preference.key = 'NativePreference'
    if value is None or value == '' or value == 'All':
        ad_format_preference.value = 'False'
    elif value == 'Native':
        ad_format_preference.value = 'True'
    else:
        raise ValueError('Unknown value for Native Preference: {0}'.format(value))
    entity.ForwardCompatibilityMap = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns2:ArrayOfKeyValuePairOfstringstring')
    entity.ForwardCompatibilityMap.KeyValuePairOfstringstring.append(ad_format_preference)


def csv_to_field_StructuredSnippetValues(entity, value):
    if value is not None and value != '':
        entity.Values.string = value.split(';')

def field_to_csv_StructuredSnippetValues(entity):
    if entity.Values is not None and entity.Values.string is not None and len(entity.Values.string) > 0:
        return ';'.join(entity.Values.string)
    return None


def ad_rotation_bulk_str(value):
    if value is None:
        return None
    elif value.Type is None:
        return DELETE_VALUE
    else:
        return bulk_str(value.Type)


def parse_ad_rotation(value):
    if not value:
        return None
    ad_rotation = _CAMPAIGN_OBJECT_FACTORY_V10.create('AdRotation')
    ad_rotation.Type = None if value == DELETE_VALUE else value
    return ad_rotation


def parse_ad_group_bid(value):
    if not value:
        return None
    bid = _CAMPAIGN_OBJECT_FACTORY_V10.create('Bid')
    bid.Amount = float(value)
    return bid


def ad_group_bid_bulk_str(value):
    if value is None or value.Amount is None:
        return None
    return bulk_str(value.Amount)


def keyword_bid_bulk_str(value):
    if value is None:
        return DELETE_VALUE
    if value.Amount is None:
        return None
    return bulk_str(value.Amount)


def parse_keyword_bid(value):
    bid = _CAMPAIGN_OBJECT_FACTORY_V10.create('Bid')
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


def parse_minute(value):
    minute_number = int(value)
    if minute_number == 0:
        return 'Zero'
    elif minute_number == 15:
        return 'Fifteen'
    elif minute_number == 30:
        return 'Thirty'
    elif minute_number == 45:
        return 'FortyFive'
    raise ValueError('Unknown minute')


def format_Day(value):
    Day = _CAMPAIGN_OBJECT_FACTORY_V10.create('Day')
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


def field_to_csv_AdSchedule(entity):
    """
    get the bulk string for Scheduling DayTimeRanges
    :param entity: Scheduling entity
    :return: bulk str
    """
    if entity is None:
        return None
    if entity.DayTimeRanges is None:
        return DELETE_VALUE
    return ';'.join('({0}[{1:02d}:{2:02d}-{3:02d}:{4:02d}])'
                    .format(d.Day, d.StartHour, int(minute_bulk_str(d.StartMinute)), d.EndHour, int(minute_bulk_str(d.EndMinute)))
                    for d in entity.DayTimeRanges.DayTime
                    )


def csv_to_field_AdSchedule(entity, value):
    if value is None or value.strip() == '':
        return
    daytime_strs = value.split(';')
    ad_schedule_pattern = '\((Monday|Tuesday|Wednesday|ThursDay|Friday|Saturday|Sunday)\[(\d\d?):(\d\d)-(\d\d?):(\d\d)\]\)'
    pattern = re.compile(ad_schedule_pattern, re.IGNORECASE)
    daytimes = []
    for daytime_str in daytime_strs:
        match = pattern.match(daytime_str)
        if match:
            daytime = _CAMPAIGN_OBJECT_FACTORY_V10.create('DayTime')
            daytime.Day = format_Day(match.group(1))
            daytime.StartHour = int(match.group(2))
            daytime.StartMinute = parse_minute(match.group(3))
            daytime.EndHour = int(match.group(4))
            daytime.EndMinute = parse_minute(match.group(5))
            daytimes.append(daytime)
        else:
            raise ValueError('Unable to parse DayTime: {0}'.format(daytime_str))
    entity.DayTimeRanges.DayTime = daytimes


def field_to_csv_SchedulingStartDate(entity):
    """
    write scheduling StartDate to bulk string
    :param entity: Scheduling entity
    :return: date bulk string
    """
    if entity is None:
        return None
    elif entity.StartDate is None:
        return DELETE_VALUE
    # this case is what the suds creates by default. return None instead of a delete value
    elif entity.StartDate.Day is None and entity.StartDate.Month is None and entity.StartDate.Year is None:
        return None
    return '{0!s}/{1!s}/{2!s}'.format(entity.StartDate.Month, entity.StartDate.Day, entity.StartDate.Year)


def field_to_csv_SchedulingEndDate(entity):
    """
    write scheduling EndDate to bulk string
    :param entity: Scheduling entity
    :return: date bulk string
    """
    if entity is None:
        return None
    elif entity.EndDate is None:
        return DELETE_VALUE
    # this case is what the suds creates by default. return None instead of a delete value
    elif entity.EndDate.Day is None and entity.EndDate.Month is None and entity.EndDate.Year is None:
        return None
    return '{0!s}/{1!s}/{2!s}'.format(entity.EndDate.Month, entity.EndDate.Day, entity.EndDate.Year)


def field_to_csv_UseSearcherTimeZone(entity):
    """
    get Scheduling UseSearcherTimeZone bulk str
    :param entity: Scheduling entity
    :return: bulk str
    """
    if entity is None:
        return None
    # this case is what suds creates by default, while set it to delete value since there's no other case for delete value
    elif entity.UseSearcherTimeZone is None:
        return DELETE_VALUE
    else:
        return str(entity.UseSearcherTimeZone)


def csv_to_field_BudgetType(entity, value):
    if value is None or value == '':
        entity.BudgetType = None
    elif value == 'MonthlyBudgetSpendUntilDepleted':
        entity.BudgetType = BudgetLimitType.MonthlyBudgetSpendUntilDepleted
    elif value == 'DailyBudgetAccelerated':
        entity.BudgetType = BudgetLimitType.DailyBudgetAccelerated
    elif value == 'DailyBudgetStandard':
        entity.BudgetType = BudgetLimitType.DailyBudgetStandard
    else:
        raise ValueError('Unable to parse BudgetType: {0}'.format(value))


def csv_to_field_DSAWebsite(entity, value):
    """
    Set Campaign settings Domain Name from bulk value if the campaign type is Dynamic Search Campaign
    :param entity: campaign entity
    :param value: bulk str value
    """
    if not entity.CampaignType or len(entity.CampaignType) == 0 or entity.CampaignType[0] != "DynamicSearchAds":
        return
    if len(entity.Settings.Setting) > 0 and entity.Settings.Setting[0].Type == 'DynamicSearchAdsSetting':
        entity.Settings.Setting[0].DomainName = value
    else:
        setting = _CAMPAIGN_OBJECT_FACTORY_V10.create('DynamicSearchAdsSetting')
        setting.DomainName = value
        setting.Type = 'DynamicSearchAdsSetting'
        entity.Settings.Setting.append(setting)


def field_to_csv_DSAWebsite(entity):
    """
    convert campaign settings Domain Name to bulk str if the campaign is Dynamic Search Campaign
    :param entity: campaign entity
    :return: bulk str
    """
    if entity.CampaignType is not None and (entity.CampaignType == 'DynamicSearchAds' or (
            len(entity.CampaignType) != 0 and entity.CampaignType[0] == 'DynamicSearchAds')):
        if entity.Settings is None or entity.Settings.Setting is None or len(entity.Settings.Setting) == 0:
            return None
        setting = entity.Settings.Setting[0]
        if isinstance(setting, type(DynamicSearchAdsSetting)):
            return setting.DomainName
    return None


def csv_to_field_DSADomainLanguage(entity, value):
    """
    Set Campaign settings Language from bulk value if the campaign type is Dynamic Search Campaign
    :param entity: campaign entity
    :param value: bulk str value
    """
    if not entity.CampaignType or len(entity.CampaignType) == 0 or entity.CampaignType[0] != "DynamicSearchAds":
        return
    if len(entity.Settings.Setting) > 0 and entity.Settings.Setting[0].Type == 'DynamicSearchAdsSetting':
        entity.Settings.Setting[0].Language = value
    else:
        setting = _CAMPAIGN_OBJECT_FACTORY_V10.create('DynamicSearchAdsSetting')
        setting.Language = value
        setting.Type = 'DynamicSearchAdsSetting'
        entity.Settings.Setting.append(setting)


def field_to_csv_DSADomainLanguage(entity):
    """
    convert campaign settings Language to bulk str if the campaign is Dynamic Search Campaign
    :param entity: campaign entity
    :return: bulk str
    """
    if entity.CampaignType is not None and (entity.CampaignType == 'DynamicSearchAds' or (
            len(entity.CampaignType) != 0 and entity.CampaignType[0] == 'DynamicSearchAds')):
        if not entity.Settings or not entity.Settings.Setting or len(entity.Settings.Setting) == 0:
            return None
        setting = entity.Settings.Setting[0]
        if isinstance(setting, type(DynamicSearchAdsSetting)):
            return setting.Language

    return None


def field_to_csv_WebpageParameter_CriterionName(entity):
    if entity.Criterion is None or entity.Criterion.Parameter is None or entity.Criterion.Parameter.CriterionName is None:
        return None
    if not entity.Criterion.Parameter.CriterionName:
        return DELETE_VALUE
    return entity.Criterion.Parameter.CriterionName


def csv_to_field_WebpageParameter_CriterionName(entity, value):
    if value is None or value == '':
        return
    if entity.Criterion is not None and isinstance(entity.Criterion, type(Webpage)):
        entity.Criterion.Parameter.CriterionName = value
    else:
        webpage = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:Webpage')
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

        conditions = entity.Criterion.Parameter.Conditions.WebpageCondition
        for i in range(0, len(conditions)):
            row_values[condition_prefix + str(i + 1)] = conditions[i].Operand
            row_values[value_prefix + str(i + 1)] = conditions[i].Argument


def csv_to_entity_DSAWebpageParameter(row_values, entity):
    """
    convert Campaign/Ad Group Criterion (WebpagePage) Web page parameters to bulk row values
    :param row_values: bulk row values
    :param entity: campaign/ad group criterion entity
    """
    MAX_NUMBER_OF_CONDITIONS = 3
    condition_prefix = _StringTable.DynamicAdTargetCondition1[:-1]
    value_prefix = _StringTable.DynamicAdTargetValue1[:-1]

    conditions = []
    for i in range(0, MAX_NUMBER_OF_CONDITIONS):
        condition_success, webpage_condition = row_values.try_get_value(condition_prefix + str(i + 1))
        value_success, webpage_value = row_values.try_get_value(value_prefix + str(i + 1))
        if condition_success and value_success and webpage_condition is not None and webpage_condition != '':
            condition = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:WebpageCondition')
            if webpage_condition.lower() == 'url':
                condition.Operand = WebpageConditionOperand.Url
            elif webpage_condition.lower() == "category":
                condition.Operand = WebpageConditionOperand.Category
            elif webpage_condition.lower() == 'pagetitle':
                condition.Operand = WebpageConditionOperand.PageTitle
            elif webpage_condition.lower() == 'pagecontent':
                condition.Operand = WebpageConditionOperand.PageContent
            else:
                raise ValueError("Unknown WebpageConditionOperand value: {0}".format(webpage_condition))

            condition.Argument = webpage_value
            conditions.append(condition)

    if len(conditions) > 0:
        if entity.Criterion is not None and isinstance(entity.Criterion, type(Webpage)):
            entity.Criterion.Parameter.Conditions.WebpageCondition = conditions
        else:
            webpage = _CAMPAIGN_OBJECT_FACTORY_V10.create('ns0:Webpage')
            webpage.Parameter.Conditions.WebpageCondition = conditions
            entity.Criterion = webpage


def parse_bool(value):
    if value is None or value == '':
        return None
    elif value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise ValueError('Unable to parse bool value: {0}.'.format(value))
