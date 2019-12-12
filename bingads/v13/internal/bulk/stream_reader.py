from .bulk_object import _BulkObject
from .format_version import _FormatVersion
from .object_reader import _BulkFileObjectReader
from .record_reader import _BulkRecordReader
from bingads.internal.error_messages import _ErrorMessages


class _BulkStreamReader(_BulkRecordReader):
    """ Reads a bulk object and also its related data (for example corresponding errors) from the stream."""

    def __init__(self, file_path, file_type, encoding='utf-8-sig'):
        super(_BulkStreamReader, self).__init__(_BulkFileObjectReader(file_path=file_path, delimiter=',' if file_type == 'Csv' else '\t', encoding=encoding))
        
        self._file_path = file_path
        self._file_type = file_type
        self._encoding = encoding

        self._delimiter = ',' if self.file_type == 'Csv' else '\t'

    @property
    def file_path(self):
        return self._file_path

    @property
    def file_type(self):
        return self._file_type

    @property
    def delimiter(self):
        return self._delimiter

    @property
    def encoding(self):
        return self._encoding
