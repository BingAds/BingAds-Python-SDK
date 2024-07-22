from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_conversion_goal import BulkConversionGoal

class BulkOfflineConversionGoal(BulkConversionGoal):
    """ Represents an OfflineConversion Goal that can be read or written in a bulk file.

    This class exposes the :attr:`offline_conversion_goal` property that can be read and written as fields of the
    OfflineConversion Goal record in a bulk file.

    For more information, see OfflineConversion Goal at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 offline_conversion_goal=None):
        super(BulkOfflineConversionGoal, self).__init__(conversion_goal = offline_conversion_goal)

    _MAPPINGS = [

    ]

    @property
    def offline_conversion_goal(self):
        """ Defines a OfflineConversion Goal """

        return self._conversion_goal

    @offline_conversion_goal.setter
    def offline_conversion_goal(self, offline_conversion_goal):
        self._conversion_goal = offline_conversion_goal


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.offline_conversion_goal, 'offline_conversion_goal')
        super(BulkOfflineConversionGoal, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkOfflineConversionGoal._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.offline_conversion_goal = _CAMPAIGN_OBJECT_FACTORY_V13.create('OfflineConversionGoal')
        super(BulkOfflineConversionGoal, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkOfflineConversionGoal._MAPPINGS)

