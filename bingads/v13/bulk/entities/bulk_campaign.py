from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities import QualityScoreData
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.extensions import *
from decimal import Decimal

_DynamicFeedSetting = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('DynamicFeedSetting'))
_TargetSetting = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('TargetSetting'))
_ShoppingSetting = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('ShoppingSetting'))
_DsaSetting = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('DynamicSearchAdsSetting'))
_DisclaimerSetting = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('DisclaimerSetting'))
_VerifiedTrackingSetting = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('VerifiedTrackingSetting'))
_PerformanceMaxSetting = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('PerformanceMaxSetting'))
_NewCustomerAcquisitionGoalSetting = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('NewCustomerAcquisitionGoalSetting'))

class BulkCampaign(_SingleRecordBulkEntity):
    """ Represents a campaign that can be read or written in a bulk file.

    This class exposes the :attr:`campaign` property that can be read and written as fields of the
    Campaign record in a bulk file.

    For more information, see Campaign at https://go.microsoft.com/fwlink/?linkid=846127.

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
        self._bid_strategy_name = None
        self._verified_tracking_data = None
        self._destination_channel = None
        self._is_multi_channel_campaign = None
        self._should_serve_on_msan = None

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
    def bid_strategy_name(self):
        """
        The budget name that the campaign associated, only for campaigns that use a shared budget

        Corresponds to 'Budget Name' field in bulk file.
        :rtype: str
        """
        return self._bid_strategy_name

    @bid_strategy_name.setter
    def bid_strategy_name(self, value):
        self._bid_strategy_name = value

    @property
    def verified_tracking_data(self):
        """
        The verified tracking data that the campaign associated, only for audience campaigns

        Corresponds to 'Verified Tracking Setting' field in bulk file.
        :rtype: ArrayOfArrayOfKeyValuePairOfstringstring
        """
        return self._verified_tracking_data

    @verified_tracking_data.setter
    def verified_tracking_data(self, value):
        self._verified_tracking_data = value

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

        See Campaign at https://docs.microsoft.com/en-us/bingads/campaign-management-service/campaign?view=bingads-13
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
    def destination_channel(self):
        return self._destination_channel

    @destination_channel.setter
    def destination_channel(self, value):
        self._destination_channel = value

    @property
    def is_multi_channel_campaign(self):
        return self._is_multi_channel_campaign

    @is_multi_channel_campaign.setter
    def is_multi_channel_campaign(self, value):
        self._is_multi_channel_campaign = value

    @property
    def should_serve_on_msan(self):
        return self._should_serve_on_msan

    @should_serve_on_msan.setter
    def should_serve_on_msan(self, value):
        self._should_serve_on_msan = value

    def _get_dynamic_feed_setting(self):
        return self._get_setting(_DynamicFeedSetting, 'DynamicFeedSetting')

    def _get_shopping_setting(self):
        return self._get_setting(_ShoppingSetting, 'ShoppingSetting')

    def _get_target_setting(self):
        return self._get_setting(_TargetSetting, 'TargetSetting')

    def _get_dsa_setting(self):
        return self._get_setting(_DsaSetting, 'DynamicSearchAdsSetting')

    def _get_disclaimer_setting(self):
        return self._get_setting(_DisclaimerSetting, 'DisclaimerSetting')

    def _get_verified_tracking_setting(self):
        return self._get_setting(_VerifiedTrackingSetting, 'VerifiedTrackingSetting')

    def _get_performance_max_setting(self):
        return self._get_setting(_PerformanceMaxSetting, 'PerformanceMaxSetting')

    def _get_new_customer_acquisition_goal_setting(self):
        return self._get_setting(_NewCustomerAcquisitionGoalSetting, 'NewCustomerAcquisitionGoalSetting')

    def _get_setting(self, setting_type, setting_name):
        if not self.campaign.Settings.Setting:
            return None
        settings = [setting for setting in self.campaign.Settings.Setting if
                             isinstance(setting, setting_type)]
        if len(settings) > 1:
            raise ValueError('Can only have 1 ' + setting_name +  ' at most in Campaign Settings.')
        elif len(settings) == 0:
            return None
        return settings[0]

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
            BulkCampaign._create_campaign_setting(c.campaign, 'ShoppingSetting')
        if campaign_type.lower() == 'audience':
            BulkCampaign._create_campaign_setting(c.campaign, 'DynamicFeedSetting')
            BulkCampaign._create_campaign_setting(c.campaign, 'ShoppingSetting')
            BulkCampaign._create_campaign_setting(c.campaign, 'VerifiedTrackingSetting')
        if campaign_type.lower() == 'dynamicsearchads' or campaign_type.lower() == 'search':
            BulkCampaign._create_campaign_setting(c.campaign, 'DynamicSearchAdsSetting')
            BulkCampaign._create_campaign_setting(c.campaign, 'DisclaimerSetting')
        if campaign_type.lower() == 'performancemax':
            BulkCampaign._create_campaign_setting(c.campaign, 'PerformanceMaxSetting')
            BulkCampaign._create_campaign_setting(c.campaign, 'ShoppingSetting')
            BulkCampaign._create_campaign_setting(c.campaign, 'NewCustomerAcquisitionGoalSetting')

    @staticmethod
    def _create_campaign_setting(campaign, setting_type):
        if not campaign.Settings:
            campaign.Settings = _CAMPAIGN_OBJECT_FACTORY_V13.create('ArrayOfSetting')

        setting = _CAMPAIGN_OBJECT_FACTORY_V13.create(setting_type)
        setting.Type = setting_type
        campaign.Settings.Setting.append(setting)

    @staticmethod
    def _write_final_url_expansion_opt_out(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            return bulk_str(performance_max_setting.FinalUrlExpansionOptOut)

    @staticmethod
    def _read_final_url_expansion_opt_out(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            performance_max_setting.FinalUrlExpansionOptOut = parse_bool(v)

    @staticmethod
    def _write_store_id(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'shopping' in campgaign_types or 'audience' in campgaign_types:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            return bulk_str(shopping_setting.StoreId)

    @staticmethod
    def _read_store_id(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'shopping' in campgaign_types or 'audience' in campgaign_types:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            shopping_setting.StoreId = int(v) if v else None

    @staticmethod
    def _write_priority(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'shopping' in campgaign_types or 'audience' in campgaign_types:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            return bulk_str(shopping_setting.Priority)

    @staticmethod
    def _read_priority(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'shopping' in campgaign_types or 'audience' in campgaign_types:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            shopping_setting.Priority = int(v) if v else None

    @staticmethod
    def _write_sales_country_code(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'shopping' in campgaign_types or 'audience' in campgaign_types:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            return shopping_setting.SalesCountryCode

    @staticmethod
    def _read_sales_country_code(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'shopping' in campgaign_types or 'audience' in campgaign_types:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            shopping_setting.SalesCountryCode = v

    @staticmethod
    def _write_local_inventory_ads_enabled(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'shopping' in campgaign_types or 'audience' in campgaign_types:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            return shopping_setting.LocalInventoryAdsEnabled

    @staticmethod
    def _read_local_inventory_ads_enabled(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'shopping' in campgaign_types or 'audience' in campgaign_types:
            shopping_setting = c._get_shopping_setting()
            if not shopping_setting:
                return None
            shopping_setting.LocalInventoryAdsEnabled = v.lower() == 'true' if v else None

    @staticmethod
    def _write_feed_id(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'audience' in campgaign_types:
            dynamic_feed_setting = c._get_dynamic_feed_setting()
            if not dynamic_feed_setting:
                return None
            return bulk_str(dynamic_feed_setting.FeedId)

    @staticmethod
    def _read_feed_id(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'audience' in campgaign_types:
            dynamic_feed_setting = c._get_dynamic_feed_setting()
            if not dynamic_feed_setting:
                return None
            dynamic_feed_setting.FeedId = int(v) if v else None

    @staticmethod
    def _read_source(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        dsa_setting = c._get_dsa_setting()
        if not dsa_setting:
            return None
        dsa_setting.Source = v

    @staticmethod
    def _write_source(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        dsa_setting = c._get_dsa_setting()
        if not dsa_setting:
            return None
        return bulk_str(dsa_setting.Source)

    @staticmethod
    def _read_domain_language(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        dsa_setting = c._get_dsa_setting()
        if not dsa_setting:
            return None
        dsa_setting.Language = v

    @staticmethod
    def _write_domain_language(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        dsa_setting = c._get_dsa_setting()
        if not dsa_setting:
            return None
        return bulk_str(dsa_setting.Language)

    @staticmethod
    def _read_DisclaimerAdsEnabled(c, v):
        if not c.campaign.CampaignType:
            return None
        disclaimer_setting = c._get_disclaimer_setting()
        if not disclaimer_setting:
            return None
        disclaimer_setting.DisclaimerAdsEnabled = parse_bool(v)

    @staticmethod
    def _write_DisclaimerAdsEnabled(c):
        if not c.campaign.CampaignType:
            return None
        disclaimer_setting = c._get_disclaimer_setting()
        if not disclaimer_setting:
            return None
        return bulk_str(disclaimer_setting.DisclaimerAdsEnabled)

    @staticmethod
    def _read_DynamicDescriptionEnabled(c, v):
        if not c.campaign.CampaignType:
            return None
        dsa_setting = c._get_dsa_setting()
        if not dsa_setting:
            return None
        dsa_setting.DynamicDescriptionEnabled = parse_bool(v)

    @staticmethod
    def _write_DynamicDescriptionEnabled(c):
        if not c.campaign.CampaignType:
            return None
        dsa_setting = c._get_dsa_setting()
        if not dsa_setting:
            return None
        return bulk_str(dsa_setting.DynamicDescriptionEnabled)

    @staticmethod
    def _read_page_feed_ids(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            performance_max_setting.PageFeedIds.long = csv_to_field_PageFeedIds(v)
        else:
            dsa_setting = c._get_dsa_setting()
            if not dsa_setting:
                return None
            dsa_setting.PageFeedIds.long = csv_to_field_PageFeedIds(v)

    @staticmethod
    def _write_page_feed_ids(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            return field_to_csv_Ids(performance_max_setting.PageFeedIds, c.campaign.Id)
        else:
            dsa_setting = c._get_dsa_setting()
            if not dsa_setting:
                return None
            return field_to_csv_Ids(dsa_setting.PageFeedIds, c.campaign.Id)

    @staticmethod
    def _read_text_opt_out(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            performance_max_setting.AutoGeneratedTextOptOut = parse_bool(v)

    @staticmethod
    def _write_text_opt_out(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            return bulk_str(performance_max_setting.AutoGeneratedTextOptOut)

    @staticmethod
    def _read_cost_per_sale_opt_out(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            performance_max_setting.CostPerSaleOptOut = parse_bool(v)

    @staticmethod
    def _write_cost_per_sale_opt_out(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            return bulk_str(performance_max_setting.CostPerSaleOptOut)

    @staticmethod
    def _read_image_opt_out(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            performance_max_setting.AutoGeneratedImageOptOut = parse_bool(v)

    @staticmethod
    def _write_image_opt_out(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            performance_max_setting = c._get_performance_max_setting()
            if not performance_max_setting:
                return None
            return bulk_str(performance_max_setting.AutoGeneratedImageOptOut)

    @staticmethod
    def _read_new_customer_acquisition_bid_only_mode(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            new_customer_acquisition_goal_setting = c._get_new_customer_acquisition_goal_setting()
            if not new_customer_acquisition_goal_setting:
                return None
            new_customer_acquisition_goal_setting.NewCustomerAcquisitionBidOnlyMode = parse_bool(v)

    @staticmethod
    def _write_new_customer_acquisition_bid_only_mode(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            new_customer_acquisition_goal_setting = c._get_new_customer_acquisition_goal_setting()
            if not new_customer_acquisition_goal_setting:
                return None
            return bulk_str(new_customer_acquisition_goal_setting.NewCustomerAcquisitionBidOnlyMode)

    @staticmethod
    def _read_new_customer_acquisition_goal_id(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            new_customer_acquisition_goal_setting = c._get_new_customer_acquisition_goal_setting()
            if not new_customer_acquisition_goal_setting:
                return None
            new_customer_acquisition_goal_setting.NewCustomerAcquisitionGoalId = int(v) if v else None

    @staticmethod
    def _write_new_customer_acquisition_goal_id(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            new_customer_acquisition_goal_setting = c._get_new_customer_acquisition_goal_setting()
            if not new_customer_acquisition_goal_setting:
                return None
            return bulk_str(new_customer_acquisition_goal_setting.NewCustomerAcquisitionGoalId)

    @staticmethod
    def _read_additional_conversion_value(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            new_customer_acquisition_goal_setting = c._get_new_customer_acquisition_goal_setting()
            if not new_customer_acquisition_goal_setting:
                return None
            new_customer_acquisition_goal_setting.AdditionalConversionValue = Decimal(v) if v else None

    @staticmethod
    def _write_additional_conversion_value(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        if 'performancemax' in campgaign_types:
            new_customer_acquisition_goal_setting = c._get_new_customer_acquisition_goal_setting()
            if not new_customer_acquisition_goal_setting:
                return None
            return bulk_str(new_customer_acquisition_goal_setting.AdditionalConversionValue)

    @staticmethod
    def _read_website(c, v):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        dsa_setting = c._get_dsa_setting()
        if not dsa_setting:
            return None
        dsa_setting.DomainName = v

    @staticmethod
    def _write_website(c):
        if not c.campaign.CampaignType:
            return None
        campgaign_types = [campaign_type.lower() for campaign_type in c.campaign.CampaignType]
        dsa_setting = c._get_dsa_setting()
        if not dsa_setting:
            return None
        return bulk_str(dsa_setting.DomainName)

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.CampaignType,
            field_to_csv=lambda c: BulkCampaign._write_campaign_type(c),
            csv_to_field=lambda c, v: BulkCampaign._read_campaign_type(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.campaign.Status),
            csv_to_field=lambda c, v: csv_to_field_enum(c.campaign, v, 'Status', CampaignStatus)
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
            csv_to_field=lambda c, v: setattr(c, '_account_id', int(v) if v else None)
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
        _SimpleBulkMapping(
            header=_StringTable.Language,
            field_to_csv=lambda c: field_to_csv_CampaignLanguages(c.campaign.Languages),
            csv_to_field=lambda c, v: csv_to_field_CampaignLanguages(c.campaign.Languages, v)
        ),
        _ComplexBulkMapping(budget_to_csv, csv_to_budget),
        _SimpleBulkMapping(
            header=_StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.campaign.AudienceAdsBidAdjustment),
            csv_to_field=lambda c, v: setattr(
                c.campaign,
                'AudienceAdsBidAdjustment',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlExpansionOptOut,
            field_to_csv=lambda c: BulkCampaign._write_final_url_expansion_opt_out(c),
            csv_to_field=lambda c, v: BulkCampaign._read_final_url_expansion_opt_out(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MerchantCenterId,
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
            header=_StringTable.LocalInventoryAdsEnabled,
            field_to_csv=lambda c: BulkCampaign._write_local_inventory_ads_enabled(c),
            csv_to_field=lambda c, v: BulkCampaign._read_local_inventory_ads_enabled(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_optional_str(c.campaign.TrackingUrlTemplate, c.campaign.Id),
            csv_to_field=lambda c, v: setattr(c.campaign, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.campaign),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.campaign, v)
        ),
        _ComplexBulkMapping(campaign_biddingscheme_to_csv, csv_to_campaign_biddingscheme),
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
            header=_StringTable.BidStrategyName,
            field_to_csv=lambda c: bulk_str(c.bid_strategy_name),
            csv_to_field=lambda c, v: setattr(c, 'bid_strategy_name', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidStrategyId,
            field_to_csv=lambda c: bulk_str(c.campaign.BidStrategyId),
            csv_to_field=lambda c, v: setattr(c.campaign, 'BidStrategyId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Website,
            field_to_csv=lambda c: BulkCampaign._write_website(c),
            csv_to_field=lambda c, v: BulkCampaign._read_website(c, v)

        ),
        _SimpleBulkMapping(
            header=_StringTable.DomainLanguage,
            field_to_csv=lambda c: BulkCampaign._write_domain_language(c),
            csv_to_field=lambda c, v: BulkCampaign._read_domain_language(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Source,
            field_to_csv=lambda c: BulkCampaign._write_source(c),
            csv_to_field=lambda c, v: BulkCampaign._read_source(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SubType,
            field_to_csv=lambda c: c.campaign.SubType,
            csv_to_field=lambda c, v: setattr(c.campaign, 'SubType', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ExperimentId,
            field_to_csv=lambda c: bulk_str(c.campaign.ExperimentId),
            csv_to_field=lambda c, v: setattr(c.campaign, 'ExperimentId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FeedId,
            field_to_csv=lambda c: BulkCampaign._write_feed_id(c),
            csv_to_field=lambda c, v: BulkCampaign._read_feed_id(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TargetSetting,
            field_to_csv=lambda c: target_setting_to_csv(c.campaign),
            csv_to_field=lambda c, v: csv_to_target_setting(c.campaign, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.campaign.FinalUrlSuffix, c.campaign.Id),
            csv_to_field=lambda c, v: setattr(c.campaign, 'FinalUrlSuffix', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.PageFeedIds,
            field_to_csv=lambda c: BulkCampaign._write_page_feed_ids(c),
            csv_to_field=lambda c, v: BulkCampaign._read_page_feed_ids(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdScheduleUseSearcherTimeZone,
            field_to_csv=lambda c: field_to_csv_UseSearcherTimeZone(c.campaign.AdScheduleUseSearcherTimeZone, None),
            csv_to_field=lambda c, v: setattr(c.campaign, 'AdScheduleUseSearcherTimeZone', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.MultiMediaAdBidAdjustment,
            field_to_csv=lambda c: bulk_str(c.campaign.MultimediaAdsBidAdjustment),
            csv_to_field=lambda c, v: setattr(
                c.campaign,
                'MultimediaAdsBidAdjustment',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.DisclaimerAdsEnabled,
            field_to_csv=lambda c: BulkCampaign._write_DisclaimerAdsEnabled(c),
            csv_to_field=lambda c, v: BulkCampaign._read_DisclaimerAdsEnabled(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DynamicDescriptionEnabled,
            field_to_csv=lambda c: BulkCampaign._write_DynamicDescriptionEnabled(c),
            csv_to_field=lambda c, v: BulkCampaign._read_DynamicDescriptionEnabled(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DestinationChannel,
            field_to_csv=lambda c: c.destination_channel,
            csv_to_field=lambda c, v: setattr(c, 'destination_channel', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.IsMultiChannelCampaign,
            field_to_csv=lambda c: field_to_csv_bool(c.is_multi_channel_campaign),
            csv_to_field=lambda c, v: setattr(c, 'is_multi_channel_campaign', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.AutoGeneratedTextOptOut,
            field_to_csv=lambda c: BulkCampaign._write_text_opt_out(c),
            csv_to_field=lambda c, v: BulkCampaign._read_text_opt_out(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AutoGeneratedImageOptOut,
            field_to_csv=lambda c: BulkCampaign._write_image_opt_out(c),
            csv_to_field=lambda c, v: BulkCampaign._read_image_opt_out(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CostPerSaleOptOut,
            field_to_csv=lambda c: BulkCampaign._write_cost_per_sale_opt_out(c),
            csv_to_field=lambda c, v: BulkCampaign._read_cost_per_sale_opt_out(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ShouldServeOnMSAN,
            field_to_csv=lambda c: field_to_csv_bool(c.should_serve_on_msan),
            csv_to_field=lambda c, v: setattr(c, 'should_serve_on_msan', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.NewCustomerAcquisitionGoalId,
            field_to_csv=lambda c: BulkCampaign._write_new_customer_acquisition_goal_id(c),
            csv_to_field=lambda c, v: BulkCampaign._read_new_customer_acquisition_goal_id(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.NewCustomerAcquisitionBidOnlyMode,
            field_to_csv=lambda c: BulkCampaign._write_new_customer_acquisition_bid_only_mode(c),
            csv_to_field=lambda c, v: BulkCampaign._read_new_customer_acquisition_bid_only_mode(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdditionalConversionValue,
            field_to_csv=lambda c: BulkCampaign._write_additional_conversion_value(c),
            csv_to_field=lambda c, v: BulkCampaign._read_additional_conversion_value(c, v)
        ),
    ]

    def read_additional_data(self, stream_reader):
        super(BulkCampaign, self).read_additional_data(stream_reader)

    def process_mappings_from_row_values(self, row_values):
        self._campaign = _CAMPAIGN_OBJECT_FACTORY_V13.create('Campaign')
        row_values.convert_to_entity(self, BulkCampaign._MAPPINGS)
        self._quality_score_data = QualityScoreData.read_from_row_values_or_null(row_values)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.campaign, 'campaign')
        self.convert_to_values(row_values, BulkCampaign._MAPPINGS)
        if not exclude_readonly_data:
            QualityScoreData.write_to_row_values_if_not_null(self.quality_score_data, row_values)
