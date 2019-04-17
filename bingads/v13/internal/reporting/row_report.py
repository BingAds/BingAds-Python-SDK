from .row_report_header import _RowReportHeader
from .row_report_iterator import _ReportStreamReader, _RowReportIterator

from bingads.v13.reporting.report_contract import Report

class _RowReport(Report):
    
    def __init__(self, file, format = 'Csv'):
        self._stream_reader = _ReportStreamReader(file, format)
        self._report_header = _RowReportHeader(self._stream_reader)
        self._report_iterator = _RowReportIterator(self._stream_reader)
    
    def close(self):
        self._stream_reader.close()