from abc import ABCMeta, abstractmethod

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.bulk.entities.bulk_entity import BulkEntity
from bingads.v13.bulk.entities.bulk_error import BulkError
from bingads.v13.internal.extensions import *


class _SingleRecordBulkEntity(BulkEntity,metaclass=ABCMeta):
    def __init__(self):
        self._client_id = None
        self._last_modified_time = None
        self._errors = None

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        self._client_id = client_id

    @property
    def last_modified_time(self):
        return self._last_modified_time

    @property
    def errors(self):
        """ A list of :class:`BulkError` details in a separate bulk record that corresponds to the record of a :class:`.BulkEntity` derived instance.

        :rtype: list[BulkError] or None
        """
        return self._errors

    @property
    def has_errors(self):
        return True if self.errors is not None and self.errors else False

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.ClientId,
            field_to_csv=lambda c: c.client_id,
            csv_to_field=lambda c, v: setattr(c, '_client_id', v),
        ),
        _SimpleBulkMapping(
            header=_StringTable.LastModifiedTime,
            field_to_csv=lambda c: bulk_datetime_str(c.last_modified_time),
            csv_to_field=lambda c, v: setattr(
                c,
                '_last_modified_time',
                parse_datetime(v) if v else None),
        ),
    ]

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, _SingleRecordBulkEntity._MAPPINGS)
        self.process_mappings_from_row_values(row_values)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, _SingleRecordBulkEntity._MAPPINGS)
        self.process_mappings_to_row_values(row_values, exclude_readonly_data)

    def read_related_data_from_stream(self, stream_reader):
        self.read_additional_data(stream_reader)
        self._read_errors(stream_reader)

    def write_to_stream(self, row_writer, exclude_readonly_data):
        row_writer.write_object_row(self, exclude_readonly_data)
        if not exclude_readonly_data:
            self._write_errors(row_writer)
            self.write_additional_data(row_writer)

    def _write_errors(self, row_writer):
        if self.has_errors:
            for error in self.errors:
                row_writer.write_object_row(error)

    def write_additional_data(self, row_writer):
        pass

    @abstractmethod
    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        """ Process specific entity mappings to CSV values. Must be implemented by each entity.

        :param row_values: Row values.
        :type row_values: _RowValues
        :param exclude_readonly_data: excludeReadonlyData indicates whether readonly data should be written (such as errors, performance data etc.)
        :type exclude_readonly_data: bool
        """

        raise NotImplementedError()

    @abstractmethod
    def process_mappings_from_row_values(self, row_values):
        """ Process specific entity mappings from CSV values. Must be implemented by each entity.

        :param row_values:
        :type row_values: _RowValues
        """

        raise NotImplementedError()

    @abstractmethod
    def read_additional_data(self, stream_reader):
        pass

    def _read_errors(self, stream_reader):
        errors = []
        success, error = stream_reader.try_read(BulkError)
        while success:
            error.entity = self
            errors.append(error)
            success, error = stream_reader.try_read(BulkError)
        self._errors = errors

    def enclose_in_multiline_entity(self):
        return super(_SingleRecordBulkEntity, self).enclose_in_multiline_entity()

    @property
    def can_enclose_in_multiline_entity(self):
        return super(_SingleRecordBulkEntity, self).can_enclose_in_multiline_entity
