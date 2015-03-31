import csv
import codecs
from six import PY2, PY3


class _CsvWriter:
    def __init__(self, filename, delimiter):
        self._filename = filename
        self._delimiter = delimiter
        self._encoding = 'utf-8-sig'

        if delimiter == ',':
            self._dialect = csv.excel
        elif delimiter == '\t':
            self._dialect = csv.excel_tab
        else:
            raise ValueError('Do not support delimiter: {0}', delimiter)

        if PY3:
            self._csv_file = codecs.open(filename, mode='w', encoding=self._encoding)
        elif PY2:
            self._csv_file = open(filename, mode='wb')
            self._csv_file.write(codecs.BOM_UTF8)
        self._csv_writer = csv.writer(self._csv_file, dialect=self._dialect)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._csv_file.flush()
        self._csv_file.close()

    def close(self):
        self.__exit__(None, None, None)

    def writerow(self, row):
        if PY3:
            self._csv_writer.writerow(row)
        elif PY2:
            def unicode_to_str(value):
                if not isinstance(value, unicode):
                    return value
                return value.encode('utf-8')
            self._csv_writer.writerow([unicode_to_str(cell) for cell in row])

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    @property
    def filename(self):
        return self._filename

    @property
    def delimiter(self):
        return self._delimiter
