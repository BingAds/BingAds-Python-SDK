from bingads.exceptions import SdkException

class Report:
    
    def __init__(self):
        self._report_header = None
        self._report_iterator = None
        pass
    
    @property
    def report_name(self):
        return self._report_header.report_name

    @property
    def last_completed_available_date(self):
        return self._report_header.last_completed_available_date

    @property
    def record_count(self):
        return self._report_header.record_count

    @property
    def time_zone(self):
        return self._report_header.time_zone

#    @property
#    def report_filter(self):
#        return self._report_header.report_filter

    @property
    def potential_incomplete_data(self):
        return self._report_header.potential_incomplete_data

    @property
    def report_aggregation(self):
        return self._report_header.report_aggregation

    @property
    def report_time_start(self):
        return self._report_header.report_time_start
    
    @property
    def report_time_end(self):
        return self._report_header.report_time_end

    @property
    def report_columns(self):
        return self._report_header.report_columns

    @property
    def report_records(self):
        return self._report_iterator
    
    def close(self):
        pass


class InvalidReportFormatException(SdkException):

    def __init__(self, format):
        """ Initializes a new instance of this class with the specified error messages.

        :param format: The format of the report file to read.
        :type format: str
        """
        super(InvalidReportFormatException, self).__init__(str.format("Report format {0} is not supported.", format))

class InvalidReportContentException(SdkException):

    def __init__(self):
        super(InvalidReportContentException, self).__init__("Report content is invalid.")


class InvalidReportColumnException(SdkException):
    """ This exception is thrown if trying to retrieve inexistent column """

    def __init__(self, column_name):
        """ Initializes a new instance of this class with the specified error messages.

        :param column_name: The column name to be retrieved from the report.
        :type column_name: str
        """
        super(InvalidReportColumnException, self).__init__(str.format("Field: {0} does not exist in report.", column_name))