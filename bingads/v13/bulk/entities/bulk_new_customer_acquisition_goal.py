from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *
from decimal import Decimal


class BulkNewCustomerAcquisitionGoal (_SingleRecordBulkEntity):
    """ Represents a new customer acquisition goal that can be read or written in a bulk file.

    Properties of this class and of classes that it is derived from, correspond to fields of the Budget record in a bulk file.
    For more information, see Budget at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, new_customer_acquisition_goal=None, target=None):
        super(BulkNewCustomerAcquisitionGoal , self).__init__()
        self._new_customer_acquisition_goal = new_customer_acquisition_goal
        self._target = target

    @property
    def new_customer_acquisition_goal (self):
        """
        the NewCustomerAcquisitionGoal object, see more detail at: https://go.microsoft.com/fwlink/?linkid=846127
        """
        return self._new_customer_acquisition_goal

    @new_customer_acquisition_goal .setter
    def new_customer_acquisition_goal (self, value):
        self._new_customer_acquisition_goal  = value

    @property
    def target(self):
        """
        The ids of audiences within the new customer acquisition.
        It should be split by simicolon. example: "123;456;789"
        Corresponds to 'Target' field in bulk file.
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, value):
        self._target = value


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.new_customer_acquisition_goal .Id),
            csv_to_field=lambda c, v: setattr(c.new_customer_acquisition_goal , 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Target,
            field_to_csv=lambda c: bulk_str(c.target),
            csv_to_field=lambda c, v: setattr(c, 'target', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdditionalConversionValue,
            field_to_csv=lambda c: bulk_str(c.new_customer_acquisition_goal.AdditionalValue),
            csv_to_field=lambda c, v: setattr(c.new_customer_acquisition_goal , 'AdditionalValue', Decimal(v) if v else None)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self._new_customer_acquisition_goal  = _CAMPAIGN_OBJECT_FACTORY_V13.create('NewCustomerAcquisitionGoal')
        row_values.convert_to_entity(self, BulkNewCustomerAcquisitionGoal ._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.new_customer_acquisition_goal , 'new_customer_acquisition_goal ')
        self.convert_to_values(row_values, BulkNewCustomerAcquisitionGoal ._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkNewCustomerAcquisitionGoal , self).read_additional_data(stream_reader)
