import tempfile
import uuid

from .bulk_operation import *
from .upload_parameters import *
from .file_reader import *
from .file_writer import *
from bingads.manifest import *
from bingads.service_client import ServiceClient
from bingads.authorization import *
from bingads.util import _TimeHelper
from bingads.exceptions import TimeoutException


class BulkServiceManager:
    """ Provides high level methods for uploading and downloading entities using the Bulk API functionality.

    Also provides methods for submitting upload or download operations.

    *Example:*

    :func:`download_file` will submit the download request to the bulk service,
    poll until the status is completed (or returns an error), and downloads the file locally.
    If instead you want to manage the low level details you would first call :func:`submit_download`,
    wait for the results file to be prepared using either :meth:`.BulkDownloadOperation.get_status`
    or :meth:`.BulkDownloadOperation.track`, and then download the file with the
    :meth:`.BulkOperation.download_result_file` method.
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
        self._service_client = ServiceClient('BulkService', authorization_data, environment, version='v10', **suds_options)
        self._authorization_data = authorization_data
        self._poll_interval_in_milliseconds = poll_interval_in_milliseconds
        self._working_directory = os.path.join(tempfile.gettempdir(), WORKING_NAME)
        if working_directory is not None:
            self._working_directory = working_directory
        # make sure the working directory exists or create it.
        if not os.path.exists(self._working_directory):
            os.makedirs(self._working_directory)
        self._suds_options = suds_options

    def download_file(self, download_parameters, progress=None):
        """ Downloads the specified Bulk entities to a local file.

        :param download_parameters: Determines various download parameters, for example where the file should be downloaded.
        :type download_parameters: DownloadParameters
        :param progress: (optional) Tracking the percent complete progress information for the bulk operation.
        :type progress: BulkOperationProgressInfo -> None
        :return: The downloaded local bulk file path.
        :rtype: str
        """

        start_timestamp = _TimeHelper.get_current_time_milliseconds()
        operation = self.submit_download(download_parameters._submit_download_parameter)
        try:
            operation.track(progress, download_parameters.timeout_in_milliseconds)
        except TimeoutException:
            raise BulkDownloadException("Bulk file download tracking status timeout.")
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

    def download_entities(self, download_parameters, progress=None):
        """ Downloads the specified Bulk entities.

        :param download_parameters: Determines various download parameters, for example where the file should be downloaded.
        :type download_parameters: DownloadParameters
        :param progress: (optional) Tracking the percent complete progress information for the bulk operation.
        :type progress: BulkOperationProgressInfo -> None
        :return: Bulk entity generator.
        :rtype: generator[BulkEntity]
        """

        result_file_path = self.download_file(download_parameters, progress)
        result_file_type = ResultFileType.full_download \
            if download_parameters.last_sync_time_in_utc is None \
            else ResultFileType.partial_download
        download_file_type = DownloadFileType.csv
        if download_parameters.file_type is not None:
            if download_parameters.file_type == 'Tsv':
                download_file_type = DownloadFileType.tsv
        with BulkFileReader(
            file_path=result_file_path,
            result_file_type=result_file_type,
            file_format=download_file_type,
        ) as reader:
            for entity in reader:
                yield entity

    def upload_file(self, file_upload_parameters, progress=None):
        """ Uploads the specified Bulk file.

        :param file_upload_parameters: Determines various upload parameters.
        :type file_upload_parameters: FileUploadParameters
        :param progress: (optional) Tracking the percent complete progress information for the bulk operation.
        :type progress: BulkOperationProgressInfo -> None
        :return: The download local bulk file path.
        :rtype: str
        """

        start_timestamp = _TimeHelper.get_current_time_milliseconds()
        file_upload_parameters._submit_upload_parameters.timeout_in_milliseconds = file_upload_parameters.timeout_in_milliseconds
        operation = self.submit_upload(file_upload_parameters._submit_upload_parameters)
        upload_operation_timeout = _TimeHelper.get_remaining_time_milliseconds_with_min_value(start_timestamp, file_upload_parameters.timeout_in_milliseconds)
        try:
            operation.track(progress, upload_operation_timeout)
        except TimeoutException:
            raise BulkUploadException("Bulk file upload tracking status timeout.")
        result_file_directory = self.working_directory
        if file_upload_parameters.result_file_directory is not None:
            result_file_directory = file_upload_parameters.result_file_directory
        download_result_file_timeout = _TimeHelper.get_remaining_time_milliseconds_with_min_value(start_timestamp, file_upload_parameters.timeout_in_milliseconds)
        result_file_path = operation.download_result_file(
            result_file_directory=result_file_directory,
            result_file_name=file_upload_parameters.result_file_name,
            decompress=file_upload_parameters.decompress_result_file,
            overwrite=file_upload_parameters.overwrite_result_file,
            timeout_in_milliseconds=download_result_file_timeout,
        )
        return result_file_path

    def upload_entities(self, entity_upload_parameters, progress=None):
        """ Uploads the specified Bulk entities.

        :param entity_upload_parameters: Determines various upload parameters, for example what entities to upload.
        :type entity_upload_parameters: EntityUploadParameters
        :param progress: (optional) Tracking the percent complete progress information for the bulk operation.
        :type progress: BulkOperationProgressInfo -> None
        :return: Bulk entity generator.
        :rtype: generator[BulkEntity]
        """

        tmp_file = path.join(self.working_directory, '{0}.csv'.format(uuid.uuid1()))
        with BulkFileWriter(tmp_file) as writer:
            for entity in entity_upload_parameters.entities:
                writer.write_entity(entity)
        file_upload_parameters = FileUploadParameters(
            upload_file_path=tmp_file,
            result_file_directory=entity_upload_parameters.result_file_directory,
            result_file_name=entity_upload_parameters.result_file_name,
            overwrite_result_file=entity_upload_parameters.overwrite_result_file,
            response_mode=entity_upload_parameters.response_mode,
            compress_upload_file=True,
        )
        result_file_path = self.upload_file(
            file_upload_parameters=file_upload_parameters,
            progress=progress,
        )
        with BulkFileReader(result_file_path, result_file_type=ResultFileType.upload) as reader:
            for entity in reader:
                yield entity

    def submit_download(self, submit_download_parameters):
        """ Submits a download request to the Bing Ads bulk service with the specified parameters.

        :param submit_download_parameters: Determines various download parameters, for example what entities to download.
        :type submit_download_parameters: SubmitDownloadParameters
        :return: The submitted download operation
        :rtype: BulkDownloadOperation
        """

        data_scope = None if submit_download_parameters.data_scope is None else ' '.join(
            submit_download_parameters.data_scope)
        download_file_type = submit_download_parameters.file_type
        entities = None if submit_download_parameters.entities is None else ' '.join(
            submit_download_parameters.entities)
        format_version = BULK_FORMAT_VERSION_4
        last_sync_time_in_utc = submit_download_parameters.last_sync_time_in_utc
        performance_stats_date_range = submit_download_parameters.performance_stats_date_range

        if submit_download_parameters.campaign_ids is None:
            response = self.service_client.DownloadCampaignsByAccountIds(
                AccountIds={'long': [self._authorization_data.account_id]},
                DataScope=data_scope,
                DownloadFileType=download_file_type,
                Entities=entities,
                FormatVersion=format_version,
                LastSyncTimeInUTC=last_sync_time_in_utc,
                PerformanceStatsDateRange=performance_stats_date_range,
            )
        else:
            response = self.service_client.DownloadCampaignsByCampaignIds(
                Campaigns={
                    'CampaignScope': [
                        {'CampaignId': campaign_id, 'ParentAccountId': self._authorization_data.account_id}
                        for campaign_id in submit_download_parameters.campaign_ids
                    ]
                },
                DataScope=data_scope,
                DownloadFileType=download_file_type,
                Entities=entities,
                FormatVersion=format_version,
                LastSyncTimeInUTC=last_sync_time_in_utc,
                PerformanceStatsDateRange=performance_stats_date_range,
            )
        operation = BulkDownloadOperation(
            request_id=response,
            authorization_data=self._authorization_data,
            poll_interval_in_milliseconds=self._poll_interval_in_milliseconds,
            environment=self._environment,
            **self.suds_options
        )
        return operation

    def submit_upload(self, submit_upload_parameters):
        """ Submits a request for a URL where a bulk upload file may be posted.

        :param submit_upload_parameters:
        :type submit_upload_parameters: SubmitUploadParameters
        :return: The submitted upload operation.
        :rtype: BulkUploadOperation
        """

        response = self.service_client.GetBulkUploadUrl(
            AccountId=self._authorization_data.account_id,
            ResponseMode=submit_upload_parameters.response_mode,
        )
        request_id = response.RequestId
        upload_url = response.UploadUrl

        self._upload_file_by_url(
            url=upload_url,
            upload_file_path=submit_upload_parameters.upload_file_path,
            compress_upload_file=submit_upload_parameters.compress_upload_file,
        )
        operation = BulkUploadOperation(
            request_id=request_id,
            authorization_data=self._authorization_data,
            poll_interval_in_milliseconds=self._poll_interval_in_milliseconds,
            environment=self._environment,
            **self.suds_options
        )
        return operation

    def _upload_file_by_url(self, url, upload_file_path, compress_upload_file, timeout_in_milliseconds=None):
        """ Upload bulk file specified in upload parameters to specified URL

        :param url: The upload target URL.
        :type url: str
        :param upload_file_path: The fully qualified local path of the upload file.
        :type upload_file_path: str
        :param compress_upload_file: whether the upload file should be compressed before uploading.
        :type compress_upload_file: bool
        """

        _, ext = path.splitext(upload_file_path)
        if compress_upload_file and ext != '.zip':
            should_compress = True
        else:
            should_compress = False

        try:
            if should_compress:
                name, ext = path.splitext(upload_file_path)
                zip_file_path = os.path.join(self.working_directory, '{0}_{1}.zip'.format(name, uuid.uuid1()))

                with contextlib.closing(zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)) as f:
                    f.write(upload_file_path)
                upload_file_path = zip_file_path
            headers = {
                'DeveloperToken': self._authorization_data.developer_token,
                'CustomerId': str(self._authorization_data.customer_id),
                'AccountId': str(self._authorization_data.account_id),
                'User-Agent': USER_AGENT,
            }
            self._authorization_data.authentication.enrich_headers(headers)

            with open(upload_file_path, 'rb') as f:
                name, ext = path.splitext(upload_file_path)

                filename = '{0}{1}'.format(uuid.uuid1(), ext)
                s = requests.Session()
                s.mount('https://', TlsHttpAdapter())
                timeout_seconds = None if timeout_in_milliseconds is None else timeout_in_milliseconds / 1000.0
                try:
                    r = s.post(url, files={'file': (filename, f)}, verify=True, headers=headers, timeout=timeout_seconds)
                except requests.Timeout as ex:
                    raise FileUploadException(ex)
                r.raise_for_status()
        except Exception as ex:
            raise ex
        finally:
            if should_compress:
                name, ext = path.splitext(upload_file_path)
                zip_file_path = name + '.zip'
                if path.exists(zip_file_path):
                    os.remove(zip_file_path)

    @property
    def service_client(self):
        """ The internal bulk service client.

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
