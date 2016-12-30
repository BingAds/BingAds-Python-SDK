from bingads.v10.bulk.entities import PerformanceData
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V10
from bingads.v10.internal.bulk.string_table import _StringTable
from bingads.v10.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v10.internal.bulk.mappings import _SimpleBulkMapping
from bingads.internal.extensions import *

# Define type used
ProductAd = type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ProductAd'))
TextAd = type(_CAMPAIGN_OBJECT_FACTORY_V10.create('TextAd'))
AppInstallAd = type(_CAMPAIGN_OBJECT_FACTORY_V10.create('AppInstallAd'))
ExpandedTextAd = type(_CAMPAIGN_OBJECT_FACTORY_V10.create('ExpandedTextAd'))
DynamicSearchAd = type(_CAMPAIGN_OBJECT_FACTORY_V10.create('DynamicSearchAd'))


class _BulkAd(_SingleRecordBulkEntity):
    """ This abstract base class provides properties that are shared by all bulk ad classes.

    *See also:*

    * :class:`.BulkProductAd`
    * :class:`.BulkTextAd`
    * :class:`.BulkAppInstallAd`
    * :class:`.BulkExpandedTextAd`
    * :class:`.BulkDynamicSearchAd`
    """

    def __init__(self,
                 ad_group_id=None,
                 campaign_name=None,
                 ad_group_name=None,
                 ad=None):
        super(_BulkAd, self).__init__()

        self._ad_group_id = ad_group_id
        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name
        self._ad = ad
        self._performance_data = None

    @property
    def ad_group_id(self):
        """ The identifier of the ad group that contains the ad.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._ad_group_id

    @ad_group_id.setter
    def ad_group_id(self, ad_group_id):
        self._ad_group_id = ad_group_id

    @property
    def campaign_name(self):
        """ The name of the campaign that contains the ad.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @property
    def ad_group_name(self):
        """ The name of the ad group that contains the ad.

        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """

        return self._ad_group_name

    @ad_group_name.setter
    def ad_group_name(self, ad_group_name):
        self._ad_group_name = ad_group_name

    @property
    def ad(self):
        """ The type of ad.

        """

        return self._ad

    @ad.setter
    def ad(self, ad):
        self._ad = ad

    @property
    def performance_data(self):
        """ The historical performance data for the ad.

        :rtype: PerformanceData
        """

        return self._performance_data

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.ad.Status),
            csv_to_field=lambda c, v: setattr(c.ad, 'Status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.ad.Id),
            csv_to_field=lambda c, v: setattr(c.ad, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.ad_group_id),
            csv_to_field=lambda c, v: setattr(c, '_ad_group_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, '_campaign_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdGroup,
            field_to_csv=lambda c: c.ad_group_name,
            csv_to_field=lambda c, v: setattr(c, '_ad_group_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialStatus,
            field_to_csv=lambda c: c.ad.EditorialStatus,
            csv_to_field=lambda c, v: setattr(c.ad, 'EditorialStatus', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DevicePreference,
            field_to_csv=lambda c: bulk_device_preference_str(c.ad.DevicePreference),
            csv_to_field=lambda c, v: setattr(c.ad, 'DevicePreference', parse_device_preference(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.ad.FinalUrls),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.ad.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.ad.FinalMobileUrls),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.ad.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.ad.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.ad, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.ad),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.ad, v)
        ),
        # TODO FinalAppUrls is not added
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, _BulkAd._MAPPINGS)
        if not exclude_readonly_data:
            PerformanceData.write_to_row_values_if_not_null(self.performance_data, row_values)

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, _BulkAd._MAPPINGS)
        self._performance_data = PerformanceData.read_from_row_values_or_null(row_values)

    def read_additional_data(self, stream_reader):
        super(_BulkAd, self).read_additional_data(stream_reader)


class BulkProductAd(_BulkAd):
    """ Represents a product ad.

    This class exposes the :attr:`product_ad` property that can be read and written as fields of the Product Ad record in a bulk file.

    For more information, see Product Ad at http://go.microsoft.com/fwlink/?LinkID=620264.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 ad_group_id=None,
                 campaign_name=None,
                 ad_group_name=None,
                 ad=None):
        super(BulkProductAd, self).__init__(
            ad_group_id,
            campaign_name,
            ad_group_name,
            ad
        )
        self.product_ad = ad

    @property
    def product_ad(self):
        """ The product ad.

        See Product Ad at: http://go.microsoft.com/fwlink/?LinkID=620264.
        """

        return self._ad

    @product_ad.setter
    def product_ad(self, product_ad):
        if product_ad is not None and not isinstance(product_ad, ProductAd):
            raise ValueError('Not an instance of ProductAd')
        self._ad = product_ad

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.PromotionalText,
            field_to_csv=lambda c: bulk_optional_str(c.product_ad.PromotionalText),
            csv_to_field=lambda c, v: setattr(c.product_ad, 'PromotionalText', v if v else '')
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.product_ad = _CAMPAIGN_OBJECT_FACTORY_V10.create('ProductAd')
        self.product_ad.Type = 'Product'
        super(BulkProductAd, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkProductAd._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.product_ad, 'product_ad')
        super(BulkProductAd, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkProductAd._MAPPINGS)


class BulkTextAd(_BulkAd):
    """ Represents a Text Ad.

    This class exposes the :attr:`text_ad` property that can be read and written as fields of the Text Ad record in a bulk file.

    For more information, see Text Ad at http://go.microsoft.com/fwlink/?LinkID=620263.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 ad_group_id=None,
                 campaign_name=None,
                 ad_group_name=None,
                 ad=None):
        super(BulkTextAd, self).__init__(
            ad_group_id,
            campaign_name,
            ad_group_name,
            ad,
        )
        self.text_ad = ad

    @property
    def text_ad(self):
        """ The text ad.

        see Text Ad at http://go.microsoft.com/fwlink/?LinkID=620263.
        """

        return self._ad

    @text_ad.setter
    def text_ad(self, text_ad):
        if text_ad is not None and not isinstance(text_ad, TextAd):
            raise ValueError('Not an instance of TextAd')
        self._ad = text_ad

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Title,
            field_to_csv=lambda c: c.text_ad.Title,
            csv_to_field=lambda c, v: setattr(c.text_ad, 'Title', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Text,
            field_to_csv=lambda c: c.text_ad.Text,
            csv_to_field=lambda c, v: setattr(c.text_ad, 'Text', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DisplayUrl,
            field_to_csv=lambda c: bulk_optional_str(c.text_ad.DisplayUrl),
            csv_to_field=lambda c, v: setattr(c.text_ad, 'DisplayUrl', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.DestinationUrl,
            field_to_csv=lambda c: bulk_optional_str(c.text_ad.DestinationUrl),
            csv_to_field=lambda c, v: setattr(c.text_ad, 'DestinationUrl', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdFormatPreference,
            field_to_csv=lambda c: field_to_csv_AdFormatPreference(c.text_ad),
            csv_to_field=lambda c, v: csv_to_field_AdFormatPreference(c.text_ad, v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.text_ad = _CAMPAIGN_OBJECT_FACTORY_V10.create('TextAd')
        self.text_ad.Type = 'Text'
        super(BulkTextAd, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkTextAd._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.text_ad, 'text_ad')
        super(BulkTextAd, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkTextAd._MAPPINGS)


class BulkAppInstallAd(_BulkAd):
    """ Represents an App Install Ad.

    This class exposes the :attr:`app_install_ad` property that can be read and written as fields of the App Install Ad record in a bulk file.

    For more information, see App Install Ad at http://go.microsoft.com/fwlink/?LinkID=730549.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 ad_group_id=None,
                 campaign_name=None,
                 ad_group_name=None,
                 ad=None):
        super(BulkAppInstallAd, self).__init__(
            ad_group_id,
            campaign_name,
            ad_group_name,
            ad,
        )
        self.app_install_ad = ad

    @property
    def app_install_ad(self):
        """ The App Install Ad.

        see App Install Ad at http://go.microsoft.com/fwlink/?LinkID=730549.
        """

        return self._ad

    @app_install_ad.setter
    def app_install_ad(self, app_install_ad):
        if app_install_ad is not None and not isinstance(app_install_ad, AppInstallAd):
            raise ValueError('Not an instance of AppInstallAd')
        self._ad = app_install_ad

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.AppPlatform,
            field_to_csv=lambda c: c.app_install_ad.AppPlatform,
            csv_to_field=lambda c, v: setattr(c.app_install_ad, 'AppPlatform', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AppStoreId,
            field_to_csv=lambda c: c.app_install_ad.AppStoreId,
            csv_to_field=lambda c, v: setattr(c.app_install_ad, 'AppStoreId', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Title,
            field_to_csv=lambda c: c.app_install_ad.Title,
            csv_to_field=lambda c, v: setattr(c.app_install_ad, 'Title', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Text,
            field_to_csv=lambda c: c.app_install_ad.Text,
            csv_to_field=lambda c, v: setattr(c.app_install_ad, 'Text', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.app_install_ad = _CAMPAIGN_OBJECT_FACTORY_V10.create('AppInstallAd')
        self.app_install_ad.Type = 'AppInstall'
        super(BulkAppInstallAd, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAppInstallAd._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.app_install_ad, 'app_install_ad')
        super(BulkAppInstallAd, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAppInstallAd._MAPPINGS)


class BulkExpandedTextAd(_BulkAd):
    """ Represents an Expanded Text Ad.

    This class exposes the :attr:`expanded_text_ad` property that can be read and written as fields of the Expanded Text Ad record in a bulk file.

    For more information, see Expanded Text Ad at http://go.microsoft.com/fwlink/?LinkID=823170.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 ad_group_id=None,
                 campaign_name=None,
                 ad_group_name=None,
                 ad=None):
        super(BulkExpandedTextAd, self).__init__(
            ad_group_id,
            campaign_name,
            ad_group_name,
            ad,
        )
        self.expanded_text_ad = ad

    @property
    def expanded_text_ad(self):
        """ The Expanded Text Ad.

        see Expanded Text Ad at http://go.microsoft.com/fwlink/?LinkID=823170.
        """

        return self._ad

    @expanded_text_ad.setter
    def expanded_text_ad(self, expanded_text_ad):
        if expanded_text_ad is not None and not isinstance(expanded_text_ad, ExpandedTextAd):
            raise ValueError('Not an instance of ExpandedTextAd')
        self._ad = expanded_text_ad

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Text,
            field_to_csv=lambda c: c.expanded_text_ad.Text,
            csv_to_field=lambda c, v: setattr(c.expanded_text_ad, 'Text', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TitlePart1,
            field_to_csv=lambda c: c.expanded_text_ad.TitlePart1,
            csv_to_field=lambda c, v: setattr(c.expanded_text_ad, 'TitlePart1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TitlePart2,
            field_to_csv=lambda c: c.expanded_text_ad.TitlePart2,
            csv_to_field=lambda c, v: setattr(c.expanded_text_ad, 'TitlePart2', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Path1,
            field_to_csv=lambda c: c.expanded_text_ad.Path1,
            csv_to_field=lambda c, v: setattr(c.expanded_text_ad, 'Path1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Path2,
            field_to_csv=lambda c: c.expanded_text_ad.Path2,
            csv_to_field=lambda c, v: setattr(c.expanded_text_ad, 'Path2', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.expanded_text_ad = _CAMPAIGN_OBJECT_FACTORY_V10.create('ExpandedTextAd')
        self.expanded_text_ad.Type = 'ExpandedText'
        super(BulkExpandedTextAd, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkExpandedTextAd._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.expanded_text_ad, 'expanded_text_ad')
        super(BulkExpandedTextAd, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkExpandedTextAd._MAPPINGS)


class BulkDynamicSearchAd(_BulkAd):
    """ Represents a Dynamic Search Ad.

    This class exposes the :attr:`dynamic_search_ad` property that can be read and written as fields of the Dynamic Search Ad record in a bulk file.

    For more information, see Dynamic Search Ad at https://go.microsoft.com/fwlink/?linkid=836840.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 ad_group_id=None,
                 campaign_name=None,
                 ad_group_name=None,
                 ad=None):
        super(BulkDynamicSearchAd, self).__init__(
            ad_group_id,
            campaign_name,
            ad_group_name,
            ad,
        )
        self.dynamic_search_ad = ad

    @property
    def dynamic_search_ad(self):
        """ The dynamic search ad.

        see Dynamic Search Ad at https://go.microsoft.com/fwlink/?linkid=836840.
        """

        return self._ad

    @dynamic_search_ad.setter
    def dynamic_search_ad(self, dynamic_search_ad):
        if dynamic_search_ad is not None and not isinstance(dynamic_search_ad, DynamicSearchAd):
            raise ValueError('Not an instance of DynamicSearchAd')
        self._ad = dynamic_search_ad

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Text,
            field_to_csv=lambda c: c.dynamic_search_ad.Text,
            csv_to_field=lambda c, v: setattr(c.dynamic_search_ad, 'Text', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Path1,
            field_to_csv=lambda c: c.dynamic_search_ad.Path1,
            csv_to_field=lambda c, v: setattr(c.dynamic_search_ad, 'Path1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Path2,
            field_to_csv=lambda c: c.dynamic_search_ad.Path2,
            csv_to_field=lambda c, v: setattr(c.dynamic_search_ad, 'Path2', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.dynamic_search_ad = _CAMPAIGN_OBJECT_FACTORY_V10.create('DynamicSearchAd')
        self.dynamic_search_ad.Type = 'DynamicSearch'
        super(BulkDynamicSearchAd, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkDynamicSearchAd._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.dynamic_search_ad, 'dynamic_search_ad')
        super(BulkDynamicSearchAd, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkDynamicSearchAd._MAPPINGS)
