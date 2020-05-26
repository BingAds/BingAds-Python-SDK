from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

from bingads.v13.internal.extensions import *


_PromotionAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('PromotionAdExtension'))


class BulkPromotionAdExtension(_BulkAdExtensionBase):
    """ Represents a promotion ad extension.

    This class exposes the :attr:`promotion_ad_extension` property that can be read and written
    as fields of the Promotion Ad Extension record in a bulk file.

    For more information, see Promotion Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _PromotionAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'PromotionAdExtension'
            ))
        super(BulkPromotionAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )
        

    @property
    def promotion_ad_extension(self):
        """ The promotion ad extension.

        see Promotion Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @promotion_ad_extension.setter
    def promotion_ad_extension(self, value):
        self._ad_extension = value
        

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Language,
            field_to_csv=lambda c: bulk_str(c.promotion_ad_extension.Language),
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'Language', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CurrencyCode,
            field_to_csv=lambda c: bulk_str(c.promotion_ad_extension.CurrencyCode),
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'CurrencyCode', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.PromotionCode,
            field_to_csv=lambda c: bulk_optional_str(c.promotion_ad_extension.PromotionCode, c.promotion_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'PromotionCode', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.PromotionTarget,
            field_to_csv=lambda c: bulk_str(c.promotion_ad_extension.PromotionItem),
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'PromotionItem', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.PromotionStart,
            field_to_csv=lambda c: field_to_csv_SchedulingDate(c.promotion_ad_extension.PromotionStartDate, c.promotion_ad_extension.Id) if c._ad_extension.Scheduling else None,
            csv_to_field=lambda c, v: csv_to_field_Date(c.promotion_ad_extension, 'PromotionStartDate', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.PromotionEnd,
            field_to_csv=lambda c: field_to_csv_SchedulingDate(c.promotion_ad_extension.PromotionEndDate, c.promotion_ad_extension.Id) if c._ad_extension.Scheduling else None,
            csv_to_field = lambda c, v: csv_to_field_Date(c.promotion_ad_extension, 'PromotionEndDate', v)
        ),        
        _SimpleBulkMapping(
            header=_StringTable.MoneyAmountOff,
            field_to_csv=lambda c: c.promotion_ad_extension.MoneyAmountOff,
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'MoneyAmountOff',float(v) if v else None)
        ),        
        _SimpleBulkMapping(
            header=_StringTable.OrdersOverAmount,
            field_to_csv=lambda c: c.promotion_ad_extension.OrdersOverAmount,
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'OrdersOverAmount',float(v) if v else None)
        ),        
        _SimpleBulkMapping(
            header=_StringTable.PercentOff,
            field_to_csv=lambda c: c.promotion_ad_extension.PercentOff,
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'PercentOff',float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DiscountModifier,
            field_to_csv=lambda c: bulk_str(c.promotion_ad_extension.DiscountModifier),
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'DiscountModifier', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Occasion,
            field_to_csv=lambda c: bulk_str(c.promotion_ad_extension.PromotionOccasion),
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'PromotionOccasion', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.promotion_ad_extension.FinalUrls, c.promotion_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.promotion_ad_extension.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.promotion_ad_extension.FinalMobileUrls, c.promotion_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.promotion_ad_extension.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_optional_str(c.promotion_ad_extension.TrackingUrlTemplate, c.promotion_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'TrackingUrlTemplate', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.promotion_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.promotion_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.promotion_ad_extension.FinalUrlSuffix, c.promotion_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.promotion_ad_extension, 'FinalUrlSuffix', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.promotion_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('PromotionAdExtension')
        self.promotion_ad_extension.Type = 'PromotionAdExtension'
        super(BulkPromotionAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkPromotionAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.promotion_ad_extension, 'promotion_ad_extension')
        super(BulkPromotionAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkPromotionAdExtension._MAPPINGS)


class BulkAccountPromotionAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level promotion ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Promotion Ad Extension record in a bulk file.

    For more information, see Account Promotion Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkCampaignPromotionAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level promotion ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Promotion Ad Extension record in a bulk file.

    For more information, see Campaign Promotion Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupPromotionAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level Promotion ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Promotion Ad Extension record in a bulk file.

    For more information, see Ad Group Promotion Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
