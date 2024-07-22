from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkSeasonalityAdjustment(_SingleRecordBulkEntity):
    """ Represents an seasonality adjustment.

    This class exposes the property :attr:`seasonality_adjustment` that can be read and written as fields of the seasonality adjustment record
    in a bulk file.

    For more information, see seasonality adjustment at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, seasonality_adjustment=None):
        super(BulkSeasonalityAdjustment, self).__init__()

        self._seasonality_adjustment = seasonality_adjustment

    @property
    def seasonality_adjustment(self):
        """ The SeasonalityAdjustment Data Object of the Campaign Management Service.

        A subset of SeasonalityAdjustment properties are available in the Seasonality Adjustment record.
        For more information, see Seasonality Adjustment at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._seasonality_adjustment

    @seasonality_adjustment.setter
    def seasonality_adjustment(self, seasonality_adjustment):
        self._seasonality_adjustment = seasonality_adjustment



    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.seasonality_adjustment.Id),
            csv_to_field=lambda c, v: setattr(c.seasonality_adjustment, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SeasonalityAdjustment,
            field_to_csv=lambda c: bulk_str(c.seasonality_adjustment.Name),
            csv_to_field=lambda c, v: setattr(c.seasonality_adjustment, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.StartDate,
            field_to_csv=lambda c: bulk_datetime_str2(c.seasonality_adjustment.StartDate),
            csv_to_field=lambda c, v: setattr(c.seasonality_adjustment, 'StartDate', parse_datetime2(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.EndDate,
            field_to_csv=lambda c: bulk_datetime_str2(c.seasonality_adjustment.EndDate),
            csv_to_field=lambda c, v: setattr(c.seasonality_adjustment, 'EndDate', parse_datetime2(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.Description,
            field_to_csv=lambda c: c.seasonality_adjustment.Description,
            csv_to_field=lambda c, v: setattr(c.seasonality_adjustment, 'Description', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CampaignType,
            field_to_csv=lambda c: field_to_csv_CampaignType(c.seasonality_adjustment),
            csv_to_field=lambda c, v: csv_to_field_CampaignType(c.seasonality_adjustment, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DeviceType,
            field_to_csv=lambda c: field_to_csv_DeviceType(c.seasonality_adjustment),
            csv_to_field=lambda c, v: csv_to_field_DeviceType(c.seasonality_adjustment, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdjustmentValue,
            field_to_csv=lambda c: c.seasonality_adjustment.AdjustmentPercentage,
            csv_to_field=lambda c, v: setattr(c.seasonality_adjustment, 'AdjustmentPercentage', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CampaignAssociations,
            field_to_csv=lambda c: field_to_csv_CampaignAssociations(c.seasonality_adjustment),
            csv_to_field=lambda c, v: csv_to_field_CampaignAssociations(c.seasonality_adjustment, v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.seasonality_adjustment = _CAMPAIGN_OBJECT_FACTORY_V13.create('SeasonalityAdjustment')

        row_values.convert_to_entity(self, BulkSeasonalityAdjustment._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._seasonality_adjustment, 'SeasonalityAdjustment')
        self.convert_to_values(row_values, BulkSeasonalityAdjustment._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkSeasonalityAdjustment, self).read_additional_data(stream_reader)
