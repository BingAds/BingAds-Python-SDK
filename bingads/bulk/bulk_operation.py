import time
import contextlib
import ssl
import requests
import zipfile
import os
import six

from .bulk_operation_status import *
from .bulk_operation_progress_info import *
from .exceptions import *

from ..service_client import ServiceClient
from ..manifest import *

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class Ssl3HttpAdapter(HTTPAdapter):
    """" Transport adapter" that allows us to use SSLv3. """

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_SSLv3,
        )


class BulkOperation(object):
    """ The base class that can be derived to represent a bulk operation requested by a user.

    You can use either the :class:`.BulkDownloadOperation` or :class:`.BulkUploadOperation`
    derived class to poll for the operation status, and then download the results file when available.
    """

    def __init__(self,
                 request_id,
                 authorization_data,
                 poll_interval_in_milliseconds=15000,
                 environment='production', ):
        self._request_id = request_id
        self._service_client = ServiceClient('BulkService', authorization_data, environment)
        self._authorization_data = authorization_data
        self._poll_interval_in_milliseconds = poll_interval_in_milliseconds
        self._final_status = None

    def download_result_file(self, result_file_directory, result_file_name, decompress, overwrite):
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
            if six.PY3:
                raise FileExistsError('Result file: {0} exists'.format(result_file_path))
            else:
                raise OSError('Result file: {0} exists'.format(result_file_path))
        headers = {
            'User-Agent': USER_AGENT,
        }
        s = requests.Session()
        s.mount('https://', Ssl3HttpAdapter())
        r = s.get(url, headers=headers, stream=True, verify=True)
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
                    with open(result_file_path, 'wb') as f:
                        f.write(compressed.read(first))
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
                 poll_interval_in_milliseconds=15000,
                 environment='production', ):
        super(BulkDownloadOperation, self).__init__(
            request_id=request_id,
            authorization_data=authorization_data,
            poll_interval_in_milliseconds=poll_interval_in_milliseconds,
            environment=environment,
        )

    def track(self, progress=None):
        """ Runs until the bulk service has finished processing the download or upload request.

        :param progress: (optional) Tracking the percent complete progress information for the bulk operation.
        :type progress: BulkOperationProgressInfo -> None
        :return: The final BulkOperationStatus.
        :rtype: BulkOperationStatus
        """

        if self.final_status is not None:
            return self.final_status
        blocker = _PollingBlocker(self.poll_interval_in_milliseconds)
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
        response = self.service_client.GetDetailedBulkDownloadStatus(RequestId=self.request_id)
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
                 poll_interval_in_milliseconds=15000,
                 environment='production', ):
        super(BulkUploadOperation, self).__init__(
            request_id=request_id,
            authorization_data=authorization_data,
            poll_interval_in_milliseconds=poll_interval_in_milliseconds,
            environment=environment,
        )

    def track(self, progress=None):
        """ Runs until the bulk service has finished processing the download or upload request.

        :param progress: (optional) Tracking the percent complete progress information for the bulk operation.
        :type progress: BulkOperationProgressInfo -> None
        :return: The final BulkOperationStatus.
        :rtype: BulkOperationStatus
        """

        if self.final_status is not None:
            return self.final_status
        blocker = _PollingBlocker(self.poll_interval_in_milliseconds)
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
        response = self.service_client.GetDetailedBulkUploadStatus(RequestId=self.request_id)
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


class _PollingBlocker(object):

    INITIAL_STATUS_CHECK_INTERVAL_IN_MS = 1000

    NUMBER_OF_INITIAL_STATUS_CHECKS = 5

    def __init__(self, poll_interval_in_milliseconds):
        self._poll_interval_in_milliseconds = poll_interval_in_milliseconds
        self._status_update_count = 0

    def wait(self):
        self._status_update_count += 1
        if self._status_update_count >= _PollingBlocker.NUMBER_OF_INITIAL_STATUS_CHECKS:
            time.sleep(self._poll_interval_in_milliseconds / 1000.0)
        else:
            time.sleep(_PollingBlocker.INITIAL_STATUS_CHECK_INTERVAL_IN_MS / 1000.0)
