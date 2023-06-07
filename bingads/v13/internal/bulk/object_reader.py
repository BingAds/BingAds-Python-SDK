import csv
from .bulk_object_factory import _BulkObjectFactory
from .row_values import _RowValues
from .csv_reader import _CsvReader

class _BulkObjectReader(object):
    """ Provides a method to read one row from bulk file and return the corresponding :class:`._BulkObject` """

    def __init__(self, _csv_reader):
        self._csv_reader = _csv_reader
        self._csv_reader.__enter__()
        headers = self._read_headers()
        self._column_mapping = dict(zip(headers, range(0, len(headers))))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._csv_reader.__exit__(exc_type, exc_value, traceback)

    def __iter__(self):
        return self

    def __next__(self):
        return self.read_next_bulk_object()

    def next(self):
        return self.__next__()

    def read_next_bulk_object(self):
        """ Reads the next csv row values, creates a new instance of the object and populates it with the row values.

        :return: next bulk object
        :rtype: _BulkObject
        """
        try:
            row_values = self._read_next_row_values()
        except StopIteration:
            return None
        bulk_object = _BulkObjectFactory.create_bulk_object(row_values)
        bulk_object.read_from_row_values(row_values)
        return bulk_object

    def close(self):
        self.__exit__(None, None, None)

    def _read_next_row_values(self):
        values = next(self._csv_reader)
        return _RowValues(columns=values, mappings=self._column_mapping)

    def _read_headers(self):
        # Need to strip BOM marker by hand, take care
        def remove_bom(unicode_str):
            unicode_bom = u'\N{ZERO WIDTH NO-BREAK SPACE}'
            if unicode_str and unicode_str[0] == unicode_bom:
                unicode_str = unicode_str[1:]
            return unicode_str

        headers = next(self._csv_reader)
        return [remove_bom(header) for header in headers]

class _BulkFileObjectReader(_BulkObjectReader):
    """ Provides a method to read one row from bulk file and return the corresponding :class:`._BulkObject` """

    def __init__(self, file_path, delimiter, encoding='utf-8-sig'):
        super(_BulkFileObjectReader, self).__init__(_CsvReader(filename=file_path, delimiter=delimiter, encoding=encoding))
        self._file_path = file_path
        self._delimiter = delimiter
        self._encoding = encoding


    @property
    def file_path(self):
        return self._file_path

    @property
    def delimiter(self):
        return self._delimiter

    @property
    def encoding(self):
        return self._encoding

class _CsvRowsReader:
    def __init__(self, csv_rows):
        self._csv_reader = csv.reader(csv_rows, dialect=csv.excel)
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()
    
    def next(self):
        return next(self._csv_reader)

class _BulkRowsObjectReader(_BulkObjectReader):
    """ Provides a method to read one row from bulk file and return the corresponding :class:`._BulkObject` """

    def __init__(self, csv_rows):
        super(_BulkRowsObjectReader, self).__init__(_CsvRowsReader(csv_rows))