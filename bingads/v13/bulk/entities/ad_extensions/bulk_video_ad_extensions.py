from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.extensions import *
from .common import _BulkAdExtensionBase
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

_VideoAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('VideoAdExtension'))


class BulkVideoAdExtension(_BulkAdExtensionBase):
    """ Represents a video ad extension.

    This class exposes the :attr:`video_ad_extension` property that can be read and written
    as fields of the Video Ad Extension record in a bulk file.

    For more information, see Video Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _VideoAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'VideoAdExtension'
            ))
        super(BulkVideoAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def video_ad_extension(self):
        """ The video ad extension.

        see Video Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @video_ad_extension.setter
    def video_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: bulk_optional_str(c.video_ad_extension.Name, c.video_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.video_ad_extension, 'Name', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.DisplayText,
            field_to_csv=lambda c: bulk_optional_str(c.video_ad_extension.DisplayText, c.video_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.video_ad_extension, 'DisplayText', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.AltText,
            field_to_csv=lambda c: bulk_str(c.video_ad_extension.AlternativeText),
            csv_to_field=lambda c, v: setattr(c.video_ad_extension, 'AlternativeText', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ActionText,
            field_to_csv=lambda c: bulk_optional_str(c.video_ad_extension.ActionText, c.video_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.video_ad_extension, 'ActionText', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.ThumbnailUrl,
            field_to_csv=lambda c: bulk_str(c.video_ad_extension.ThumbnailUrl),
            csv_to_field=lambda c, v: setattr(c.video_ad_extension, 'ThumbnailUrl', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ThumbnailId,
            field_to_csv=lambda c: bulk_str(c.video_ad_extension.ThumbnailId),
            csv_to_field=lambda c, v: setattr(c.video_ad_extension, 'ThumbnailId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.VideoId,
            field_to_csv=lambda c: bulk_str(c.video_ad_extension.VideoId),
            csv_to_field=lambda c, v: setattr(c.video_ad_extension, 'VideoId', int(v) if v else None)
        ),        
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.video_ad_extension.FinalUrlSuffix, c.video_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.video_ad_extension, 'FinalUrlSuffix', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.video_ad_extension.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.video_ad_extension, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.video_ad_extension),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.video_ad_extension, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.video_ad_extension.FinalUrls, c.video_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.video_ad_extension.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.video_ad_extension.FinalMobileUrls, c.video_ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.video_ad_extension.FinalMobileUrls, v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.video_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('VideoAdExtension')
        self.video_ad_extension.Type = 'VideoAdExtension'
        super(BulkVideoAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkVideoAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.video_ad_extension, 'video_ad_extension')
        super(BulkVideoAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkVideoAdExtension._MAPPINGS)


class BulkAccountVideoAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level video ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Video Ad Extension record in a bulk file.

    For more information, see Account Video Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass


class BulkCampaignVideoAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level video ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Video Ad Extension record in a bulk file.

    For more information, see Campaign Video Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupVideoAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level video ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Video Ad Extension record in a bulk file.

    For more information, see Ad Group Video Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
