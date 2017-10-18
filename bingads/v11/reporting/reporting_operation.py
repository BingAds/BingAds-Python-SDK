import time
import contextlib
import ssl
import requests
import zipfile
import os
import six
import sys
imoprt shutil

from .reporting_operation_status import *
from .exceptions import *
from bingads.util import _PollingBlocker
from bingads.exceptions import *

from ...service_client import ServiceClient
from ...manifest import *

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class TlsHttpAdapter(HTTPAdapter):
    """" Transport adapter that chooses the TLS protocols based on python versions. """

    def init_poolmanager(self, connections, maxsize, block=False):
        ssl_version = ssl.PROTOCOL_TLSv1 if sys.version_info < (2, 7, 9) or sys.version_info[0:2] == (3, 3) \
                                         else ssl.PROTOCOL_SSLv23
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl_version
        )


class ReportingDownloadOperation(object):
    """ Represents a reporting download operation requested by a user.

    You can use this class to poll for the download status, and then download the file when available.

    *Example:*

    The :meth:`.ReportingServiceManager.submit_download` method returns an instance of this class.
    If for any reason you do not want to wait for the file to be prepared for download,
    for example if your application quits unexpectedly or you have other tasks to process, you can
    use an instance of :class:`.ReportingDownloadOperation` to download the file when it is available.
    """

    def __init__(self,
                 request_id,
                 authorization_data,
                 poll_interval_in_milliseconds=5000,
                 environment='production',
                 **suds_options):
        self._request_id = request_id
        self._service_client = ServiceClient('ReportingService', authorization_data, environment, 11, **suds_options)
        self._authorization_data = authorization_data
        self._poll_interval_in_milliseconds = poll_interval_in_milliseconds
        self._final_status = None

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
        :return: The download file path.
        :rtype: str
        :param timeout_in_milliseconds: (optional) timeout for download result file in milliseconds
        :type timeout_in_milliseconds: int
        """

        if result_file_directory is None:
            raise ValueError('result_file_directory cannot be None.')

        url = self.final_status.report_download_url

        if url is None or url == '':
            return None

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
                        shutil.copyfileobj(cc, f)
        except Exception as ex:
            raise ex
        finally:
            if decompress and os.path.exists(zip_file_path):
                os.remove(zip_file_path)
        return result_file_path

    def track(self, timeout_in_milliseconds=None):
        """ Runs until the reporting service has finished processing the download or upload request.

        :param timeout_in_milliseconds: (optional) timeout for tracking reporting download operation
        :type timeout_in_milliseconds: int
        :return: The final ReportingOperationStatus.
        :rtype: ReportingOperationStatus
        """

        if self.final_status is not None:
            return self.final_status
        blocker = _PollingBlocker(self.poll_interval_in_milliseconds, timeout_in_milliseconds)
        blocker.wait()
        while True:
            status = self.get_status()
            if status.status == 'Pending':
                blocker.wait()
                continue
            if status.status != 'Success':
                raise ReportingException('Exceptions while reporting download.', status.status)
            self._final_status = status
            return self._final_status

    def get_status(self):
        """ Track the detailed download status.

        :return: The status of reporting download operation.
        :rtype: ReportingOperationStatus
        """
        if self.final_status is not None:
            return self.final_status
        response = self._get_status_with_retry(3)
        status = ReportingOperationStatus(
            status=response.Status,
            report_download_url=response.ReportDownloadUrl
            )
        if status.status == 'Success' or \
                status.status == 'Error':
            self._final_status = status
        return status

    def _get_status_with_retry(self, retry_times):
        while retry_times > 1:
            try:
                return self.service_client.PollGenerateReport(self.request_id)
            except Exception:
                retry_times -= 1
                time.sleep(1000)
        return self.service_client.PollGenerateReport(self.request_id)

    @property
    def request_id(self):
        """ The request identifier corresponding to the reporting download, depending on the derived type.

        :rtype: str
        """

        return self._request_id

    @property
    def final_status(self):
        """ Gets the final status of the reporting operation or null if the operation is still running.

        :rtype: ReportingOperationStatus
        """

        return self._final_status

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
