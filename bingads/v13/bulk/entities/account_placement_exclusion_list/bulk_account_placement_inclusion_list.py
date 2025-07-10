from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkAccountPlacementInclusionList(_SingleRecordBulkEntity):
    """ Represents an account placement inclusion list.

    This class exposes the property :attr:`account_placement_inclusion_list` that can be read and written as fields of the account placement inclusion list record
    in a bulk file.

    For more information, see account placement inclusion list at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, account_placement_inclusion_list=None):
        super(BulkAccountPlacementInclusionList, self).__init__()

        self._status = status
        self._account_placement_inclusion_list = account_placement_inclusion_list


    @property
    def status(self):
        """ The status of the account placement inclusion list.

        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def account_placement_inclusion_list(self):
        """ The AccountPlacementInclusionList Data Object of the Campaign Management Service.

        A subset of AccountPlacementInclusionList properties are available in the Ad Group record.
        For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._account_placement_inclusion_list

    @account_placement_inclusion_list.setter
    def account_placement_inclusion_list(self, account_placement_inclusion_list):
        self._account_placement_inclusion_list = account_placement_inclusion_list

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.account_placement_inclusion_list.Id),
            csv_to_field=lambda c, v: setattr(c.account_placement_inclusion_list, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: bulk_str(c.account_placement_inclusion_list.Name),
            csv_to_field=lambda c, v: setattr(c.account_placement_inclusion_list, 'Name', v)
        ),
    ]


    def process_mappings_from_row_values(self, row_values):
        self.account_placement_inclusion_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('AccountPlacementInclusionList')

        row_values.convert_to_entity(self, BulkAccountPlacementInclusionList._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._account_placement_inclusion_list, 'AccountPlacementInclusionList')
        self.convert_to_values(row_values, BulkAccountPlacementInclusionList._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAccountPlacementInclusionList, self).read_additional_data(stream_reader)
