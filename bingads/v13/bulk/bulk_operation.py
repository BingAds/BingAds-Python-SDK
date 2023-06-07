import time
import contextlib
import ssl
import requests
import zipfile
import os
import sys
import shutil


from .bulk_operation_status import *
from .bulk_operation_progress_info import *
from .exceptions import *
from bingads.util import _PollingBlocker, errorcode_of_exception, ratelimit_retry_duration, operation_errorcode_of_exception
from bingads.exceptions import *

from bingads.service_client import ServiceClient
from bingads.manifest import *


from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class TlsHttpAdapter(HTTPAdapter):
    """" Transport adapter that chooses the TLS protocols based on python versions. """

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_SSLv23
        )


class BulkOperation(object):
    """ The base class that can be derived to represent a bulk operation requested by a user.

    You can use either the :class:`.BulkDownloadOperation` or :class:`.BulkUploadOperation`
    derived class to poll for the operation status, and then download the results file when available.
    """

    def __init__(self,
                 request_id,
                 authorization_data,
                 poll_interval_in_milliseconds=5000,
                 environment='production',
                 tracking_id=None,
                 **suds_options):
        self._request_id = request_id
        self._service_client = ServiceClient('BulkService', 13, authorization_data, environment, **suds_options)
        self._authorization_data = authorization_data
        self._poll_interval_in_milliseconds = poll_interval_in_milliseconds
        self._final_status = None
        self.tracking_id=tracking_id

    def download_result_file(self, result_file_directory, result_file_name, decompress, overwrite, timeout_in_milliseconds=None):
        """ Download file with specified URL and download parameters.

        :param result_file_directory: The download result local directory name.
        :type result_file_directory: str
        :param result_file_name: The download result local file name.
        :type result_file_name: str | None
        :param decompress: Determines whether to decompress the ZIP file.
                            If set to true, the file will be decompressed after download.
                            The default value is false, in which case the downloaded file is not decompressed.
        :type decompress: bool
        :param overwrite: Indicates whether the result file should overwrite the existing file if any.
        :type overwrite: bool
        :param timeout_in_milliseconds: (optional) timeout for download result file in milliseconds
        :type timeout_in_milliseconds: int
        :return: The download file path.
        :rtype: str
        """

        if result_file_directory is None:
            raise ValueError('result_file_directory cannot be None.')

        url = self.final_status.result_file_url
        if result_file_name is None:
            result_file_name = self.request_id

        if decompress:
            name, ext = os.path.splitext(result_file_name)
            if ext == '.zip':
                raise ValueError("Result file can't be decompressed into a file with extension 'zip'."
                                 " Please change the extension of the result_file_name or pass decompress_result_file = false")
            zip_file_path = os.path.join(result_file_directory, name + '.zip')
            result_file_path = os.path.join(result_file_directory, result_file_name)
        else:
            result_file_path = os.path.join(result_file_directory, result_file_name)
            zip_file_path = result_file_path

        if os.path.exists(result_file_path) and overwrite is False:
            raise FileExistsError('Result file: {0} exists'.format(result_file_path))
            
        headers = {
            'User-Agent': USER_AGENT,
        }
        s = requests.Session()
        s.mount('https://', TlsHttpAdapter())
        timeout_seconds = None if timeout_in_milliseconds is None else timeout_in_milliseconds / 1000.0
        try:
            r = s.get(url, headers=headers, stream=True, verify=True, timeout=timeout_seconds)
        except requests.Timeout as ex:
            raise FileDownloadException(ex)
        r.raise_for_status()
        try:
            with open(zip_file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            if decompress:
                with contextlib.closing(zipfile.ZipFile(zip_file_path)) as compressed:
                    first = compressed.namelist()[0]
                    with open(result_file_path, 'wb') as f, compressed.open(first, 'r') as cc:
                        #f.write(compressed.read(first))
                        shutil.copyfileobj(cc, f)
        except Exception as ex:
            raise ex
        finally:
            if decompress and os.path.exists(zip_file_path):
                os.remove(zip_file_path)
        return result_file_path

    def track(self, percent_complete=None):
        raise NotImplementedError()

    def get_status(self):
        raise NotImplementedError()

    @property
    def request_id(self):
        """ The request identifier corresponding to the bulk upload or download, depending on the derived type.

        :rtype: str
        """

        return self._request_id

    @property
    def final_status(self):
        """ Gets the final status of the bulk operation or null if the operation is still running.

        :rtype: BulkOperationStatus
        """

        return self._final_status

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


class BulkDownloadOperation(BulkOperation):
    """ Represents a bulk download operation requested by a user.

    You can use this class to poll for the download status, and then download the file when available.

    *Example:*

    The :meth:`.BulkServiceManager.submit_download` method returns an instance of this class.
    If for any reason you do not want to wait for the file to be prepared for download,
    for example if your application quits unexpectedly or you have other tasks to process, you can
    use an instance of :class:`.BulkDownloadOperation` to download the file when it is available.
    """

    def __init__(self,
                 request_id,
                 authorization_data,
                 poll_interval_in_milliseconds=5000,
                 environment='production',
                 tracking_id=None,
                 **suds_options):
        super(BulkDownloadOperation, self).__init__(
            request_id=request_id,
            authorization_data=authorization_data,
            poll_interval_in_milliseconds=poll_interval_in_milliseconds,
            environment=environment,
            tracking_id=tracking_id,
            **suds_options
        )

    def track(self, progress=None, timeout_in_milliseconds=None):
        """ Runs until the bulk service has finished processing the download or upload request.

        :param progress: (optional) Tracking the percent complete progress information for the bulk operation.
        :type progress: BulkOperationProgressInfo -> None
        :return: The final BulkOperationStatus.
        :rtype: BulkOperationStatus
        """

        if self.final_status is not None:
            return self.final_status
        blocker = _PollingBlocker(self.poll_interval_in_milliseconds, timeout_in_milliseconds)
        blocker.wait()
        while True:
            status = self.get_status()
            percentage = int(status.percent_complete)
            if progress is not None:
                progress(BulkOperationProgressInfo(percentage))
            if status.status == 'InProgress':
                blocker.wait()
                continue
            if status.status != 'Completed':
                raise BulkException('Exceptions while bulk download.', status.errors)
            self._final_status = status
            return self._final_status

    def get_status(self):
        """ Track the detailed download status.

        :return: The status of bulk download operation.
        :rtype: BulkOperationStatus
        """

        if self.final_status is not None:
            return self.final_status
        response = self._get_status_with_retry(4)
        headers = self.service_client.get_response_header()
        self.tracking_id = headers['TrackingId'] if 'TrackingId' in headers else None
        status = BulkOperationStatus(
            status=response.RequestStatus,
            percent_complete=int(response.PercentComplete),
            result_file_url=response.ResultFileUrl,
            errors=None if response.Errors is None else [
                OperationError(
                    code=error.Code,
                    details=error.Details,
                    error_code=error.ErrorCode,
                    message=error.Message,
                ) for error in response.Errors.OperationError
            ]
        )
        if status.status == 'Completed' or \
                status.status == 'Failed' or \
                status.status == 'FailedFullSyncRequired':
            self._final_status = status
        return status

    def _get_status_with_retry(self, retry_times):
        while retry_times > 1:
            try:
                return self.service_client.GetBulkDownloadStatus(RequestId=self.request_id)
            except Exception as ex:
                retry_times -= 1
                if '117' == errorcode_of_exception(ex):
                    time.sleep(ratelimit_retry_duration[3 - retry_times])
                else:
                    time.sleep(1)
        return self.service_client.GetBulkDownloadStatus(RequestId=self.request_id)


class BulkUploadOperation(BulkOperation):
    """ Represents a bulk upload operation requested by a user.

    You can use this class to poll for the upload status, and then download the upload results file when available.

    *Example:*

    The :meth:`.BulkServiceManager.submit_upload` method returns an instance of this class.
    If for any reason you do not want to wait for the file to finish uploading,
    for example if your application quits unexpectedly or you have other tasks to process, you can
    use an instance of :class:`.BulkUploadOperation` to download the upload results file when it is available.
    """

    def __init__(self,
                 request_id,
                 authorization_data,
                 poll_interval_in_milliseconds=5000,
                 environment='production',
                 tracking_id=None,
                 **suds_options):
        super(BulkUploadOperation, self).__init__(
            request_id=request_id,
            authorization_data=authorization_data,
            poll_interval_in_milliseconds=poll_interval_in_milliseconds,
            environment=environment,
            tracking_id=tracking_id,
            **suds_options
        )

    def track(self, progress=None, timeout_in_milliseconds=None):
        """ Runs until the bulk service has finished processing the download or upload request.

        :param progress: (optional) Tracking the percent complete progress information for the bulk operation.
        :type progress: BulkOperationProgressInfo -> None
        :return: The final BulkOperationStatus.
        :rtype: BulkOperationStatus
        """

        if self.final_status is not None:
            return self.final_status
        blocker = _PollingBlocker(self.poll_interval_in_milliseconds, timeout_in_milliseconds)
        blocker.wait()
        while True:
            status = self.get_status()
            percentage = int(status.percent_complete)
            if progress is not None:
                progress(BulkOperationProgressInfo(percentage))
            if status.status == 'InProgress' or status.status == 'FileUploaded' or status.status == 'PendingFileUpload':
                blocker.wait()
                continue
            if status.status != 'Completed' and status.status != 'CompletedWithErrors':
                raise BulkException("Exceptions while bulk upload.", status.errors)
            self._final_status = status
            return self._final_status

    def get_status(self):
        """ Track the detailed upload status.

        :return: The status of bulk upload operation.
        :rtype: BulkOperationStatus
        """

        if self.final_status is not None:
            return self.final_status
        response = self._get_status_with_retry(4)
        headers = self.service_client.get_response_header()
        self.tracking_id = headers['TrackingId'] if 'TrackingId' in headers else None
        status = BulkOperationStatus(
            status=response.RequestStatus,
            percent_complete=int(response.PercentComplete),
            result_file_url=response.ResultFileUrl,
            errors=None if response.Errors is None else [
                OperationError(
                    code=error.Code,
                    details=error.Details,
                    error_code=error.ErrorCode,
                    message=error.Message,
                ) for error in response.Errors.OperationError
            ]
        )
        if status.status == 'Completed' or \
                status.status == 'CompletedWithErrors' or \
                status.status == 'Failed' or \
                status.status == 'Expired' or \
                status.status == 'Aborted':
            self._final_status = status
        return status

    def _get_status_with_retry(self, retry_times):
        while retry_times > 1:
            try:
                return self.service_client.GetBulkUploadStatus(RequestId=self.request_id)
            except Exception as ex:
                retry_times -= 1
                if '117' == errorcode_of_exception(ex):
                    time.sleep(ratelimit_retry_duration[3 - retry_times])
                else:
                    time.sleep(1)
        return self.service_client.GetBulkUploadStatus(RequestId=self.request_id)
