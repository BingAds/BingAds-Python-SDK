import tempfile

from openapi_client.models.reporting import *
from .reporting_operation import *
from .report_file_reader import *
from ...manifest import *
from ...service_client import ServiceClient
from ...exceptions import TimeoutException
from ...util import _TimeHelper

class ReportingServiceManager:
    """ Provides high level methods for downloading reporting files using the Reporting API functionality.

    Also provides methods for submitting download operations.

    *Example:*

    :func:`download_file` will submit the download request to the reporting service,
    poll until the status is completed (or returns an error), and downloads the file locally.
    If instead you want to manage the low level details you would first call :func:`submit_download`,
    wait for the results file to be prepared using either :meth:`.ReportingDownloadOperation.get_status`
    or :meth:`.ReportingDownloadOperation.track`, and then download the file with the
    :meth:`.ReportingOperation.download_result_file` method.
    """
    def __init__(self, authorization_data, poll_interval_in_milliseconds=5000, environment='production', working_directory=None, **suds_options):
        """ Initialize a new instance of this class.

        :param authorization_data: Represents a user who intends to access the corresponding customer and account.
        :type authorization_data: AuthorizationData
        :param environment: (optional) Represents which API environment to use, default is `production`, you can also pass `sandbox` in
        :type environment: str
        :param poll_interval_in_milliseconds: (optional) The time interval in milliseconds between two status polling attempts.
                                                         The default value is 15000 milliseconds.
        :type poll_interval_in_milliseconds: int
        :param working_directory: (optional)  Directory for storing temporary files needed for some operations
                                    (for example :func:`upload_entities` creates a temporary upload file).
        :param suds_options: The suds options need to pass to suds client
        """

        self._environment = environment
        self._service_client = ServiceClient('Reporting', 13, authorization_data, environment, **suds_options)
        self._authorization_data = authorization_data
        self._poll_interval_in_milliseconds = poll_interval_in_milliseconds
        self._working_directory = os.path.join(tempfile.gettempdir(), WORKING_NAME)
        if working_directory is not None:
            self._working_directory = working_directory
        # make sure the working directory exists or create it.
        if not os.path.exists(self._working_directory):
            os.makedirs(self._working_directory)
        self._suds_options = suds_options

    def download_report(self, download_parameters):
        """ Downloads the specified reporting to a local file and parse it with report_file_reader.

        :param download_parameters: Determines various download parameters, for example where the file should be downloaded.
        :type download_parameters: ReportingDownloadParameters
        :return: Report object parsed from the downloaded local reporting file path.
        :rtype: Report
        """
        report_file_path = self.download_file(download_parameters)
        if report_file_path:
            reader = ReportFileReader(report_file_path, download_parameters.report_request.Format)
            return reader.get_report()


    def download_file(self, download_parameters):
        """ Downloads the specified reporting to a local file.

        :param download_parameters: Determines various download parameters, for example where the file should be downloaded.
        :type download_parameters: ReportingDownloadParameters
        :return: The downloaded local reporting file path.
        :rtype: str
        """

        start_timestamp = _TimeHelper.get_current_time_milliseconds()
        operation = self.submit_download(download_parameters.report_request)
        try:
            operation.track(download_parameters.timeout_in_milliseconds)
        except TimeoutException:
            raise ReportingDownloadException("Reporting file download tracking status timeout.")
        result_file_directory = self.working_directory
        if download_parameters.result_file_directory is not None:
            result_file_directory = download_parameters.result_file_directory
        download_result_file_timeout = _TimeHelper.get_remaining_time_milliseconds_with_min_value(start_timestamp, download_parameters.timeout_in_milliseconds)
        result_file_path = operation.download_result_file(
            result_file_directory=result_file_directory,
            result_file_name=download_parameters.result_file_name,
            decompress=download_parameters.decompress_result_file,
            overwrite=download_parameters.overwrite_result_file,
            timeout_in_milliseconds=download_result_file_timeout,
        )
        return result_file_path

    def submit_download(self, report_request):
        """ Submits a download request to the Bing Ads reporting service with the specified request.

        :param report_request: Determines what kind of reporting file to download
        :type report_request: ReportRequest
        :return: The submitted download operation
        :rtype: ReportingDownloadOperation
        """
        self.normalize_request(report_request)
        submit_generate_report_request = SubmitGenerateReportRequest(
            ReportRequest=ReportRequest(report_request)
        )
        response = self.service_client.SubmitGenerateReport(submit_generate_report_request)
        headers = self.service_client.get_response_header()
        operation = ReportingDownloadOperation(
            request_id=response,
            authorization_data=self._authorization_data,
            poll_interval_in_milliseconds=self._poll_interval_in_milliseconds,
            environment=self._environment,
            tracking_id = headers['TrackingId'] if 'TrackingId' in headers else None,
            **self.suds_options
        )
        return operation

    def normalize_request(self, report_request):

        if report_request is None:
            return

        if not hasattr(report_request, 'Time'):
            return

        if hasattr(report_request.Time, 'ReportTimeZone') \
        and hasattr(report_request.Time.ReportTimeZone, 'value') \
        and report_request.Time.ReportTimeZone.value is None:
            report_request.Time.ReportTimeZone=None

        if hasattr(report_request.Time, 'PredefinedTime') \
        and hasattr(report_request.Time.PredefinedTime, 'value') \
        and report_request.Time.PredefinedTime.value is None:
            report_request.Time.PredefinedTime=None

    @property
    def service_client(self):
        """ The internal reporting service client.

        :rtype: ServiceClient
        """

        return self._service_client

    @property
    def poll_interval_in_milliseconds(self):
        """ The time interval in milliseconds between two status polling attempts.

        :rtype: int
        """

        return self._poll_interval_in_milliseconds

    @poll_interval_in_milliseconds.setter
    def poll_interval_in_milliseconds(self, poll_interval):
        self._poll_interval_in_milliseconds = poll_interval

    @property
    def working_directory(self):
        """ Directory for storing temporary files needed for some operations (for example :func:`upload_entities` creates a temporary upload file).

        :rtype: str
        """

        return self._working_directory

    @working_directory.setter
    def working_directory(self, value):
        self._working_directory = value

    @property
    def suds_options(self):
        """ suds option parameters

        :return: dict
        """
        return self._suds_options

    @suds_options.setter
    def suds_options(self, value):
        self._suds_options = value
