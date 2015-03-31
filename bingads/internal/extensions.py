from datetime import datetime

from bingads.internal.bulk.string_table import _StringTable
from six import PY2

from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY


DELETE_VALUE = "delete_value"
_BULK_DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'
_BULK_DATETIME_FORMAT_2 = '%m/%d/%Y %H:%M:%S.%f'
_BULK_DATE_FORMAT = "%m/%d/%Y"


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
    if value is None:
        return None
    return '{0!s}/{1!s}/{2!s}'.format(value.Month, value.Day, value.Year)


def bulk_datetime_str(value):
    if value is None:
        return None
    return value.strftime(_BULK_DATETIME_FORMAT)


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
        c.ad_group.Status = 'Deleted'
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
    bing_ads_date = _CAMPAIGN_OBJECT_FACTORY.create('Date')
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
    ad_rotation = _CAMPAIGN_OBJECT_FACTORY.create('AdRotation')
    ad_rotation.Type = None if value == DELETE_VALUE else value
    return ad_rotation


def parse_ad_group_bid(value):
    if not value:
        return None
    bid = _CAMPAIGN_OBJECT_FACTORY.create('Bid')
    bid.Amount = float(value)
    return bid


def ad_group_bid_bulk_str(value):
    if value is None or value.Amount is None:
        return None
    return bulk_str(value.Amount)


def keyword_bid_bulk_str(value):
    if value is None:
        return None
    if value.Amount is None:
        return DELETE_VALUE
    return bulk_str(value.Amount)


def parse_keyword_bid(value):
    bid = _CAMPAIGN_OBJECT_FACTORY.create('Bid')
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
