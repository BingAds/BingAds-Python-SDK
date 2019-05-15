from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

from bingads.v13.internal.extensions import *

_SitelinkAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('SitelinkAdExtension'))


class BulkSitelinkAdExtension(_BulkAdExtensionBase):
    """ Represents a sitelink ad extension.

    This class exposes the :attr:`sitelink_ad_extension` property that can be read and written
    as fields of the Sitelink Ad Extension record in a bulk file.

    For more information, see Sitelink Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _SitelinkAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'SitelinkAdExtension'
            ))
        super(BulkSitelinkAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def sitelink_ad_extension(self):
        """ The sitelink ad extension.

        see Sitelink Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @sitelink_ad_extension.setter
    def sitelink_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDescription1,
            field_to_csv=lambda c: c.sitelink_ad_extension.Description1,
            csv_to_field=lambda c, v: setattr(c.sitelink_ad_extension, 'Description1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDescription2,
            field_to_csv=lambda c: c.sitelink_ad_extension.Description2,
            csv_to_field=lambda c, v: setattr(c.sitelink_ad_extension, 'Description2', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DestinationUrl,
            field_to_csv=lambda c: bulk_optional_str(c.sitelink_ad_extension.DestinationUrl, c.sitelink_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.sitelink_ad_extension, 'DestinationUrl', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDisplayText,
            field_to_csv=lambda c: c.sitelink_ad_extension.DisplayText,
            csv_to_field=lambda c, v: setattr(c.sitelink_ad_extension, 'DisplayText', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.sitelink_ad_extension.FinalUrls, c.sitelink_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.sitelink_ad_extension.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.sitelink_ad_extension.FinalMobileUrls, c.sitelink_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.sitelink_ad_extension.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.sitelink_ad_extension.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.sitelink_ad_extension, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.sitelink_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.sitelink_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.sitelink_ad_extension.FinalUrlSuffix, c.sitelink_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.sitelink_ad_extension, 'FinalUrlSuffix', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.sitelink_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('SitelinkAdExtension')
        self.sitelink_ad_extension.Type = 'SitelinkAdExtension'
        super(BulkSitelinkAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkSitelinkAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.sitelink_ad_extension, 'sitelink_ad_extension')
        super(BulkSitelinkAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkSitelinkAdExtension._MAPPINGS)


class BulkAccountSitelinkAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level sitelink ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Sitelink Ad Extension record in a bulk file.

    For more information, see Account Sitelink Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkCampaignSitelinkAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level sitelink ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Sitelink Ad Extension record in a bulk file.

    For more information, see Campaign Sitelink Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupSitelinkAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level Sitelink ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Sitelink Ad Extension record in a bulk file.

    For more information, see Ad Group Sitelink Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
