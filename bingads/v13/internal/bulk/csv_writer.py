import csv
import codecs


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

        self._csv_file = codecs.open(filename, mode='w', encoding=self._encoding)
        self._csv_writer = csv.writer(self._csv_file, dialect=self._dialect)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._csv_file.flush()
        self._csv_file.close()

    def close(self):
        self.__exit__(None, None, None)

    def writerow(self, row):
        self._csv_writer.writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    @property
    def filename(self):
        return self._filename

    @property
    def delimiter(self):
        return self._delimiter
