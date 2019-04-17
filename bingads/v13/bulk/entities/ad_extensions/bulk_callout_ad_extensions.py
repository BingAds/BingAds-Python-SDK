from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

_CalloutAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('CalloutAdExtension'))


class BulkCalloutAdExtension(_BulkAdExtensionBase):
    """ Represents a callout ad extension.

    This class exposes the :attr:`callout_ad_extension` property that can be read and written
    as fields of the Callout Ad Extension record in a bulk file.

    For more information, see Callout Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _CalloutAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'CalloutAdExtension'
            ))
        super(BulkCalloutAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def callout_ad_extension(self):
        """ The callout ad extension.

        see Callout Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @callout_ad_extension.setter
    def callout_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.CalloutText,
            field_to_csv=lambda c: c.callout_ad_extension.Text,
            csv_to_field=lambda c, v: setattr(c.callout_ad_extension, 'Text', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.callout_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('CalloutAdExtension')
        self.callout_ad_extension.Type = 'CalloutAdExtension'
        super(BulkCalloutAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkCalloutAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.callout_ad_extension, 'callout_ad_extension')
        super(BulkCalloutAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkCalloutAdExtension._MAPPINGS)


class BulkAccountCalloutAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level callout ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Callout Ad Extension record in a bulk file.

    For more information, see Account Callout Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkCampaignCalloutAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level callout ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Callout Ad Extension record in a bulk file.

    For more information, see Campaign Callout Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupCalloutAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level Callout ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Callout Ad Extension record in a bulk file.

    For more information, see Ad Group Callout Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
