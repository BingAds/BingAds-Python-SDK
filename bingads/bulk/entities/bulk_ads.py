from bingads.bulk.entities import PerformanceData
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY
from bingads.internal.bulk.string_table import _StringTable
from bingads.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.internal.bulk.mappings import _SimpleBulkMapping
from bingads.internal.extensions import *

# Define type used
MobileAd = type(_CAMPAIGN_OBJECT_FACTORY.create('MobileAd'))
ProductAd = type(_CAMPAIGN_OBJECT_FACTORY.create('ProductAd'))
TextAd = type(_CAMPAIGN_OBJECT_FACTORY.create('TextAd'))


class _BulkAd(_SingleRecordBulkEntity):
    """ This abstract base class provides properties that are shared by all bulk ad classes.

    *See also:*

    * :class:`.BulkMobileAd`
    * :class:`.BulkProductAd`
    * :class:`.BulkTextAd`
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


class BulkMobileAd(_BulkAd):
    """ Represents a mobile ad.

    This class exposes the :attr:`mobile_ad` property that can be read and written as fields of the Mobile Ad record in a bulk file.

    For more information, see Mobile Ad at http://go.microsoft.com/fwlink/?LinkID=511553.

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
        super(BulkMobileAd, self).__init__(
            ad_group_id,
            campaign_name,
            ad_group_name,
            ad
        )
        self.mobile_ad = ad

    @property
    def mobile_ad(self):
        """ The mobile ad.

        See Mobile Ad at: https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-mobilead.aspx
        """

        return self._ad

    @mobile_ad.setter
    def mobile_ad(self, mobile_ad):
        if mobile_ad is not None and not isinstance(mobile_ad, MobileAd):
            raise ValueError('Not an instance of MobileAd')
        self._ad = mobile_ad

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Title,
            field_to_csv=lambda c: c.mobile_ad.Title,
            csv_to_field=lambda c, v: setattr(c.mobile_ad, 'Title', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Text,
            field_to_csv=lambda c: c.mobile_ad.Text,
            csv_to_field=lambda c, v: setattr(c.mobile_ad, 'Text', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DisplayUrl,
            field_to_csv=lambda c: bulk_optional_str(c.mobile_ad.DisplayUrl),
            csv_to_field=lambda c, v: setattr(c.mobile_ad, 'DisplayUrl', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.DestinationUrl,
            field_to_csv=lambda c: bulk_optional_str(c.mobile_ad.DestinationUrl),
            csv_to_field=lambda c, v: setattr(c.mobile_ad, 'DestinationUrl', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.BusinessName,
            field_to_csv=lambda c: bulk_optional_str(c.mobile_ad.BusinessName),
            csv_to_field=lambda c, v: setattr(c.mobile_ad, 'BusinessName', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.PhoneNumber,
            field_to_csv=lambda c: bulk_optional_str(c.mobile_ad.PhoneNumber),
            csv_to_field=lambda c, v: setattr(c.mobile_ad, 'PhoneNumber', v if v else '')
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.mobile_ad = _CAMPAIGN_OBJECT_FACTORY.create('MobileAd')
        self.mobile_ad.Type = 'Mobile'
        super(BulkMobileAd, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkMobileAd._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.mobile_ad, 'mobile_ad')
        super(BulkMobileAd, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkMobileAd._MAPPINGS)


class BulkProductAd(_BulkAd):
    """ Represents a product ad.

    This class exposes the :attr:`product_ad` property that can be read and written as fields of the Product Ad record in a bulk file.

    For more information, see Product Ad at http://go.microsoft.com/fwlink/?LinkID=511555.

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

        See Product Ad at: http://go.microsoft.com/fwlink/?LinkID=511555.
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
        self.product_ad = _CAMPAIGN_OBJECT_FACTORY.create('ProductAd')
        self.product_ad.Type = 'Product'
        super(BulkProductAd, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkProductAd._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.product_ad, 'product_ad')
        super(BulkProductAd, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkProductAd._MAPPINGS)


class BulkTextAd(_BulkAd):
    """ Represents a product ad.

    This class exposes the :attr:`text_ad` property that can be read and written as fields of the Text Ad record in a bulk file.

    For more information, see Text Ad at http://go.microsoft.com/fwlink/?LinkID=511554.

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

        see Text Ad at http://go.microsoft.com/fwlink/?LinkID=511554.
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
    ]

    def process_mappings_from_row_values(self, row_values):
        self.text_ad = _CAMPAIGN_OBJECT_FACTORY.create('TextAd')
        self.text_ad.Type = 'Text'
        super(BulkTextAd, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkTextAd._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.text_ad, 'text_ad')
        super(BulkTextAd, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkTextAd._MAPPINGS)
