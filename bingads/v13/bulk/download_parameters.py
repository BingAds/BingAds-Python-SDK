import os

class DownloadParameters:
    """ Describes the related parameters when downloading file from server.

    such as the type of entities and data scope that you want to download.
    """

    def __init__(self,
                 result_file_directory=None,
                 result_file_name=None,
                 overwrite_result_file=False,
                 data_scope=None,
                 download_entities=None,
                 file_type='Csv',
                 campaign_ids=None,
                 last_sync_time_in_utc=None,
                 timeout_in_milliseconds=None):
        """ Initialize an instance of this class.

        :param result_file_directory: (optional) The directory where the file will be downloaded.
        :type result_file_directory: str
        :param result_file_name: (optional) The name of the download result file.
        :type result_file_name: str
        :param overwrite_result_file: (optional) Whether the local result file should be overwritten if it already exists, default is False.
        :type overwrite_result_file: bool
        :param data_scope: (optional) The scope or types of data to download.
                            For possible values, see DataScope Value Set at https://go.microsoft.com/fwlink/?linkid=846127.
        :type data_scope: list[str]
        :param download_entities: (optional) The type of entities to download.
                            For possible values, see BulkDownloadEntity Value Set at https://go.microsoft.com/fwlink/?linkid=846127.
        :type download_entities: list[str]
        :param file_type: (optional) The extension type of the downloaded file.
                            For possible values, see DownloadFileType Value Set at https://go.microsoft.com/fwlink/?linkid=846127.
        :type file_type: str
        :param campaign_ids: (optional) The campaigns to download.
                            You can specify a maximum of 1,000 campaigns. The campaigns that you specify must belong to the same account.
        :type campaign_ids: list[int]
        :param last_sync_time_in_utc: (optional) The last time that you requested a download.
                            The date and time is expressed in Coordinated Universal Time (UTC).
                            Typically, you request a full download the first time you call the operation by setting this element to null.
                            On all subsequent calls you set the last sync time to the time stamp of the previous download.
                            The download file contains the time stamp of the download in the SyncTime column of the Account record.
                            Use the time stamp to set LastSyncTimeInUTC the next time that you request a download.
                            If you specify the last sync time, only those entities that have changed (been updated or deleted)
                            since the specified date and time will be downloaded. However, if the campaign data has not been previously downloaded,
                            the operation performs a full download.
        :type last_sync_time_in_utc: datetime
        :param timeout_in_milliseconds: (optional) timeout for bulk download operations in milliseconds
        :type timeout_in_milliseconds: int
        """

        self._result_file_directory = result_file_directory
        self._result_file_name = result_file_name
        self._decompress_result_file = True
        if result_file_name is not None:
            _, ext = os.path.splitext(result_file_name)
            if ext == '.zip':
                self._decompress_result_file = False
        self._overwrite_result_file = overwrite_result_file
        self._submit_download_parameter = SubmitDownloadParameters(
            data_scope=data_scope,
            download_entities=download_entities,
            file_type=file_type,
            campaign_ids=campaign_ids,
            last_sync_time_in_utc=last_sync_time_in_utc,
        )
        self._timeout_in_milliseconds = timeout_in_milliseconds


    @property
    def result_file_directory(self):
        """ The directory where the file will be downloaded.

        :rtype: str
        """

        return self._result_file_directory

    @property
    def result_file_name(self):
        """ The name of the download result file.

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
    def data_scope(self):
        """ The scope or types of data to download.

        For possible values, see DataScope Value Set at https://go.microsoft.com/fwlink/?linkid=846127.

        :rtype: list[str]
        """

        return self._submit_download_parameter.data_scope

    @data_scope.setter
    def data_scope(self, value):
        self._submit_download_parameter.data_scope = value

    @property
    def download_entities(self):
        """ The type of entities to download.

        For possible values, see BulkDownloadEntity Value Set at https://go.microsoft.com/fwlink/?linkid=846127.

        :rtype: list[str]
        """

        return self._submit_download_parameter.download_entities

    @download_entities.setter
    def download_entities(self, value):
        self._submit_download_parameter.download_entities = value

    @property
    def file_type(self):
        """ The extension type of the downloaded file.

        For possible values, see DownloadFileType Value Set at https://go.microsoft.com/fwlink/?linkid=846127.

        :rtype: str
        """

        return self._submit_download_parameter.file_type

    @file_type.setter
    def file_type(self, value):
        self._submit_download_parameter.file_type = value

    @property
    def campaign_ids(self):
        """ The campaigns to download.

        You can specify a maximum of 1,000 campaigns. The campaigns that you specify must belong to the same account.

        :rtype: list[int]
        """

        return self._submit_download_parameter.campaign_ids

    @campaign_ids.setter
    def campaign_ids(self, value):
        self._submit_download_parameter.campaign_ids = value

    @property
    def last_sync_time_in_utc(self):
        """ The last time that you requested a download.

        The date and time is expressed in Coordinated Universal Time (UTC).
        Typically, you request a full download the first time you call the operation by setting this element to null.
        On all subsequent calls you set the last sync time to the time stamp of the previous download.
        The download file contains the time stamp of the download in the SyncTime column of the Account record.
        Use the time stamp to set LastSyncTimeInUTC the next time that you request a download.
        If you specify the last sync time, only those entities that have changed (been updated or deleted)
        since the specified date and time will be downloaded. However, if the campaign data has not been previously downloaded,
        the operation performs a full download.

        :rtype: datetime
        """

        return self._submit_download_parameter.last_sync_time_in_utc

    @last_sync_time_in_utc.setter
    def last_sync_time_in_utc(self, value):
        self._submit_download_parameter.last_sync_time_in_utc = value

    @property
    def timeout_in_milliseconds(self):
        return self._timeout_in_milliseconds

    @timeout_in_milliseconds.setter
    def timeout_in_milliseconds(self, value):
        self._timeout_in_milliseconds = value


class SubmitDownloadParameters(object):
    """ Describes the service request parameters such as the type of entities and data scope that you want to download. """

    def __init__(self,
                 data_scope=None,
                 download_entities=None,
                 file_type='Csv',
                 campaign_ids=None,
                 last_sync_time_in_utc=None):
        """ Initialize an object of this class.

        :param data_scope: (optional) The scope or types of data to download.
                            For possible values, see DataScope Value Set at https://go.microsoft.com/fwlink/?linkid=846127.
        :type data_scope: list[str]
        :param download_entities: (optional) The type of entities to download.
                            For possible values, see BulkDownloadEntity Value Set at https://go.microsoft.com/fwlink/?linkid=846127.
        :type download_entities: list[str]
        :param file_type: (optional) The extension type of the downloaded file.
                            For possible values, see DownloadFileType Value Set at https://go.microsoft.com/fwlink/?linkid=846127.
        :type file_type: str
        :param campaign_ids: (optional) The campaigns to download.
                            You can specify a maximum of 1,000 campaigns. The campaigns that you specify must belong to the same account.
        :type campaign_ids: list[int]
        :param last_sync_time_in_utc: (optional) The last time that you requested a download.
                            The date and time is expressed in Coordinated Universal Time (UTC).
                            Typically, you request a full download the first time you call the operation by setting this element to null.
                            On all subsequent calls you set the last sync time to the time stamp of the previous download.
                            The download file contains the time stamp of the download in the SyncTime column of the Account record.
                            Use the time stamp to set LastSyncTimeInUTC the next time that you request a download.
                            If you specify the last sync time, only those entities that have changed (been updated or deleted)
                            since the specified date and time will be downloaded. However, if the campaign data has not been previously downloaded,
                            the operation performs a full download.
        :type last_sync_time_in_utc: datetime
        """

        self._data_scope = data_scope
        self._download_entities = download_entities
        self._file_type = file_type
        self._campaign_ids = campaign_ids
        self._last_sync_time_in_utc = last_sync_time_in_utc

    @property
    def data_scope(self):
        """ The scope or types of data to download.

        For possible values, see DataScope Value Set at https://go.microsoft.com/fwlink/?linkid=846127.

        :rtype: list[str]
        """

        return self._data_scope

    @data_scope.setter
    def data_scope(self, value):
        self._data_scope = value

    @property
    def download_entities(self):
        """ The type of entities to download.

        For possible values, see BulkDownloadEntity Value Set at https://go.microsoft.com/fwlink/?linkid=846127.

        :rtype: list[str]
        """

        return self._download_entities

    @download_entities.setter
    def download_entities(self, value):
        self._download_entities = value

    @property
    def file_type(self):
        """ The extension type of the downloaded file.

        For possible values, see DownloadFileType Value Set at https://go.microsoft.com/fwlink/?linkid=846127.

        :rtype: str
        """

        return self._file_type

    @file_type.setter
    def file_type(self, value):
        self._file_type = value

    @property
    def campaign_ids(self):
        """ The campaigns to download.

        You can specify a maximum of 1,000 campaigns. The campaigns that you specify must belong to the same account.

        :rtype: list[int]
        """

        return self._campaign_ids

    @campaign_ids.setter
    def campaign_ids(self, value):
        self._campaign_ids = value

    @property
    def last_sync_time_in_utc(self):
        """ The last time that you requested a download.

        The date and time is expressed in Coordinated Universal Time (UTC).
        Typically, you request a full download the first time you call the operation by setting this element to null.
        On all subsequent calls you set the last sync time to the time stamp of the previous download.
        The download file contains the time stamp of the download in the SyncTime column of the Account record.
        Use the time stamp to set LastSyncTimeInUTC the next time that you request a download.
        If you specify the last sync time, only those entities that have changed (been updated or deleted)
        since the specified date and time will be downloaded. However, if the campaign data has not been previously downloaded,
        the operation performs a full download.

        :rtype: datetime
        """

        return self._last_sync_time_in_utc

    @last_sync_time_in_utc.setter
    def last_sync_time_in_utc(self, value):
        self._last_sync_time_in_utc = value
