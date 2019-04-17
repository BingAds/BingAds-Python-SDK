from .bulk_object import _BulkObject
from .string_table import _StringTable
from .mappings import _SimpleBulkMapping


class _FormatVersion(_BulkObject):
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Name,
            csv_to_field=lambda c, v: setattr(c, "_value", v)
        )
    ]

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, _FormatVersion._MAPPINGS)

    def write_to_row_values(self, row_values):
        super(_FormatVersion, self).write_to_row_values(row_values)

    def read_related_data_from_stream(self, stream_reader):
        super(_FormatVersion, self).read_related_data_from_stream(stream_reader)

    def write_to_stream(self, row_writer):
        super(_FormatVersion, self).write_to_stream(row_writer)

    @property
    def can_enclose_in_multiline_entity(self):
        return super(_FormatVersion, self).can_enclose_in_multiline_entity

    def enclose_in_multiline_entity(self):
        return super(_FormatVersion, self).enclose_in_multiline_entity()
