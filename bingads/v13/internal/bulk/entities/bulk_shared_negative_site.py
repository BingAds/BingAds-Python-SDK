from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkSharedNegativeSite(_SingleRecordBulkEntity):
    """ Represents a negative site.

    This class exposes the property :attr:`negative_site` that can be read and written as fields of the negative site record
    in a bulk file.

    For more information, see negative site at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, parent_id=None, status=None, negative_site=None):
        super(BulkSharedNegativeSite, self).__init__()

        self._parent_id = parent_id
        self._status = status
        self._negative_site = negative_site

    @property
    def parent_id(self):
        """ The identifier of the parent entity that contains the negative site.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        self._parent_id = parent_id

    @property
    def status(self):
        """ The status of the negative site.

        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def negative_site(self):
        """ The NegativeSite Data Object of the Campaign Management Service.

        A subset of NegativeSite properties are available in the Ad Group record.
        For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._negative_site

    @negative_site.setter
    def negative_site(self, negative_site):
        self._negative_site = negative_site

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.negative_site.Id),
            csv_to_field=lambda c, v: setattr(c.negative_site, 'Id', int(v) if v else None)
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
            field_to_csv=lambda c: bulk_str(c.negative_site.Url),
            csv_to_field=lambda c, v: setattr(c.negative_site, 'Url', v if v else None)
        ),
    ]


    def process_mappings_from_row_values(self, row_values):
        self.negative_site = _CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeSite')

        row_values.convert_to_entity(self, BulkSharedNegativeSite._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._negative_site, 'NegativeSite')
        self.convert_to_values(row_values, BulkSharedNegativeSite._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkSharedNegativeSite, self).read_additional_data(stream_reader)
