from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

from bingads.v13.internal.extensions import *

_PriceAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('PriceAdExtension'))


class BulkPriceAdExtension(_BulkAdExtensionBase):
    """ Represents a Price Ad Extension.

    This class exposes the :attr:`price_ad_extension` property that can be read and written
    as fields of the Price Ad Extension record in a bulk file.

    For more information, see Price Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _PriceAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'PriceAdExtension'
            ))
        super(BulkPriceAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def price_ad_extension(self):
        """ The Price Ad Extension.

        see Price Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @price_ad_extension.setter
    def price_ad_extension(self, value):
        self._ad_extension = value


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Language,
            field_to_csv=lambda c: c.price_ad_extension.Language,
            csv_to_field=lambda c, v: setattr(c.price_ad_extension, 'Language', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.PriceExtensionType,
            field_to_csv=lambda c: c.price_ad_extension.PriceExtensionType,
            csv_to_field=lambda c, v: setattr(c.price_ad_extension, 'PriceExtensionType', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.price_ad_extension.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.price_ad_extension, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.price_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.price_ad_extension, v)
        ),
        _ComplexBulkMapping(
            entity_to_csv=lambda c, v: entity_to_csv_PriceTableRows(c.price_ad_extension, v),
            csv_to_entity=lambda v, c: csv_to_entity_PriceTableRows(v, c.price_ad_extension)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.price_ad_extension.FinalUrlSuffix, c.price_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.price_ad_extension, 'FinalUrlSuffix', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.price_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('PriceAdExtension')
        self.price_ad_extension.Type = 'PriceAdExtension'
        super(BulkPriceAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkPriceAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.price_ad_extension, 'price_ad_extension')
        super(BulkPriceAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkPriceAdExtension._MAPPINGS)


class BulkAccountPriceAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level Price Ad Extension.

    This class exposes properties that can be read and written
    as fields of the Account Price Ad Extension record in a bulk file.

    For more information, see Account Price Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkCampaignPriceAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level Price Ad Extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Price Ad Extension record in a bulk file.

    For more information, see Campaign Price Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupPriceAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level Price ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Price Ad Extension record in a bulk file.

    For more information, see Ad Group Price Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
