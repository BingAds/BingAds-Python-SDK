from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_conversion_goal import BulkConversionGoal

class BulkProductGoal(BulkConversionGoal):
    """ Represents an ProductGoal Goal that can be read or written in a bulk file.

    This class exposes the :attr:`product_goal` property that can be read and written as fields of the
    ProductGoal Goal record in a bulk file.

    For more information, see ProductGoal Goal at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 product_goal=None):
        super(BulkProductGoal, self).__init__(conversion_goal = product_goal)

    _MAPPINGS = [

    ]

    @property
    def product_goal(self):
        """ Defines a ProductGoal Goal """

        return self._conversion_goal

    @product_goal.setter
    def product_goal(self, product_goal):
        self._conversion_goall = product_goal


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.product_goal, 'product_goal')
        super(BulkProductGoal, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkProductGoal._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.product_goal = _CAMPAIGN_OBJECT_FACTORY_V13.create('ConversionGoal')
        super(BulkProductGoal, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkProductGoal._MAPPINGS)

