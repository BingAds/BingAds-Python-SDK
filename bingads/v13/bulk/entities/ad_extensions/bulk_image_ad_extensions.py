from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.extensions import *
from .common import _BulkAdExtensionBase
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

_ImageAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('ImageAdExtension'))


class BulkImageAdExtension(_BulkAdExtensionBase):
    """ Represents a image ad extension.

    This class exposes the :attr:`image_ad_extension` property that can be read and written
    as fields of the Image Ad Extension record in a bulk file.

    For more information, see Image Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _ImageAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'ImageAdExtension'
            ))
        super(BulkImageAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def image_ad_extension(self):
        """ The image ad extension.

        see Image Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @image_ad_extension.setter
    def image_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.DestinationUrl,
            field_to_csv=lambda c: bulk_optional_str(c.image_ad_extension.DestinationUrl, c.image_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.image_ad_extension, 'DestinationUrl', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.AltText,
            field_to_csv=lambda c: c.image_ad_extension.AlternativeText,
            csv_to_field=lambda c, v: setattr(c.image_ad_extension, 'AlternativeText', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MediaIds,
            field_to_csv=lambda c: field_to_csv_MediaIds(c.image_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_MediaIds(c.image_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.image_ad_extension.FinalUrlSuffix, c.image_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.image_ad_extension, 'FinalUrlSuffix', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_optional_str(c.image_ad_extension.TrackingUrlTemplate, c.image_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.image_ad_extension, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.image_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.image_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.image_ad_extension.FinalUrls, c.image_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.image_ad_extension.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.image_ad_extension.FinalMobileUrls, c.image_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.image_ad_extension.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DisplayText,
            field_to_csv=lambda c: bulk_optional_str(c.image_ad_extension.DisplayText, c.image_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.image_ad_extension, 'DisplayText', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.Layouts,
            field_to_csv=lambda c: field_to_csv_delimited_strings(c.image_ad_extension.Layouts),
            csv_to_field=lambda c, v: csv_to_field_delimited_strings(c.image_ad_extension.Layouts, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Images,
            field_to_csv=lambda c: field_to_csv_ImageAssetLinks(c.image_ad_extension.Images),
            csv_to_field=lambda c, v: csv_to_field_ImageAssetLinks(c.image_ad_extension.Images, v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.image_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('ImageAdExtension')
        self.image_ad_extension.Type = 'ImageAdExtension'
        super(BulkImageAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkImageAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.image_ad_extension, 'image_ad_extension')
        super(BulkImageAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkImageAdExtension._MAPPINGS)


class BulkAccountImageAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level image ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Image Ad Extension record in a bulk file.

    For more information, see Account Image Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass


class BulkCampaignImageAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level image ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Image Ad Extension record in a bulk file.

    For more information, see Campaign Image Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupImageAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level image ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Image Ad Extension record in a bulk file.

    For more information, see Ad Group Image Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
