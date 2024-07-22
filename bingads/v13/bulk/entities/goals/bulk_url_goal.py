from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_conversion_goal import BulkConversionGoal

class BulkUrlGoal(BulkConversionGoal):
    """ Represents an Url Goal that can be read or written in a bulk file.

    This class exposes the :attr:`url_goal` property that can be read and written as fields of the
    Url Goal record in a bulk file.

    For more information, see Url Goal at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 url_goal=None):
        super(BulkUrlGoal, self).__init__(conversion_goal = url_goal)

    _MAPPINGS = [

        _SimpleBulkMapping(
            header=_StringTable.UrlExpression,
            field_to_csv=lambda c: bulk_str(c.url_goal.UrlExpression),
            csv_to_field=lambda c, v: setattr(c.url_goal, 'UrlExpression', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.UrlOperator,
            field_to_csv=lambda c: bulk_str(c.url_goal.UrlOperator),
            csv_to_field=lambda c, v: setattr(c.url_goal, 'UrlOperator', v)
        ),

    ]

    @property
    def url_goal(self):
        """ Defines a Url Goal """

        return self._conversion_goal

    @url_goal.setter
    def url_goal(self, url_goal):
        self._conversion_goal = url_goal


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.url_goal, 'url_goal')
        super(BulkUrlGoal, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkUrlGoal._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.url_goal = _CAMPAIGN_OBJECT_FACTORY_V13.create('UrlGoal')
        super(BulkUrlGoal, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkUrlGoal._MAPPINGS)

