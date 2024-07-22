from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_conversion_goal import BulkConversionGoal

class BulkInStoreVisitGoal(BulkConversionGoal):
    """ Represents an InStoreVisit Goal that can be read or written in a bulk file.

    This class exposes the :attr:`in_store_visit_goal` property that can be read and written as fields of the
    InStoreVisit Goal record in a bulk file.

    For more information, see InStoreVisit Goal at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 in_store_visit_goal=None,):
        super(BulkInStoreVisitGoal, self).__init__(conversion_goal = in_store_visit_goal)

    _MAPPINGS = [

    ]

    @property
    def in_store_visit_goal(self):
        """ Defines a InStoreVisit Goal """

        return self._conversion_goal

    @in_store_visit_goal.setter
    def in_store_visit_goal(self, in_store_visit_goal):
        self._conversion_goall = in_store_visit_goal


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.in_store_visit_goal, 'in_store_visit_goal')
        super(BulkInStoreVisitGoal, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkInStoreVisitGoal._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.in_store_visit_goal = _CAMPAIGN_OBJECT_FACTORY_V13.create('ConversionGoal')
        super(BulkInStoreVisitGoal, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkInStoreVisitGoal._MAPPINGS)

