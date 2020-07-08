from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_audience import BulkAudience

class BulkCombinedList(BulkAudience):
    """ Represents a CombinedList that can be read or written in a bulk file.

    This class exposes the :attr:`combined_list` property that can be read and written as fields of the
    CombinedList record in a bulk file.

    For more information, see CombinedList at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 combined_list=None,
                 status=None):
        super(BulkCombinedList, self).__init__(audience = combined_list, status = status)


    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.CombinationRule,
            field_to_csv=lambda c: combination_rules_to_bulkstring(c.combined_list.CombinationRules) if c.combined_list.CombinationRules else None,
            csv_to_field=lambda c, v: parse_combination_rules(c.combined_list, v)
        )
    ]

    @property
    def combined_list(self):
        """ Defines a CombinedList """

        return self._audience

    @combined_list.setter
    def combined_list(self, combined_list):
        self._audience = combined_list

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.combined_list, 'combined_list')
        super(BulkCombinedList, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkCombinedList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.combined_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('CombinedList')
        super(BulkCombinedList, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkCombinedList._MAPPINGS)

