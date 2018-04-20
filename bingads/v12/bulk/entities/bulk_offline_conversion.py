from __future__ import print_function
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V12
from bingads.v12.internal.bulk.string_table import _StringTable
from bingads.v12.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v12.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v12.internal.extensions import *


class BulkOfflineConversion(_SingleRecordBulkEntity):
    """ Represents an offline conversion that can be read or written in a bulk file.

    This class exposes the :attr:`offline_conversion` property that can be read and written as fields of the Keyword record in a bulk file.
    Properties of this class and of classes that it is derived from, correspond to fields of the Keyword record in a bulk file.
    For more information, see Keyword at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, offline_conversion=None):
        super(BulkOfflineConversion, self).__init__()
        self._offline_conversion = offline_conversion

    @property
    def offline_conversion(self):
        """ The offline conversion Data Object of the Campaign Management Service.

        """

        return self._offline_conversion

    @offline_conversion.setter
    def offline_conversion(self, value):
        self._offline_conversion = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.ConversionCurrencyCode,
            field_to_csv=lambda c: c.offline_conversion.ConversionCurrencyCode,
            csv_to_field=lambda c, v: setattr(
                c.offline_conversion,
                'ConversionCurrencyCode',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ConversionName,
            field_to_csv=lambda c: c.offline_conversion.ConversionName,
            csv_to_field=lambda c, v: setattr(
                c.offline_conversion,
                'ConversionName',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.MicrosoftClickId,
            field_to_csv=lambda c: c.offline_conversion.MicrosoftClickId,
            csv_to_field=lambda c, v: setattr(
                c.offline_conversion,
                'MicrosoftClickId',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ConversionValue,
            field_to_csv=lambda c: c.offline_conversion.ConversionValue,
            csv_to_field=lambda c, v: setattr(
                c.offline_conversion,
                'ConversionValue',
                float(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ConversionTime,
            field_to_csv=lambda c: bulk_datetime_str(c.offline_conversion.ConversionTime),
            csv_to_field=lambda c, v: setattr(
                c.offline_conversion,
                'ConversionTime',
                parse_datetime(v) if v else None
            )
        ),
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._offline_conversion, 'offline_conversion')
        self.convert_to_values(row_values, BulkOfflineConversion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._offline_conversion = _CAMPAIGN_OBJECT_FACTORY_V12.create('OfflineConversion')
        row_values.convert_to_entity(self, BulkOfflineConversion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkOfflineConversion, self).read_additional_data(stream_reader)
