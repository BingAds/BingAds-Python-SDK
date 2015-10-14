class ReportingOperationStatus(object):
    """ Contains tracking details about the Report Request Status """

    def __init__(self,
                 status=None,
                 report_download_url=None):
        """ Initialize a new instance of this class.

        :param status: (optional) The download or upload status.
        :type status: str
        :param report_download_url: (optional) The report download Url.
        :type report_download_url: str
        """

        self._status = status
        self._report_download_url = report_download_url

    @property
    def status(self):
        """ The download status.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


    @property
    def report_download_url(self):
        """ The report download Url.
        :rtype: str
        """
        return self._report_download_url

    @report_download_url.setter
    def report_download_url(self, value):
        self._report_download_url = value
