from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


class BulkOnlineConversionAdjustment(_SingleRecordBulkEntity):
    """ Represents an online conversion adjustment that can be read or written in a bulk file.

    This class exposes the :attr:`online_conversion_adjustment` property that can be read and written as fields of the Keyword record in a bulk file.
    Properties of this class and of classes that it is derived from, correspond to fields of the Keyword record in a bulk file.
    For more information, see Keyword at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, online_conversion_adjustment=None):
        super(BulkOnlineConversionAdjustment, self).__init__()
        self._online_conversion_adjustment = online_conversion_adjustment

    @property
    def online_conversion_adjustment(self):
        """ The online conversion adjustment Data Object of the Campaign Management Service.

        """

        return self._online_conversion_adjustment

    @online_conversion_adjustment.setter
    def online_conversion_adjustment(self, value):
        self._online_conversion_adjustment = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.TransactionId,
            field_to_csv=lambda c: c.online_conversion_adjustment.TransactionId,
            csv_to_field=lambda c, v: setattr(
                c.online_conversion_adjustment,
                'TransactionId',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ConversionName,
            field_to_csv=lambda c: c.online_conversion_adjustment.ConversionName,
            csv_to_field=lambda c, v: setattr(
                c.online_conversion_adjustment,
                'ConversionName',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdjustmentType,
            field_to_csv=lambda c: c.online_conversion_adjustment.AdjustmentType,
            csv_to_field=lambda c, v: setattr(
                c.online_conversion_adjustment,
                'AdjustmentType',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdjustmentValue,
            field_to_csv=lambda c: c.online_conversion_adjustment.AdjustmentValue,
            csv_to_field=lambda c, v: setattr(
                c.online_conversion_adjustment,
                'AdjustmentValue',
                float(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdjustmentTime,
            field_to_csv=lambda c: bulk_datetime_str(c.online_conversion_adjustment.AdjustmentTime),
            csv_to_field=lambda c, v: setattr(
                c.online_conversion_adjustment,
                'AdjustmentTime',
                parse_datetime(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdjustmentCurrencyCode,
            field_to_csv=lambda c: c.online_conversion_adjustment.AdjustmentCurrencyCode,
            csv_to_field=lambda c, v: setattr(
                c.online_conversion_adjustment,
                'AdjustmentCurrencyCode',
                v
            )
        ),
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._online_conversion_adjustment, 'online_conversion_adjustment')
        self.convert_to_values(row_values, BulkOnlineConversionAdjustment._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._online_conversion_adjustment = _CAMPAIGN_OBJECT_FACTORY_V13.create('OnlineConversionAdjustment')
        row_values.convert_to_entity(self, BulkOnlineConversionAdjustment._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkOnlineConversionAdjustment, self).read_additional_data(stream_reader)
