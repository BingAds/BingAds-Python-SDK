from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


class BulkLabel(_SingleRecordBulkEntity):
    """ Represents a label that can be read or written in a bulk file.

    This class exposes the :attr:`label` property that can be read and written as fields of the Keyword record in a bulk file.
    Properties of this class and of classes that it is derived from, correspond to fields of the Keyword record in a bulk file.
    For more information, see Keyword at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label=None, status=None):
        super(BulkLabel, self).__init__()
        self._label = label
        self._status = status

    @property
    def label(self):
        """ The Label Data Object of the Campaign Management Service.

        A subset of Label properties are available in the Ad Group record.
        """

        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def status(self):
        """ the status of bulk record
        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(
                c,
                'status',
                v if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: c.label.Id,
            csv_to_field=lambda c, v: setattr(
                c.label,
                'Id',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ColorCode,
            field_to_csv=lambda c: c.label.ColorCode,
            csv_to_field=lambda c, v: setattr(
                c.label,
                'ColorCode',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Description,
            field_to_csv=lambda c: c.label.Description,
            csv_to_field=lambda c, v: setattr(c.label, 'Description', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Label,
            field_to_csv=lambda c: c.label.Name,
            csv_to_field=lambda c, v: setattr(c.label, 'Name', v)
        ),
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._label, 'label')
        self.convert_to_values(row_values, BulkLabel._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._label = _CAMPAIGN_OBJECT_FACTORY_V13.create('Label')
        row_values.convert_to_entity(self, BulkLabel._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkLabel, self).read_additional_data(stream_reader)
