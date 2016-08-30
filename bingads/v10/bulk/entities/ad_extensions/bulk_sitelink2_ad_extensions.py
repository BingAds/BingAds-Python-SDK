from bingads.v10.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v10.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V10

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation

from bingads.internal.extensions import *

_Sitelink2AdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V10.create('Sitelink2AdExtension'))


class BulkSitelink2AdExtension(_BulkAdExtensionBase):
    """ Represents a sitelink2 ad extension.

    This class exposes the :attr:`sitelink2_ad_extension` property that can be read and written
    as fields of the Sitelink2 Ad Extension record in a bulk file.

    For more information, see Sitelink2 Ad Extension at http://go.microsoft.com/fwlink/?LinkID=799375.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _Sitelink2AdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'Sitelink2AdExtension'
            ))
        super(BulkSitelink2AdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def sitelink2_ad_extension(self):
        """ The sitelink2 ad extension.

        see Sitelink2 Ad Extension at http://go.microsoft.com/fwlink/?LinkID=799375.
        """

        return self._ad_extension

    @sitelink2_ad_extension.setter
    def sitelink2_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDescription1,
            field_to_csv=lambda c: c.sitelink2_ad_extension.Description1,
            csv_to_field=lambda c, v: setattr(c.sitelink2_ad_extension, 'Description1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDescription2,
            field_to_csv=lambda c: c.sitelink2_ad_extension.Description2,
            csv_to_field=lambda c, v: setattr(c.sitelink2_ad_extension, 'Description2', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DestinationUrl,
            field_to_csv=lambda c: bulk_optional_str(c.sitelink2_ad_extension.DestinationUrl),
            csv_to_field=lambda c, v: setattr(c.sitelink2_ad_extension, 'DestinationUrl', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.DevicePreference,
            field_to_csv=lambda c: bulk_device_preference_str(c.sitelink2_ad_extension.DevicePreference),
            csv_to_field=lambda c, v: setattr(c.sitelink2_ad_extension, 'DevicePreference', parse_device_preference(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDisplayText,
            field_to_csv=lambda c: c.sitelink2_ad_extension.DisplayText,
            csv_to_field=lambda c, v: setattr(c.sitelink2_ad_extension, 'DisplayText', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.sitelink2_ad_extension.FinalUrls),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.sitelink2_ad_extension.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.sitelink2_ad_extension.FinalMobileUrls),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.sitelink2_ad_extension.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.sitelink2_ad_extension.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.sitelink2_ad_extension, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.sitelink2_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.sitelink2_ad_extension, v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.sitelink2_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V10.create('Sitelink2AdExtension')
        self.sitelink2_ad_extension.Type = 'Sitelink2AdExtension'
        super(BulkSitelink2AdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkSitelink2AdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.sitelink2_ad_extension, 'sitelink2_ad_extension')
        super(BulkSitelink2AdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkSitelink2AdExtension._MAPPINGS)


class BulkCampaignSitelink2AdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents an campaign level sitelink2 ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Sitelink2 Ad Extension record in a bulk file.

    For more information, see Campaign Sitelink2 Ad Extension at http://go.microsoft.com/fwlink/?LinkID=823166.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass


class BulkAdGroupSitelink2AdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level Sitelink2 ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Sitelink2 Ad Extension record in a bulk file.

    For more information, see Ad Group Sitelink2 Ad Extension at http://go.microsoft.com/fwlink/?LinkID=823165.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
