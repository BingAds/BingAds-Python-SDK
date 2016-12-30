from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V10
from bingads.v10.bulk.entities import QualityScoreData, PerformanceData
from bingads.v10.internal.bulk.string_table import _StringTable
from bingads.v10.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v10.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
# from bingads.internal.extensions import bulk_str, csv_to_budget, budget_to_csv
from bingads.internal.extensions import *

_ShoppingSetting = type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ShoppingSetting'))

class BulkCampaign(_SingleRecordBulkEntity):
    """ Represents a campaign that can be read or written in a bulk file.

    This class exposes the :attr:`campaign` property that can be read and written as fields of the
    Campaign record in a bulk file.

    For more information, see Campaign at http://go.microsoft.com/fwlink/?LinkID=620239.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, campaign=None):
        super(BulkCampaign, self).__init__()

        self._account_id = account_id
        self._campaign = campaign
        self._quality_score_data = None
        self._performance_data = None
        self._budget_name = None

    @property
    def account_id(self):
        """ The identifier of the account that contains the campaign.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    @property
    def budget_name(self):
        """
        The budget name that the campaign associated, only for campaigns that use a shared budget

        Corresponds to 'Budget Name' field in bulk file.
        :rtype: str
        """
        return self._budget_name

    @budget_name.setter
    def budget_name(self, value):
        self._budget_name = value

    @property
    def campaign(self):
        """ Defines a campaign within an account.

        See Campaign at https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-campaign.aspx
        """

        return self._campaign

    @campaign.setter
    def campaign(self, campaign):
        self._campaign = campaign

    @property
    def quality_score_data(self):
        """ The quality score data for the campaign.

        :rtype: QualityScoreData
        """

        return self._quality_score_data

    @property
    def performance_data(self):
        """ The historical performance data for the campaign

        :rtype: PerformanceData
        """

        return self._performance_data

    def _get_shopping_setting(self):
        if not self.campaign.Settings.Setting:
            return None
        shopping_settings = [setting for setting in self.campaign.Settings.Setting if
                             isinstance(setting, _ShoppingSetting)]
        if len(shopping_settings) != 1:
            raise ValueError('Can only have 1 ShoppingSetting in Campaign Settings.')
        return shopping_settings[0]

    @staticmethod
    def _write_campaign_type(c):
        if not c.campaign.CampaignType:
            return None
        if len(c.campaign.CampaignType) != 1:
            raise ValueError("Only 1 CampaignType can be set in Campaign")
        return c.campaign.CampaignType[0]

    @staticmethod
    def _read_campaign_type(c, v):
        if not v:
            return []
        campaign_type = v
        c.campaign.CampaignType = [campaign_type]
        if campaign_type.lower() == 'shopping':
            c.campaign.Settings = _CAMPAIGN_OBJECT_FACTORY_V10.create('ArrayOfSetting')
            shopping_setting = _CAMPAIGN_OBJECT_FACTORY_V10.create('ShoppingSetting')
            shopping_setting.Type = 'ShoppingSetting'
            c.campaign.Settings.Setting = [shopping_setting]

    @staticmethod
    def _write_store_id(c):
        if not c.campaign.CampaignType:
            return None
        if 'shopping' in [campaign_type.lower() for campaign_type in c.campaign.CampaignType]:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            return bulk_str(shopping_setting.StoreId)

    @staticmethod
    def _read_store_id(c, v):
        if not c.campaign.CampaignType:
            return None
        if 'shopping' in [campaign_type.lower() for campaign_type in c.campaign.CampaignType]:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            shopping_setting.StoreId = int(v) if v else None

    @staticmethod
    def _write_priority(c):
        if not c.campaign.CampaignType:
            return None
        if 'shopping' in [campaign_type.lower() for campaign_type in c.campaign.CampaignType]:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            return bulk_str(shopping_setting.Priority)

    @staticmethod
    def _read_priority(c, v):
        if not c.campaign.CampaignType:
            return None
        if 'shopping' in [campaign_type.lower() for campaign_type in c.campaign.CampaignType]:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            shopping_setting.Priority = int(v) if v else None

    @staticmethod
    def _write_sales_country_code(c):
        if not c.campaign.CampaignType:
            return None
        if 'shopping' in [campaign_type.lower() for campaign_type in c.campaign.CampaignType]:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            return shopping_setting.SalesCountryCode

    @staticmethod
    def _read_sales_country_code(c, v):
        if not c.campaign.CampaignType:
            return None
        if 'shopping' in [campaign_type.lower() for campaign_type in c.campaign.CampaignType]:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            shopping_setting.SalesCountryCode = v

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.CampaignType,
            field_to_csv=lambda c: BulkCampaign._write_campaign_type(c),
            csv_to_field=lambda c, v: BulkCampaign._read_campaign_type(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.campaign.Status),
            csv_to_field=lambda c, v: setattr(
                c.campaign,
                'Status',
                v if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.campaign.Id),
            csv_to_field=lambda c, v: setattr(
                c.campaign,
                'Id',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, '_account_id', int(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign.Name,
            csv_to_field=lambda c, v: setattr(c.campaign, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TimeZone,
            field_to_csv=lambda c: c.campaign.TimeZone,
            csv_to_field=lambda c, v: setattr(c.campaign, 'TimeZone', v)
        ),
        _ComplexBulkMapping(budget_to_csv, csv_to_budget),
        _SimpleBulkMapping(
            header=_StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.campaign.NativeBidAdjustment),
            csv_to_field=lambda c, v: setattr(
                c.campaign,
                'NativeBidAdjustment',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.BingMerchantCenterId,
            field_to_csv=lambda c: BulkCampaign._write_store_id(c),
            csv_to_field=lambda c, v: BulkCampaign._read_store_id(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CampaignPriority,
            field_to_csv=lambda c: BulkCampaign._write_priority(c),
            csv_to_field=lambda c, v: BulkCampaign._read_priority(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CountryCode,
            field_to_csv=lambda c: BulkCampaign._write_sales_country_code(c),
            csv_to_field=lambda c, v: BulkCampaign._read_sales_country_code(c, v)
        ),
        _SimpleBulkMapping(
            # TODO now use bulk_str not bulk_optional_str
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.campaign.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.campaign, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.campaign),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.campaign, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidStrategyType,
            field_to_csv=lambda c: field_to_csv_BidStrategyType(c.campaign),
            csv_to_field=lambda c, v: csv_to_field_BidStrategyType(c.campaign, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BudgetId,
            field_to_csv=lambda c: bulk_str(c.campaign.BudgetId),
            csv_to_field=lambda c, v: setattr(c.campaign, 'BudgetId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BudgetType,
            field_to_csv=lambda c: bulk_str(c.campaign.BudgetType),
            csv_to_field=lambda c, v: csv_to_field_BudgetType(c.campaign, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BudgetName,
            field_to_csv=lambda c: bulk_str(c.budget_name),
            csv_to_field=lambda c, v: setattr(c, 'budget_name', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Website,
            field_to_csv=lambda c: field_to_csv_DSAWebsite(c.campaign),
            csv_to_field=lambda c, v: csv_to_field_DSAWebsite(c.campaign, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DomainLanguage,
            field_to_csv=lambda c: field_to_csv_DSADomainLanguage(c.campaign),
            csv_to_field=lambda c, v: csv_to_field_DSADomainLanguage(c.campaign, v)
        ),
    ]

    def read_additional_data(self, stream_reader):
        super(BulkCampaign, self).read_additional_data(stream_reader)

    def process_mappings_from_row_values(self, row_values):
        self._campaign = _CAMPAIGN_OBJECT_FACTORY_V10.create('Campaign')
        row_values.convert_to_entity(self, BulkCampaign._MAPPINGS)
        self._quality_score_data = QualityScoreData.read_from_row_values_or_null(row_values)
        self._performance_data = PerformanceData.read_from_row_values_or_null(row_values)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.campaign, 'campaign')
        self.convert_to_values(row_values, BulkCampaign._MAPPINGS)
        if not exclude_readonly_data:
            QualityScoreData.write_to_row_values_if_not_null(self.quality_score_data, row_values)
            PerformanceData.write_to_row_values_if_not_null(self.performance_data, row_values)
