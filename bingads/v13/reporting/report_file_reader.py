from bingads.v13.internal.reporting.row_report import _RowReport
from bingads.v13.internal.reporting.xml_report import _XmlReport
from .report_contract import InvalidReportFormatException

class ReportFileReader:
    def __init__(self, file_path, format):
        if format is None:
            return
        self._file_path = file_path
        lower = format.lower()
        if lower == 'csv':
            self._report = _RowReport(file_path, format = 'Csv')
        elif lower == 'tsv':
            self._report = _RowReport(file_path, format = 'Tsv')
        elif lower == 'xml':
            self._report = _XmlReport(file_path)
        else:
            raise InvalidReportFormatException(format)

    def get_report(self):
        return self._report
    
    @property
    def file_path(self):
        """ The path of the bulk file to read.

        :rtype: str
        """

        return self._file_path
    
    def close(self):
        self._report.close()
        self._report = None