from bingads.v13.bulk.entities import *
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from decimal import Decimal

class BulkConversionGoal(_SingleRecordBulkEntity):
    """ Represents a ConversionGoal that can be read or written in a bulk file.

    This class exposes the :attr:`conversion_goal` property that can be read and written as fields of the
    ConversionGoal record in a bulk file.

    For more information, see ConversionGoal at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 conversion_goal=None):
        super(BulkConversionGoal, self).__init__()

        self._conversion_goal = conversion_goal

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.Status),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'Status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.Id),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.Name),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AttributionModelType,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.AttributionModelType),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'AttributionModelType', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ConversionWindowInMinutes,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.ConversionWindowInMinutes),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'ConversionWindowInMinutes', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CountType,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.CountType),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'CountType', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ExcludeFromBidding,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.ExcludeFromBidding),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'ExcludeFromBidding', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.GoalCategory,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.GoalCategory),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'GoalCategory', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.IsEnhancedConversionsEnabled,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.IsEnhancedConversionsEnabled),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'IsEnhancedConversionsEnabled', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.CurrencyCode,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.Revenue.CurrencyCode),
            csv_to_field=lambda c, v: setattr(c.conversion_goal.Revenue, 'CurrencyCode', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.RevenueValue,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.Revenue.Value),
            csv_to_field=lambda c, v: setattr(c.conversion_goal.Revenue, 'Value', Decimal(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.RevenueType,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.Revenue.Type),
            csv_to_field=lambda c, v: setattr(c.conversion_goal.Revenue, 'Type', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Scope,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.Scope),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'Scope', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TagId,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.TagId),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'TagId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ViewThroughConversionWindowInMinutes,
            field_to_csv=lambda c: bulk_str(c.conversion_goal.ViewThroughConversionWindowInMinutes),
            csv_to_field=lambda c, v: setattr(c.conversion_goal, 'ViewThroughConversionWindowInMinutes', int(v) if v else None)
        ),
    ]

    @property
    def conversion_goal(self):
        """ Defines a ConversionGoal """

        return self._conversion_goal

    @conversion_goal.setter
    def conversion_goal(self, conversion_goal):
        self._conversion_goal = conversion_goal

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkConversionGoal._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkConversionGoal._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkConversionGoal, self).read_additional_data(stream_reader)
