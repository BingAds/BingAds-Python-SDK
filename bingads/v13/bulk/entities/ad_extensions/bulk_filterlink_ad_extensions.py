from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.extensions import *
from .common import _BulkAdExtensionBase
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

_FilterLinkAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('FilterLinkAdExtension'))


class BulkFilterLinkAdExtension(_BulkAdExtensionBase):
    """ Represents a filter link ad extension.

    This class exposes the :attr:`filter_link_ad_extension` property that can be read and written
    as fields of the Filter Link Ad Extension record in a bulk file.

    For more information, see Filter Link Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _FilterLinkAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'FilterLinkAdExtension'
            ))
        super(BulkFilterLinkAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def filter_link_ad_extension(self):
        """ The filter link ad extension.

        see Filter Link Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @filter_link_ad_extension.setter
    def filter_link_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.AdExtensionHeaderType,
            field_to_csv=lambda c: bulk_str(c.filter_link_ad_extension.AdExtensionHeaderType),
            csv_to_field=lambda c, v: setattr(c.filter_link_ad_extension, 'AdExtensionHeaderType', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Language,
            field_to_csv=lambda c: c.filter_link_ad_extension.Language,
            csv_to_field=lambda c, v: setattr(c.filter_link_ad_extension, 'Language', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Texts,
            field_to_csv=lambda c: field_to_csv_delimited_strings(c.filter_link_ad_extension.Texts),
            csv_to_field=lambda c, v: csv_to_field_delimited_strings(c.filter_link_ad_extension.Texts, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.filter_link_ad_extension.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.filter_link_ad_extension, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.filter_link_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.filter_link_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.filter_link_ad_extension.FinalUrls, c.filter_link_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.filter_link_ad_extension.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.filter_link_ad_extension.FinalMobileUrls, c.filter_link_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.filter_link_ad_extension.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.filter_link_ad_extension.FinalUrlSuffix, c.filter_link_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.filter_link_ad_extension, 'FinalUrlSuffix', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.filter_link_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('FilterLinkAdExtension')
        self.filter_link_ad_extension.Type = 'FilterLinkAdExtension'
        super(BulkFilterLinkAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkFilterLinkAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.filter_link_ad_extension, 'filter_link_ad_extension')
        super(BulkFilterLinkAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkFilterLinkAdExtension._MAPPINGS)


class BulkAccountFilterLinkAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level filter link ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Filter Link Ad Extension record in a bulk file.

    For more information, see Account Filter Link Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass


class BulkCampaignFilterLinkAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level filter link ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Filter Link Ad Extension record in a bulk file.

    For more information, see Campaign Filter Link Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupFilterLinkAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level filter link ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Filter Link Ad Extension record in a bulk file.

    For more information, see Ad Group Filter Link Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
