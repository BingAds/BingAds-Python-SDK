from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkDataExclusion(_SingleRecordBulkEntity):
    """ Represents an data exclusion.

    This class exposes the property :attr:`data_exclusion` that can be read and written as fields of the data exclusion record
    in a bulk file.

    For more information, see data exclusion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, data_exclusion=None):
        super(BulkDataExclusion, self).__init__()

        self._data_exclusion = data_exclusion

    @property
    def data_exclusion(self):
        """ The DataExclusion Data Object of the Campaign Management Service.

        A subset of DataExclusion properties are available in the Data Exclusion record.
        For more information, see Data Exclusion at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._data_exclusion

    @data_exclusion.setter
    def data_exclusion(self, data_exclusion):
        self._data_exclusion = data_exclusion

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.data_exclusion.Id),
            csv_to_field=lambda c, v: setattr(c.data_exclusion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DataExclusion,
            field_to_csv=lambda c: bulk_str(c.data_exclusion.Name),
            csv_to_field=lambda c, v: setattr(c.data_exclusion, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.StartDate,
            field_to_csv=lambda c: bulk_datetime_str2(c.data_exclusion.StartDate),
            csv_to_field=lambda c, v: setattr(c.data_exclusion, 'StartDate', parse_datetime2(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.EndDate,
            field_to_csv=lambda c: bulk_datetime_str2(c.data_exclusion.EndDate),
            csv_to_field=lambda c, v: setattr(c.data_exclusion, 'EndDate', parse_datetime2(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.Description,
            field_to_csv=lambda c: c.data_exclusion.Description,
            csv_to_field=lambda c, v: setattr(c.data_exclusion, 'Description', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CampaignType,
            field_to_csv=lambda c: field_to_csv_CampaignType(c.data_exclusion),
            csv_to_field=lambda c, v: csv_to_field_CampaignType(c.data_exclusion, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DeviceType,
            field_to_csv=lambda c: field_to_csv_DeviceType(c.data_exclusion),
            csv_to_field=lambda c, v: csv_to_field_DeviceType(c.data_exclusion, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CampaignAssociations,
            field_to_csv=lambda c: field_to_csv_CampaignAssociations(c.data_exclusion),
            csv_to_field=lambda c, v: csv_to_field_CampaignAssociations(c.data_exclusion, v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.data_exclusion = _CAMPAIGN_OBJECT_FACTORY_V13.create('DataExclusion')

        row_values.convert_to_entity(self, BulkDataExclusion._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._data_exclusion, 'DataExclusion')
        self.convert_to_values(row_values, BulkDataExclusion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkDataExclusion, self).read_additional_data(stream_reader)
