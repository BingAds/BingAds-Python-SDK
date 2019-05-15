from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

from bingads.v13.internal.extensions import *


_ActionAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('ActionAdExtension'))


class BulkActionAdExtension(_BulkAdExtensionBase):
    """ Represents a action ad extension.

    This class exposes the :attr:`action_ad_extension` property that can be read and written
    as fields of the Action Ad Extension record in a bulk file.

    For more information, see Action Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _ActionAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'ActionAdExtension'
            ))
        super(BulkActionAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )
        self._action_text = None
        

    @property
    def action_ad_extension(self):
        """ The action ad extension.

        see Action Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @action_ad_extension.setter
    def action_ad_extension(self, value):
        self._ad_extension = value
        
        
    @property
    def action_text(self):
        """ The action text.

        """

        return self._action_text

    @action_text.setter
    def action_text(self, value):
        self._action_text = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.ActionType,
            field_to_csv=lambda c: bulk_str(c.action_ad_extension.ActionType),
            csv_to_field=lambda c, v: setattr(c.action_ad_extension, 'ActionType', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.action_ad_extension.FinalUrls, c.action_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.action_ad_extension.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.action_ad_extension.FinalMobileUrls, c.action_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.action_ad_extension.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_optional_str(c.action_ad_extension.TrackingUrlTemplate, c.action_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.action_ad_extension, 'TrackingUrlTemplate', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.Language,
            field_to_csv=lambda c: bulk_optional_str(c.action_ad_extension.Language, c.action_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.action_ad_extension, 'Language', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.action_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.action_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ActionText,
            field_to_csv=lambda c: c.action_text,
            csv_to_field=lambda c, v: setattr(c, 'action_text', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.action_ad_extension.FinalUrlSuffix, c.action_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.action_ad_extension, 'FinalUrlSuffix', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.action_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('ActionAdExtension')
        self.action_ad_extension.Type = 'ActionAdExtension'
        super(BulkActionAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkActionAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.action_ad_extension, 'action_ad_extension')
        super(BulkActionAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkActionAdExtension._MAPPINGS)


class BulkAccountActionAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level action ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Action Ad Extension record in a bulk file.

    For more information, see Account Action Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkCampaignActionAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level action ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Action Ad Extension record in a bulk file.

    For more information, see Campaign Action Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupActionAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level Action ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Action Ad Extension record in a bulk file.

    For more information, see Ad Group Action Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
