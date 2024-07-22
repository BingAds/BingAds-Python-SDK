from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_conversion_goal import BulkConversionGoal
from decimal import Decimal

class BulkEventGoal(BulkConversionGoal):
    """ Represents an Event Goal that can be read or written in a bulk file.

    This class exposes the :attr:`event_goal` property that can be read and written as fields of the
    Event Goal record in a bulk file.

    For more information, see Event Goal at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 event_goal=None):
        super(BulkEventGoal, self).__init__(conversion_goal = event_goal)

    _MAPPINGS = [

        _SimpleBulkMapping(
            header=_StringTable.CategoryExpression,
            field_to_csv=lambda c: bulk_str(c.event_goal.CategoryExpression),
            csv_to_field=lambda c, v: setattr(c.event_goal, 'CategoryExpression', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CategoryOperator,
            field_to_csv=lambda c: bulk_str(c.event_goal.CategoryOperator),
            csv_to_field=lambda c, v: setattr(c.event_goal, 'CategoryOperator', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ActionExpression,
            field_to_csv=lambda c: bulk_str(c.event_goal.ActionExpression),
            csv_to_field=lambda c, v: setattr(c.event_goal, 'ActionExpression', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ActionOperator,
            field_to_csv=lambda c: bulk_str(c.event_goal.ActionOperator),
            csv_to_field=lambda c, v: setattr(c.event_goal, 'ActionOperator', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.LabelExpression,
            field_to_csv=lambda c: bulk_str(c.event_goal.LabelExpression),
            csv_to_field=lambda c, v: setattr(c.event_goal, 'LabelExpression', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.LabelOperator,
            field_to_csv=lambda c: bulk_str(c.event_goal.LabelOperator),
            csv_to_field=lambda c, v: setattr(c.event_goal, 'LabelOperator', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EventValue,
            field_to_csv=lambda c: bulk_str(c.event_goal.Value),
            csv_to_field=lambda c, v: setattr(c.event_goal, 'Value', Decimal(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EventValueOperator,
            field_to_csv=lambda c: bulk_str(c.event_goal.ValueOperator),
            csv_to_field=lambda c, v: setattr(c.event_goal, 'ValueOperator', v)
        ),
    ]

    @property
    def event_goal(self):
        """ Defines a Event Goal """

        return self._conversion_goal

    @event_goal.setter
    def event_goal(self, event_goal):
        self._conversion_goal = event_goal


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.event_goal, 'event_goal')
        super(BulkEventGoal, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkEventGoal._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.event_goal = _CAMPAIGN_OBJECT_FACTORY_V13.create('EventGoal')
        super(BulkEventGoal, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkEventGoal._MAPPINGS)

