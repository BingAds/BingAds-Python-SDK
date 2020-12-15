from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.extensions import *
from .common import _BulkAdExtensionBase
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

_FlyerAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('FlyerAdExtension'))


class BulkFlyerAdExtension(_BulkAdExtensionBase):
    """ Represents a flyer ad extension.

    This class exposes the :attr:`flyer_ad_extension` property that can be read and written
    as fields of the Flyer Ad Extension record in a bulk file.

    For more information, see Flyer Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _FlyerAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'FlyerAdExtension'
            ))
        super(BulkFlyerAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def flyer_ad_extension(self):
        """ The flyer ad extension.

        see Flyer Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @flyer_ad_extension.setter
    def flyer_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.FlyerName,
            field_to_csv=lambda c: bulk_str(c.flyer_ad_extension.FlyerName),
            csv_to_field=lambda c, v: setattr(c.flyer_ad_extension, 'FlyerName', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MerchantCenterId,
            field_to_csv=lambda c: bulk_str(c.flyer_ad_extension.StoreId),
            csv_to_field=lambda c, v: setattr(c.flyer_ad_extension, 'StoreId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Description,
            field_to_csv=lambda c: bulk_str(c.flyer_ad_extension.Description),
            csv_to_field=lambda c, v: setattr(c.flyer_ad_extension, 'Description', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MediaIds,
            field_to_csv=lambda c: field_to_csv_MediaIds(c.flyer_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_MediaIds(c.flyer_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.flyer_ad_extension.FinalUrlSuffix, c.flyer_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.flyer_ad_extension, 'FinalUrlSuffix', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.flyer_ad_extension.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.flyer_ad_extension, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.flyer_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.flyer_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.flyer_ad_extension.FinalUrls, c.flyer_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.flyer_ad_extension.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.flyer_ad_extension.FinalMobileUrls, c.flyer_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.flyer_ad_extension.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MediaUrls,
            field_to_csv=lambda c: field_to_csv_Urls(c.flyer_ad_extension.ImageMediaUrls, c.flyer_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.flyer_ad_extension.ImageMediaUrls, v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.flyer_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('FlyerAdExtension')
        self.flyer_ad_extension.Type = 'FlyerAdExtension'
        super(BulkFlyerAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkFlyerAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.flyer_ad_extension, 'flyer_ad_extension')
        super(BulkFlyerAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkFlyerAdExtension._MAPPINGS)


class BulkAccountFlyerAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level flyer ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Flyer Ad Extension record in a bulk file.

    For more information, see Account Flyer Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass


class BulkCampaignFlyerAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level imflyerage ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Flyer Ad Extension record in a bulk file.

    For more information, see Campaign Flyer Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    """

    pass

class BulkAdGroupFlyerAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level flyer ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Flyer Ad Extension record in a bulk file.

    For more information, see Ad Group Flyer Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
