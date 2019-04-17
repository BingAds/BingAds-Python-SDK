from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import *
from .common import _BulkAdExtensionBase
from .common import _BulkCampaignAdExtensionAssociation

_CallAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('CallAdExtension'))


class BulkCallAdExtension(_BulkAdExtensionBase):
    """ Represents a call ad extension.

    This class exposes the :attr:`call_ad_extension` property that can be read and written
    as fields of the Call Ad Extension record in a bulk file.

    For more information, see Call Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 account_id=None,
                 ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _CallAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'CallAdExtension'
            ))
        super(BulkCallAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def call_ad_extension(self):
        """ The call ad extension.

        see Call Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @call_ad_extension.setter
    def call_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.PhoneNumber,
            field_to_csv=lambda c: c.call_ad_extension.PhoneNumber,
            csv_to_field=lambda c, v: setattr(c.call_ad_extension, 'PhoneNumber', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CountryCode,
            field_to_csv=lambda c: c.call_ad_extension.CountryCode,
            csv_to_field=lambda c, v: setattr(c.call_ad_extension, 'CountryCode', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.IsCallOnly,
            field_to_csv=lambda c: bulk_str(c.call_ad_extension.IsCallOnly),
            csv_to_field=lambda c, v: setattr(c.call_ad_extension, 'IsCallOnly',
                                              v.lower() == 'true' if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.IsCallTrackingEnabled,
            field_to_csv=lambda c: bulk_str(c.call_ad_extension.IsCallTrackingEnabled),
            csv_to_field=lambda c, v: setattr(c.call_ad_extension, 'IsCallTrackingEnabled',
                                              v.lower() == 'true' if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.RequireTollFreeTrackingNumber,
            field_to_csv=lambda c: bulk_str(c.call_ad_extension.RequireTollFreeTrackingNumber),
            csv_to_field=lambda c, v: setattr(c.call_ad_extension, 'RequireTollFreeTrackingNumber',
                                              v.lower() == 'true' if v else None)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.call_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('CallAdExtension')
        self.call_ad_extension.Type = 'CallAdExtension'
        super(BulkCallAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkCallAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.call_ad_extension, 'call_ad_extension')
        super(BulkCallAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkCallAdExtension._MAPPINGS)


class BulkCampaignCallAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level call ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Call Ad Extension record in a bulk file.

    For more information, see Campaign Call Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
