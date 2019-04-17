import os


class ReportingDownloadParameters:
    """ Describes the related parameters when downloading file from server.

    such as the file name and directory that you want to specify.
    """

    def __init__(self,
                 report_request=None,
                 result_file_directory=None,
                 result_file_name=None,
                 overwrite_result_file=False,
                 timeout_in_milliseconds=None):
        """
        :param report_request: the report request object, which derives from the base request report class
        :type report_request: ReportRequest
        :param result_file_directory: (optional) The directory where the file will be downloaded.
        :type result_file_directory: str
        :param result_file_name: (optional) The name of the download result file.
        :type result_file_name: str
        :param overwrite_result_file:
        :type overwrite_result_file: bool
        :param timeout_in_milliseconds: (optional) timeout for reporting download operations in milliseconds
        :type timeout_in_milliseconds: int
        :return:
        """

        self._report_request = report_request
        self._result_file_directory = result_file_directory
        self._result_file_name = result_file_name
        self._decompress_result_file = True
        if result_file_name is not None:
            _, ext = os.path.splitext(result_file_name)
            if ext == '.zip':
                self._decompress_result_file = False
        self._overwrite_result_file = overwrite_result_file
        self._timeout_in_milliseconds=timeout_in_milliseconds

    @property
    def result_file_directory(self):
        """ The directory where the reporting file will be downloaded.
        :rtype: str
        """

        return self._result_file_directory

    @property
    def result_file_name(self):
        """ The name of the download reporting file.
        :rtype: str
        """

        return self._result_file_name

    @property
    def overwrite_result_file(self):
        """ Whether the local result file should be overwritten if it already exists.
        :rtype: bool
        """

        return self._overwrite_result_file

    @result_file_directory.setter
    def result_file_directory(self, result_file_directory):
        self._result_file_directory = result_file_directory

    @result_file_name.setter
    def result_file_name(self, result_file_name):
        self._result_file_name = result_file_name

    @overwrite_result_file.setter
    def overwrite_result_file(self, overwrite):
        self._overwrite_result_file = overwrite

    @property
    def decompress_result_file(self):
        """ If need to decompress the result file after download.
        This property is determined by the result_file_name, by default will do decompression.
        if the result_file_name has the extension of '.zip' then do not do decompression.
        :rtype: bool
        """

        return self._decompress_result_file


    @property
    def report_request(self):
        """ The report request.
        :rtype: ReportRequest
        """

        return self._report_request


    @report_request.setter
    def report_request(self, value):
        self._report_request = value

    @property
    def timeout_in_milliseconds(self):
        return self._timeout_in_milliseconds

    @timeout_in_milliseconds.setter
    def timeout_in_milliseconds(self, value):
        self._timeout_in_milliseconds = value
