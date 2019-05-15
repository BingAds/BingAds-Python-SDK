from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

from bingads.v13.internal.extensions import *


_AppAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('AppAdExtension'))


class BulkAppAdExtension(_BulkAdExtensionBase):
    """ Represents a app ad extension.

    This class exposes the :attr:`app_ad_extension` property that can be read and written
    as fields of the App Ad Extension record in a bulk file.

    For more information, see App Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _AppAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'AppAdExtension'
            ))
        super(BulkAppAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def app_ad_extension(self):
        """ The app ad extension.

        see App Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @app_ad_extension.setter
    def app_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.AppPlatform,
            field_to_csv=lambda c: c.app_ad_extension.AppPlatform,
            csv_to_field=lambda c, v: setattr(c.app_ad_extension, 'AppPlatform', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AppStoreId,
            field_to_csv=lambda c: c.app_ad_extension.AppStoreId,
            csv_to_field=lambda c, v: setattr(c.app_ad_extension, 'AppStoreId', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DestinationUrl,
            field_to_csv=lambda c: c.app_ad_extension.DestinationUrl,
            csv_to_field=lambda c, v: setattr(c.app_ad_extension, 'DestinationUrl', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Text,
            field_to_csv=lambda c: c.app_ad_extension.DisplayText,
            csv_to_field=lambda c, v: setattr(c.app_ad_extension, 'DisplayText', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.app_ad_extension.FinalUrlSuffix, c.app_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.app_ad_extension, 'FinalUrlSuffix', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.app_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('AppAdExtension')
        self.app_ad_extension.Type = 'AppAdExtension'
        super(BulkAppAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAppAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.app_ad_extension, 'app_ad_extension')
        super(BulkAppAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAppAdExtension._MAPPINGS)


class BulkAccountAppAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level app ad extension.

    This class exposes properties that can be read and written
    as fields of the Account App Ad Extension record in a bulk file.

    For more information, see Account App Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkCampaignAppAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level app ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign App Ad Extension record in a bulk file.

    For more information, see Campaign App Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupAppAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level App ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group App Ad Extension record in a bulk file.

    For more information, see Ad Group App Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
