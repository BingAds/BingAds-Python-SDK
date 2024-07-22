from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_conversion_goal import BulkConversionGoal

class BulkDurationGoal(BulkConversionGoal):
    """ Represents an Duration Goal that can be read or written in a bulk file.

    This class exposes the :attr:`duration_goal` property that can be read and written as fields of the
    Duration Goal record in a bulk file.

    For more information, see Duration Goal at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 duration_goal=None):
        super(BulkDurationGoal, self).__init__(conversion_goal = duration_goal)

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.MinimumDurationInSecond,
            field_to_csv=lambda c: bulk_str(c.duration_goal.MinimumDurationInSeconds),
            csv_to_field=lambda c, v: setattr(c.duration_goal, 'MinimumDurationInSeconds', int(v) if v else None)
        ),
    ]

    @property
    def duration_goal(self):
        """ Defines a Duration Goal """

        return self._conversion_goal

    @duration_goal.setter
    def duration_goal(self, duration_goal):
        self._conversion_goal = duration_goal


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.duration_goal, 'duration_goal')
        super(BulkDurationGoal, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkDurationGoal._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.duration_goal = _CAMPAIGN_OBJECT_FACTORY_V13.create('DurationGoal')
        super(BulkDurationGoal, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkDurationGoal._MAPPINGS)

