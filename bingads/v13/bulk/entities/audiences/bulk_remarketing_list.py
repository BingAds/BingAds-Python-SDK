from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_audience import BulkAudience

class BulkRemarketingList(BulkAudience):
    """ Represents an Remarketing List that can be read or written in a bulk file.

    This class exposes the :attr:`remarketing_list` property that can be read and written as fields of the
    Remarketing List record in a bulk file.

    For more information, see Remarketing List at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 remarketing_list=None,
                 status=None,):
        super(BulkRemarketingList, self).__init__(audience = remarketing_list, status = status)

    _MAPPINGS = [
       
        _SimpleBulkMapping(
            _StringTable.TagId,
            field_to_csv=lambda c: bulk_str(c.remarketing_list.TagId),
            csv_to_field=lambda c, v: setattr(c.remarketing_list, 'TagId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.RemarketingRule,
            field_to_csv=lambda c: field_to_csv_RemarketingRule(c.remarketing_list),
            csv_to_field=lambda c, v: csv_to_field_RemarketingRule(c.remarketing_list, v)
        ),
    ]

    @property
    def remarketing_list(self):
        """ Defines a Remarketing List """

        return self._audience

    @remarketing_list.setter
    def remarketing_list(self, remarketing_list):
        self._audience = remarketing_list
   

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.remarketing_list, 'remarketing_list')
        super(BulkRemarketingList, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkRemarketingList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.remarketing_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('RemarketingList')
        super(BulkRemarketingList, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkRemarketingList._MAPPINGS)

