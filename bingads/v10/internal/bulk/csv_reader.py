import csv
import io
from six import PY2, PY3

import chardet


class _CsvReader:

    def __init__(self, filename, delimiter, encoding=None):
        self._filename = filename
        self._delimiter = delimiter
        self._encoding = encoding

        if delimiter == ',':
            self._dialect = csv.excel
        elif delimiter == '\t':
            self._dialect = csv.excel_tab
        else:
            raise ValueError('Do not support delimiter: {0}', delimiter)

        if self._encoding is None:
            self._encoding = self._detected_encoding

        self._csv_file = io.open(self.filename, encoding=self.encoding)

        if PY3:
            self._csv_reader = csv.reader(self._csv_file, dialect=self._dialect)
        elif PY2:
            byte_lines = [line.encode('utf-8') for line in self._csv_file]
            self._csv_reader = csv.reader(byte_lines, dialect=self._dialect)

    @property
    def _detected_encoding(self):
        buffer_size = 1024 * 1024
        with open(self._filename, mode='rb') as bfile:
            content = bfile.read(buffer_size)
            result = chardet.detect(content)
        return result['encoding']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._csv_file.__exit__(exc_type, exc_value, traceback)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self)

    def close(self):
        self.__exit__(None, None, None)

    def __next__(self):
        if PY3:
            return next(self._csv_reader)
        elif PY2:
            row = next(self._csv_reader)
            return [str(cell, encoding='utf-8') for cell in row]

    @property
    def filename(self):
        return self._filename

    @property
    def delimiter(self):
        return self._delimiter

    @property
    def encoding(self):
        return self._encoding
