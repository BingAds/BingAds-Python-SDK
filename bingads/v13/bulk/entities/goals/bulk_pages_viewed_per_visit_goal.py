from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_conversion_goal import BulkConversionGoal

class BulkPagesViewedPerVisitGoal(BulkConversionGoal):
    """ Represents an PagesViewedPerVisit Goal that can be read or written in a bulk file.

    This class exposes the :attr:`pages_viewed_per_visit_goal` property that can be read and written as fields of the
    PagesViewedPerVisit Goal record in a bulk file.

    For more information, see PagesViewedPerVisit Goal at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 pages_viewed_per_visit_goal=None):
        super(BulkPagesViewedPerVisitGoal, self).__init__(conversion_goal = pages_viewed_per_visit_goal)

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.MinimumPagesViewed,
            field_to_csv=lambda c: bulk_str(c.pages_viewed_per_visit_goal.MinimumPagesViewed),
            csv_to_field=lambda c, v: setattr(c.pages_viewed_per_visit_goal, 'MinimumPagesViewed', int(v) if v else None)
        ),
    ]

    @property
    def pages_viewed_per_visit_goal(self):
        """ Defines a PagesViewedPerVisit Goal """

        return self._conversion_goal

    @pages_viewed_per_visit_goal.setter
    def pages_viewed_per_visit_goal(self, pages_viewed_per_visit_goal):
        self._conversion_goal = pages_viewed_per_visit_goal


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.pages_viewed_per_visit_goal, 'pages_viewed_per_visit_goal')
        super(BulkPagesViewedPerVisitGoal, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkPagesViewedPerVisitGoal._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.pages_viewed_per_visit_goal = _CAMPAIGN_OBJECT_FACTORY_V13.create('PagesViewedPerVisitGoal')
        super(BulkPagesViewedPerVisitGoal, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkPagesViewedPerVisitGoal._MAPPINGS)

