from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


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
        self._adjustment_value = None
        self._adjustment_time = None
        self._adjustment_type = None
        self._adjustment_currency_code = None
        self._external_attribution_model = None
        self._external_attribution_credit = None

    @property
    def adjustment_value(self):
        return self._adjustment_value;

    @adjustment_value.setter
    def adjustment_value(self, value):
        self._adjustment_value = value

    @property
    def adjustment_time(self):
        return self._adjustment_time;

    @adjustment_time.setter
    def adjustment_time(self, value):
        self._adjustment_time = value

    @property
    def adjustment_type(self):
        return self._adjustment_type;

    @adjustment_type.setter
    def adjustment_type(self, value):
        self._adjustment_type = value

    @property
    def adjustment_currency_code(self):
        return self._adjustment_currency_code;

    @adjustment_currency_code.setter
    def adjustment_currency_code(self, value):
        self._adjustment_currency_code = value

    @property
    def external_attribution_model(self):
        return self._external_attribution_model;

    @external_attribution_model.setter
    def external_attribution_model(self, value):
        self._external_attribution_model = value

    @property
    def external_attribution_credit(self):
        return self._external_attribution_credit;

    @external_attribution_credit.setter
    def external_attribution_credit(self, value):
        self._external_attribution_credit = value

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
        _SimpleBulkMapping(
            header=_StringTable.AdjustmentValue,
            field_to_csv=lambda c: c.adjustment_value,
            csv_to_field=lambda c, v: setattr(
                c,
                'adjustment_value',
                float(v) if v else None
            )
        ),

        _SimpleBulkMapping(
            header=_StringTable.AdjustmentType,
            field_to_csv=lambda c: c.adjustment_type,
            csv_to_field=lambda c, v: setattr(
                c,
                'adjustment_type',
                v
            )
        ),

        _SimpleBulkMapping(
            header=_StringTable.AdjustmentCurrencyCode,
            field_to_csv=lambda c: c.adjustment_currency_code,
            csv_to_field=lambda c, v: setattr(
                c,
                'adjustment_currency_code',
                v
            )
        ),

        _SimpleBulkMapping(
            header=_StringTable.ExternalAttributionModel,
            field_to_csv=lambda c: c.external_attribution_model,
            csv_to_field=lambda c, v: setattr(
                c,
                'external_attribution_model',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ExternalAttributionCredit,
            field_to_csv=lambda c: c.external_attribution_credit,
            csv_to_field=lambda c, v: setattr(
                c,
                'external_attribution_credit',
                float(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdjustmentTime,
            field_to_csv=lambda c: bulk_datetime_str(c.adjustment_time),
            csv_to_field=lambda c, v: setattr(
                c,
                'adjustment_time',
                parse_datetime(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.HashedEmailAddress,
            field_to_csv=lambda c: c.offline_conversion.HashedEmailAddress,
            csv_to_field=lambda c, v: setattr(
                c.offline_conversion,
                'HashedEmailAddress',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.HashedPhoneNumber,
            field_to_csv=lambda c: c.offline_conversion.HashedPhoneNumber,
            csv_to_field=lambda c, v: setattr(
                c.offline_conversion,
                'HashedPhoneNumber',
                v
            )
        ),
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._offline_conversion, 'offline_conversion')
        self.convert_to_values(row_values, BulkOfflineConversion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._offline_conversion = _CAMPAIGN_OBJECT_FACTORY_V13.create('OfflineConversion')
        row_values.convert_to_entity(self, BulkOfflineConversion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkOfflineConversion, self).read_additional_data(stream_reader)
