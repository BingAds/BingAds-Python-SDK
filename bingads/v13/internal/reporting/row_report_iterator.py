import re
from .csv_reader import _CsvReader
from bingads.v13.reporting.report_contract import InvalidReportColumnException

class _RowReportRecord:

    def __init__(self, row_values):
        self._row_values = row_values

    def value(self, header):
        flag, result = self._row_values.try_get_value(header)
        if flag:
            return result
        raise InvalidReportColumnException(header)

    def int_value(self, header):
        try:
            return 0 if '--' == self.value(header) else int(self.value(header))
        except ValueError:
            return 0

    def float_value(self, header):
        try:
            return 0 if '--' == self.value(header) else float(self.value(header))
        except ValueError:
            return 0

class _RowReportRecordReader():
    """ Provides a method to read one row from report file"""

    def __init__(self, file_path, delimiter):
        self._column_mapping = None
        self._csv_reader = _CsvReader(file_path, delimiter)

    def read_next_header(self, parser):

        def remove_bom(unicode_str):
            unicode_bom = u'\N{ZERO WIDTH NO-BREAK SPACE}'
            if unicode_str and unicode_str[0] == unicode_bom:
                unicode_str = unicode_str[1:]
            return unicode_str
        try:
            fields =  [remove_bom(header) for header in next(self._csv_reader)] 

            if self.valid_header(fields) == False:
                return self.read_next_header(parser)
            
            valid_values = list(filter(lambda x: x is not None and len(x) > 0, [s.strip() for s in fields]))
            
            if len(valid_values) == 0:
                return False
            else:
                header = parser.parse_header(fields)
                if len(valid_values) > 1:
                    if header:
                        self._column_mapping = dict(zip(fields, range(0, len(fields))))
                        self.peek()
                    elif self.valid_record(fields):
                        # Exclude Column Header is set
                        self.next_object = _RowReportRecord(_RowValues(columns=fields, mappings=None))
                    return False
                return True
        except StopIteration:
            return False

    def valid_header(self, fields):
        if fields is None:
            return False
        
        valid_values = list(filter(lambda x: x is not None and len(x) > 0, [s.replace('-', '').strip() for s in fields]))
        return len(valid_values) > 0
        pass

    def read_next_object(self):
        if self.next_object != None:
            ret = self.next_object
            self.peek()
            return ret
        return None

    def peek(self):
        self.next_object = None
        try:
            row_values = self._read_next_row_values()
            self.next_object = _RowReportRecord(row_values)
        except StopIteration:
            pass

    def valid_record(self, values):
        if values is None:
            return False

        valid_values = list(filter(lambda x: x is not None and len(x) > 0, [s.replace('-', '').strip() for s in values]))

        if len(valid_values) == 0:
            return False
        if re.match(u'Total|\xa9\\d+ Microsoft Corporation. All rights reserved.*', valid_values[0]):
            return False

        return True
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._csv_reader.__exit__(exc_type, exc_value, traceback)

    def close(self):
        self._csv_reader.close()

    def _read_next_row_values(self):
        values = next(self._csv_reader)
        if self.valid_record(values) == False:
            return self._read_next_row_values()
        return _RowValues(columns=values, mappings=self._column_mapping)

    def _read_headers(self):
        pass

class _ReportStreamReader():

    def __init__(self, file_path, file_type):
        self._report_object_reader = _RowReportRecordReader(file_path, ',' if file_type == 'Csv' else '\t')

    def read_report_header(self, parser):
        while (self._report_object_reader.read_next_header(parser) == True):
            pass
        pass

    def read(self):
        peeked = self._report_object_reader.read_next_object()
        if peeked is not None:
            return peeked
        self._report_object_reader.close()
        return None

    def close(self):
        self._report_object_reader.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self._report_object_reader.__exit__(exc_type, exc_value, traceback)

class _RowReportIterator():
    
    def __init__(self, stream_reader):
        self._stream_reader = stream_reader

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stream_reader.__exit__(exc_type, exc_value, traceback)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        ret = self._stream_reader.read()
        if not ret:
            raise StopIteration()
        return ret

class _RowValues:
    def __init__(self, mappings=None, columns=None):
        self._mappings = mappings
        self._columns = columns

    def __getitem__(self, key):
        return self.columns[self._mappings[key]]

    def __setitem__(self, key, value):
        self.columns[self._mappings[key]] = value

    def __contains__(self, item):
        return item in self.mappings

    def __len__(self):
        return len(self.mappings)

    def __str__(self):
        return u'{' + u', '.join([u'{0}:{1}'.format(k, self.columns[v]) for (k, v) in self.mappings.items()]) + u'}'

    def try_get_value(self, header):
        if not self.mappings or header not in self.mappings:
            return False, None
        return True, self[header]

    def to_dict(self):
        return dict([(k, self.columns[v]) for (k, v) in self.mappings.items()])

    @property
    def mappings(self):
        return self._mappings

    @property
    def columns(self):
        return self._columns