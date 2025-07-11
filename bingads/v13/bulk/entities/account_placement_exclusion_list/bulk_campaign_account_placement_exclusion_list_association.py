from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkAccountPlacementExclusionListAssociation(_SingleRecordBulkEntity):
    """ Represents an account placement exclusion list association.

    This class exposes the property :attr:`shared_entity_association` that can be read and written as fields of the account placement exclusion list association record
    in a bulk file.

    For more information, see account placement exclusion list association at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, shared_entity_association=None):
        super(BulkAccountPlacementExclusionListAssociation, self).__init__()

        self._status = status
        self._shared_entity_association = shared_entity_association


    @property
    def status(self):
        """ The status of the account placement exclusion list association.

        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def shared_entity_association(self):
        """ The AccountPlacementExclusionList Data Object of the Campaign Management Service.

        A subset of AccountPlacementExclusionList properties are available in the Ad Group record.
        For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._shared_entity_association

    @shared_entity_association.setter
    def shared_entity_association(self, shared_entity_association):
        self._shared_entity_association = shared_entity_association

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.shared_entity_association.SharedEntityId),
            csv_to_field=lambda c, v: setattr(c.shared_entity_association, 'SharedEntityId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.shared_entity_association.EntityId),
            csv_to_field=lambda c, v: setattr(c.shared_entity_association, 'EntityId', v)
        ),
    ]


    def process_mappings_from_row_values(self, row_values):
        self.shared_entity_association = _CAMPAIGN_OBJECT_FACTORY_V13.create('AccountPlacementExclusionList')

        row_values.convert_to_entity(self, BulkAccountPlacementExclusionListAssociation._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._shared_entity_association, 'AccountPlacementExclusionList')
        self.convert_to_values(row_values, BulkAccountPlacementExclusionListAssociation._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAccountPlacementExclusionListAssociation, self).read_additional_data(stream_reader)
