from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_audience import BulkAudience

class BulkCustomerList(BulkAudience):
    """ Represents a CustomerList that can be read or written in a bulk file.

    This class exposes the :attr:`customer_list` property that can be read and written as fields of the
    CustomerList record in a bulk file.

    For more information, see CustomerList at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 customer_list=None,
                 status=None,
                 action_type = None):
        super(BulkCustomerList, self).__init__(audience = customer_list, status = status)
        self._action_type = action_type


    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.ActionType,
            field_to_csv=lambda c: bulk_str(c.action_type),
            csv_to_field=lambda c, v: setattr(c, 'action_type', v)
        )
    ]
    
    @property
    def action_type(self):
        """ Defines a action_type """

        return self._action_type

    @action_type.setter
    def action_type(self, action_type):
        self._action_type = action_type

    @property
    def customer_list(self):
        """ Defines a CustomerList """

        return self._audience

    @customer_list.setter
    def customer_list(self, customer_list):
        self._audience = customer_list

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.customer_list, 'customer_list')
        super(BulkCustomerList, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkCustomerList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.customer_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('Audience')
        super(BulkCustomerList, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkCustomerList._MAPPINGS)

