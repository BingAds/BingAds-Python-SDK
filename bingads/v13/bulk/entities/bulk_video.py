from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *
from decimal import Decimal


class BulkVideo(_SingleRecordBulkEntity):
    """ Represents a video that can be read or written in a bulk file.

    Properties of this class and of classes that it is derived from, correspond to fields of the Video record in a bulk file.
    For more information, see Video at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, video=None, account_id=None):
        super(BulkVideo, self).__init__()
        self._account_id = account_id
        self._video=video

    @property
    def video(self):
        """
        the Video object
        """
        return self._video

    @video.setter
    def video(self, value):
        self._video = value

    @property
    def account_id(self):
        """ the id of the account which contains the video
        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: long
        """
        return self._account_id
    
    @account_id.setter
    def account_id(self, value):
        self._account_id = value


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.video.Id),
            csv_to_field=lambda c, v: setattr(c.video, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, 'account_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.video.Status,
            csv_to_field=lambda c, v: setattr(c.video, 'Status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Description,
            field_to_csv=lambda c: bulk_str(c.video.Description),
            csv_to_field=lambda c, v: setattr(c.video, 'Description', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AspectRatio,
            field_to_csv=lambda c: bulk_str(c.video.AspectRatio),
            csv_to_field=lambda c, v: setattr(c.video, 'AspectRatio', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Url,
            field_to_csv=lambda c: bulk_str(c.video.Url),
            csv_to_field=lambda c, v: setattr(c.video, 'Url', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SourceUrl,
            field_to_csv=lambda c: bulk_str(c.video.SourceUrl),
            csv_to_field=lambda c, v: setattr(c.video, 'SourceUrl', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ThumbnailUrl,
            field_to_csv=lambda c: bulk_str(c.video.ThumbnailUrl),
            csv_to_field=lambda c, v: setattr(c.video, 'ThumbnailUrl', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DurationInMillionSeconds,
            field_to_csv=lambda c: bulk_str(c.video.DurationInMilliseconds),
            csv_to_field=lambda c, v: setattr(c.video, 'DurationInMilliseconds', int(v) if v else None)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        self.video=_CAMPAIGN_OBJECT_FACTORY_V13.create('Video')
        row_values.convert_to_entity(self, BulkVideo._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkVideo._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkVideo, self).read_additional_data(stream_reader)
