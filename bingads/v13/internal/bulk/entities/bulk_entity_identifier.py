from abc import ABCMeta, abstractproperty, abstractmethod

from bingads.v13.bulk.entities import BulkError
from bingads.v13.internal.bulk.bulk_object import _BulkObject


class _BulkEntityIdentifier(_BulkObject, metaclass=ABCMeta):

    @abstractproperty
    def is_delete_row(self):
        raise NotImplementedError()

    @abstractmethod
    def _create_entity_with_this_identifier(self):
        raise NotImplementedError()

    def write_to_stream(self, row_writer, exclude_readonly_data):
        row_writer.write_object_row(self)

    def read_related_data_from_stream(self, stream_reader):
        if self.is_delete_row:
            has_more_errors = True

            while has_more_errors:
                has_more_errors, error = stream_reader.try_read(BulkError)

    @property
    def can_enclose_in_multiline_entity(self):
        return True

    def enclose_in_multiline_entity(self):
        return self._create_entity_with_this_identifier()
