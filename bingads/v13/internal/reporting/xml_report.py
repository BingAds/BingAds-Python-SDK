import codecs
import xml.etree.cElementTree as et
import re
from bingads.v13.internal.extensions import *
from bingads.v13.reporting.report_contract import *

'''
Implement with context.next.xml.etree.cElementTree is far more faster than xml.etree.ElementTree with python 2.7.10
'''

schema=''
class _XmlReportRecord:
    def __init__(self, row):
        self._row_values = {}
        start = len(schema)
        for elem in row:
            self._row_values[elem.tag[start:]] = elem.attrib['value']

    def value(self, header):
        if header in self._row_values:
            return self._row_values[header]
        raise InvalidReportColumnException(header)

    def int_value(self, header):
        return 0 if '--' == self.value(header) else int(self.value(header))

    def double_value(self, header):
        return 0.0 if '--' == self.value(header) else float(self.value(header))

class _XmlReportIterator():
    
    def __init__(self, context, header):
        self._context = context
        self._header = header
        self._row_pattern = schema + 'Row'
        self._next_report_record = None
        self.move_to_next_row()
                 
    def move_to_next_row(self):
        for event, elem in self._context:
            if event == 'end' and self._row_pattern == elem.tag:
                self._next_report_record = _XmlReportRecord(elem)
                # self.try_set_report_columns(elem)
                elem.clear
                break
    def try_set_report_columns(self, element):
        if len(self._header._report_columns) == 0:
            start = len(schema)
            for e in element:
                self._header._report_columns.append(e.tag[start:])
        

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()
    
    def next(self):
        if self._next_report_record == None:
            raise StopIteration()
            
        ret = self._next_report_record
        self._next_report_record = None
        self.move_to_next_row()
        return ret


class _XmlReportHeader:

    def __init__(self, context):
        self._report_columns = []
        if context is not None:
            event, root = context.next()
            if event == 'start':
                m = re.compile(r'^(.*)Report').match(root.tag)
                if not m:
                    raise InvalidReportContentException()
                self.set_report_attribute(root.attrib.copy())
                global schema
                schema = m.group(1)
                root.clear()
            self.parse_column_names(context)
    
    def set_report_attribute(self, report_attr):
        self._report_attr = report_attr
        self.set_report_time()

    def set_report_time(self):
        self._report_time_start = None
        self._report_time_end = None
        if 'ReportTime' in self._report_attr:
            time_array = self._report_attr['ReportTime'].split(',')
            
            if len(time_array) == 1:
                self._report_time_start = datetime.strptime(time_array[0], '%m/%d/%Y') if time_array[0] else None
                self._report_time_end = datetime.strptime(time_array[0], '%m/%d/%Y') if time_array[0] else None
            elif len(time_array) == 2:
                self._report_time_start = datetime.strptime(time_array[0], '%m/%d/%Y') if time_array[0] else None
                self._report_time_end = datetime.strptime(time_array[0], '%m/%d/%Y') if time_array[1] else None
    
    def parse_column_names(self, context):
        for event, elem in context:
            if event == 'start' and schema + 'Column' == elem.tag:
                self._report_columns.append(elem.attrib['name'])
                elem.clear()
            elif  event == 'start' and 'Table' in elem.tag:
                # in case there is no columns names - ExcludeColumnHeader is set to true.
                break

    @property
    def last_completed_available_date(self):
        if 'LastCompletedAvailableDay'  in self._report_attr:
            str_time = self._report_attr['LastCompletedAvailableDay']
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
        return int(self._report_attr['Rows']) if 'Rows' in self._report_attr else None
    
    @property
    def time_zone(self):
        return self._report_attr['TimeZone'] if 'TimeZone' in self._report_attr else None
    
#    @property
#    def report_filter(self):
#        return None
    
    @property
    def report_aggregation(self):
        return self._report_attr['ReportAggregation'] if 'ReportAggregation' in self._report_attr else None
    
    @property
    def report_name(self):
        return self._report_attr['ReportName'] if 'ReportName' in self._report_attr else None
    
    @property
    def potential_incomplete_data(self):
        return parse_bool(self._report_attr['PotentialIncompleteData']) if 'PotentialIncompleteData' in self._report_attr else None

    @property
    def report_time_start(self):
        return self._report_time_start
    
    @property
    def report_time_end(self):
        return self._report_time_end
    
    @property
    def report_columns(self):
        return self._report_columns
    
        

class _XmlReport(Report):
    
    def __init__(self, file):
        context = et.iterparse(file, events=("start", "end"))
        self._report_header = _XmlReportHeader(context)
        self._report_iterator = _XmlReportIterator(context, self._report_header)
