from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

from bingads.v13.internal.extensions import *


_DisclaimerAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('DisclaimerAdExtension'))


class BulkDisclaimerAdExtension(_BulkAdExtensionBase):
    """ Represents a disclaimer ad extension.

    This class exposes the :attr:`disclaimer_ad_extension` property that can be read and written
    as fields of the Disclaimer Ad Extension record in a bulk file.

    For more information, see Disclaimer Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _DisclaimerAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'DisclaimerAdExtension'
            ))
        super(BulkDisclaimerAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def disclaimer_ad_extension(self):
        """ The disclaimer ad extension.

        see Disclaimer Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @disclaimer_ad_extension.setter
    def disclaimer_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.DisclaimerName,
            field_to_csv=lambda c: bulk_str(c.disclaimer_ad_extension.Name),
            csv_to_field=lambda c, v: setattr(c.disclaimer_ad_extension, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DisclaimerTitle,
            field_to_csv=lambda c: bulk_str(c.disclaimer_ad_extension.Title),
            csv_to_field=lambda c, v: setattr(c.disclaimer_ad_extension, 'Title', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DisclaimerPopupText,
            field_to_csv=lambda c: bulk_str(c.disclaimer_ad_extension.PopupText),
            csv_to_field=lambda c, v: setattr(c.disclaimer_ad_extension, 'PopupText', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DisclaimerLineText,
            field_to_csv=lambda c: bulk_str(c.disclaimer_ad_extension.LineText),
            csv_to_field=lambda c, v: setattr(c.disclaimer_ad_extension, 'LineText', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DisclaimerLayout,
            field_to_csv=lambda c: bulk_str(c.disclaimer_ad_extension.DisclaimerLayout),
            csv_to_field=lambda c, v: setattr(c.disclaimer_ad_extension, 'DisclaimerLayout', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.disclaimer_ad_extension.FinalUrls, c.disclaimer_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.disclaimer_ad_extension.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.disclaimer_ad_extension.FinalMobileUrls, c.disclaimer_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.disclaimer_ad_extension.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_optional_str(c.disclaimer_ad_extension.TrackingUrlTemplate, c.disclaimer_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.disclaimer_ad_extension, 'TrackingUrlTemplate', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.disclaimer_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.disclaimer_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.disclaimer_ad_extension.FinalUrlSuffix, c.disclaimer_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.disclaimer_ad_extension, 'FinalUrlSuffix', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.disclaimer_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('DisclaimerAdExtension')
        self.disclaimer_ad_extension.Type = 'DisclaimerAdExtension'
        super(BulkDisclaimerAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkDisclaimerAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.disclaimer_ad_extension, 'disclaimer_ad_extension')
        super(BulkDisclaimerAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkDisclaimerAdExtension._MAPPINGS)

class BulkCampaignDisclaimerAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level disclaimer ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Disclaimer Ad Extension record in a bulk file.

    For more information, see Campaign Disclaimer Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
