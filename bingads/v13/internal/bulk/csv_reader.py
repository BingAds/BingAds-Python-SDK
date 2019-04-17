import csv
import io
from six import PY2, PY3

class _CsvReader:

    def __init__(self, filename, delimiter, encoding='utf-8-sig'):
        self._filename = filename
        self._delimiter = delimiter
        self._encoding = encoding

        if delimiter == ',':
            self._dialect = csv.excel
        elif delimiter == '\t':
            self._dialect = csv.excel_tab
        else:
            raise ValueError('Do not support delimiter: {0}', delimiter)

        self._csv_file = io.open(self.filename, encoding=self.encoding)

        if PY3:
            self._csv_reader = csv.reader(self._csv_file, dialect=self._dialect)
        elif PY2:
            byte_lines = [line.encode('utf-8') for line in self._csv_file]
            self._csv_reader = csv.reader(byte_lines, dialect=self._dialect)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._csv_file.__exit__(exc_type, exc_value, traceback)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def close(self):
        self.__exit__(None, None, None)

    def next(self):
        if PY3:
            return next(self._csv_reader)
        elif PY2:
            row = next(self._csv_reader)
            return [unicode(cell, encoding='utf-8') for cell in row]

    @property
    def filename(self):
        return self._filename

    @property
    def delimiter(self):
        return self._delimiter

    @property
    def encoding(self):
        return self._encoding
