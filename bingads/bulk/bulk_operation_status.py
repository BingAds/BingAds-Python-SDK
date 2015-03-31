class BulkOperationStatus(object):
    """ Contains tracking details about the results and status of the corresponding :class:`.BulkDownloadOperation` or :class:`.BulkUploadOperation`. """

    def __init__(self,
                 status=None,
                 percent_complete=None,
                 result_file_url=None,
                 errors=None):
        """ Initialize a new instance of this class.

        :param status: (optional) The download or upload status.
        :type status: str
        :param percent_complete: (optional) Percent complete progress information for the bulk operation.
        :type percent_complete: int
        :param result_file_url: (optional) The download or upload result file Url.
        :type result_file_url: str
        :param errors: (optional) The list of errors associated with the operation.
        :type errors: list[OperationError]
        """

        self._status = status
        self._percent_complete = percent_complete
        self._result_file_url = result_file_url
        self._errors = errors

    @property
    def status(self):
        """ The download or upload status.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def percent_complete(self):
        """ Percent complete progress information for the bulk operation.

        :rtype: int
        """

        return self._percent_complete

    @percent_complete.setter
    def percent_complete(self, value):
        self._percent_complete = value

    @property
    def result_file_url(self):
        """ The download or upload result file Url.

        :rtype: str
        """

        return self._result_file_url

    @result_file_url.setter
    def result_file_url(self, value):
        self._result_file_url = value

    @property
    def errors(self):
        """ The list of errors associated with the operation.

        :rtype: list[OperationError]
        """

        return self._errors

    @errors.setter
    def errors(self, value):
        self._errors = value
