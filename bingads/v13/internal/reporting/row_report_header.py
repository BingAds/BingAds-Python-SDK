import re
from bingads.v13.internal.extensions import *

class _RowReportHeader:

    def __init__(self, stream_reader):
        self._regex = re.compile(r'^(Report Name|Report Time|Report Aggregation|Report Filter|Time Zone|Rows|Last Completed Available Day|Last Completed Available Hour|Potential Incomplete Data): (.*)$')
        self._value_regex = re.compile(r'^(([1-9]\d*\.?\d*)|(0\.\d*[1-9]))%?$')
        self._stream_reader = stream_reader
        self._report_name = None
        self._report_time_start = None
        self._report_time_end = None
        self._report_aggregation = None
        self._time_zone = None
        self._row_number = None
        self._last_completed_available_date = None
        self._report_columns = None
        self._potential_incomplete_data = None
        self.read_header()

    def read_header(self):
        self._stream_reader.read_report_header(self)
    
    def parse_header(self, fields):
        valid_values = list(filter(lambda x: x is not None and len(x) > 0, [s.strip() for s in fields]))
        if len(valid_values) == 1 and ':' in fields[0]:
            self.parse_meta(fields[0])
            return True
        else:
            for s in fields:
                if self._value_regex.match(s):
                    return False
            self._report_columns = fields
            return True
    
    def parse_meta(self, header):
        res = self._regex.match(header)
        if res:
            if res.group(1) == 'Report Name':
                self._report_name = res.group(2)
            elif res.group(1) == 'Report Time':
                self.set_report_time(res.group(2))
            elif res.group(1) == 'Report Aggregation':
                self._report_aggregation = res.group(2)
            elif res.group(1) == 'Report Filter':
                self._report_filter = res.group(2)
            elif res.group(1) == 'Time Zone':
                self._time_zone = res.group(2)
            elif res.group(1) == 'Rows':
                self._row_number = res.group(2)
            elif res.group(1) == 'Last Completed Available Day':
                self._last_completed_available_date = res.group(2)
            elif res.group(1) == 'Potential Incomplete Data':
                self._potential_incomplete_data = parse_bool(res.group(2))
        pass

    def set_report_time(self, report_time):
        if report_time is None or report_time == '':
            return
        time_array = report_time.split(',')

        if len(time_array) == 1:
            self._report_time_start = datetime.strptime(time_array[0], '%m/%d/%Y') if time_array[0] else None
            self._report_time_end = datetime.strptime(time_array[0], '%m/%d/%Y') if time_array[0] else None
        elif len(time_array) == 2:
            self._report_time_start = datetime.strptime(time_array[0], '%m/%d/%Y') if time_array[0] else None
            self._report_time_end = datetime.strptime(time_array[1], '%m/%d/%Y') if time_array[1] else None

    @property
    def last_completed_available_date(self):
        if self._last_completed_available_date:
            str_time = self._last_completed_available_date
            if '(' in str_time:
                str_time = str_time[:str_time.rfind('(') - 1]

            try:
                return datetime.strptime(str_time, '%m/%d/%Y %I:%M:%S %p')
            except Exception:
                dt_tokens = str_time.split(' ')
                if len(dt_tokens) > 1:
                    return datetime.strptime(' '.join(dt_tokens[:2]), '%m/%d/%Y %H:%M:%S')
        return None
    
    @property
    def record_count(self):
        return int(self._row_number) if self._row_number else None
    
    
    @property
    def time_zone(self):
        return self._time_zone
    
    @property
    def potential_incomplete_data(self):
        return self._potential_incomplete_data
    
#    @property
#    def report_filter(self):
#        return self._report_filter
    
    @property
    def report_aggregation(self):
        return self._report_aggregation
    
    @property
    def report_name(self):
        return self._report_name
    
    @property
    def report_time_start(self):
        return self._report_time_start

    @property
    def report_time_end(self):
        return self._report_time_end

    @property
    def report_columns(self):
        return self._report_columns

