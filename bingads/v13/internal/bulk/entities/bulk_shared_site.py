from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkSharedSite(_SingleRecordBulkEntity):
    """ Represents a site.

    This class exposes the property :attr:`site` that can be read and written as fields of the site record
    in a bulk file.

    For more information, see site at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, parent_id=None, url=None, status=None, site=None):
        super(BulkSharedSite, self).__init__()

        self._parent_id = parent_id
        self._url = url
        self._status = status
        self._site = site

    @property
    def parent_id(self):
        """ The identifier of the parent entity that contains the site.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        self._parent_id = parent_id

    @property
    def url(self):
        """ The url of a website.

        Corresponds to the 'Website' field in the bulk file.

        :rtype: str
        """

        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def status(self):
        """ The status of the site.

        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.site.Id),
            csv_to_field=lambda c, v: setattr(c.site, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.parent_id),
            csv_to_field=lambda c, v: setattr(c, 'parent_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AccountPlacementListItemUrl,
            field_to_csv=lambda c: bulk_str(c.site.Url),
            csv_to_field=lambda c, v: setattr(c.site, 'Url', v if v else None)
        ),
    ]


    def process_mappings_from_row_values(self, row_values):
        self.site = _CAMPAIGN_OBJECT_FACTORY_V13.create('Site')

        row_values.convert_to_entity(self, BulkSharedSite._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._site, 'Site')
        self.convert_to_values(row_values, BulkSharedSite._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkSharedSite, self).read_additional_data(stream_reader)
