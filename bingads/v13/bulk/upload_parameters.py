from os import path


class FileUploadParameters:
    """ Describes the available parameters when submitting a file for upload, such as the path of the upload result file. """

    def __init__(self,
                 upload_file_path,
                 result_file_directory=None,
                 result_file_name=None,
                 overwrite_result_file=False,
                 compress_upload_file=True,
                 response_mode='ErrorsAndResults',
                 timeout_in_milliseconds=None, 
                 rename_upload_file_to_match_request_id = True):
        """ Initialize a new instance of this class.

        :param result_file_directory: The directory where the file will be downloaded.
        :type result_file_directory: str
        :param result_file_name: The name of the download result file.
        :type result_file_name: str
        :param overwrite_result_file: (optional) Whether the local result file should be overwritten if it already exists, default is False.
        :type overwrite_result_file: bool
        :param upload_file_path: The fully qualified local path of the upload file.
        :type upload_file_path: str
        :param compress_upload_file: (optional) Determines whether the upload file should be compressed before uploading. The default value is True.
        :type compress_upload_file: bool
        :param response_mode: (optional) Determines whether the bulk service should return upload errors with the corresponding entity data.
                                If not specified, this property is set by default to ErrorsAndResults.
        :type response_mode: str
        :param timeout_in_milliseconds: (optional) timeout for bulk upload operations in milliseconds
        :type timeout_in_milliseconds: int
        """

        self._result_file_directory = result_file_directory
        self._result_file_name = result_file_name
        self._decompress_result_file = True
        if result_file_name is not None:
            _, ext = path.splitext(result_file_name)
            if ext == '.zip':
                self._decompress_result_file = False
        self._overwrite_result_file = overwrite_result_file
        self._submit_upload_parameters = SubmitUploadParameters(
            upload_file_path=upload_file_path,
            compress_upload_file=compress_upload_file,
            response_mode=response_mode,
            rename_upload_file_to_match_request_id= rename_upload_file_to_match_request_id
        )
        self._timeout_in_milliseconds=timeout_in_milliseconds

    @property
    def decompress_result_file(self):
        return self._decompress_result_file

    @property
    def upload_file_path(self):
        """ The fully qualified local path of the upload file.

        :rtype: str
        """

        return self._submit_upload_parameters.upload_file_path

    @upload_file_path.setter
    def upload_file_path(self, upload_file_path):
        self._submit_upload_parameters.upload_file_path = upload_file_path

    @property
    def compress_upload_file(self):
        """ Determines whether the upload file should be compressed before uploading. The default value is True.

        :rtype: bool
        """

        return self._submit_upload_parameters.compress_upload_file

    @compress_upload_file.setter
    def compress_upload_file(self, compress):
        self._submit_upload_parameters.compress_upload_file = compress

    @property
    def response_mode(self):
        """ Determines whether the bulk service should return upload errors with the corresponding entity data.

        If not specified, this property is set by default to ErrorsAndResults.

        :rtype: str
        """

        return self._submit_upload_parameters.response_mode

    @response_mode.setter
    def response_mode(self, value):
        self._submit_upload_parameters.response_mode = value

    @property
    def result_file_directory(self):
        """ The directory where the file will be downloaded.

        :rtype: str
        """

        return self._result_file_directory

    @result_file_directory.setter
    def result_file_directory(self, result_file_directory):
        self._result_file_directory = result_file_directory

    @property
    def result_file_name(self):
        """ The name of the download result file.

        :rtype: str
        """

        return self._result_file_name

    @result_file_name.setter
    def result_file_name(self, result_file_name):
        self._result_file_name = result_file_name

    @property
    def overwrite_result_file(self):
        """ Whether the local result file should be overwritten if it already exists.

        :rtype: bool
        """

        return self._overwrite_result_file

    @overwrite_result_file.setter
    def overwrite_result_file(self, overwrite):
        self._overwrite_result_file = overwrite

    @property
    def timeout_in_milliseconds(self):
        return self._timeout_in_milliseconds


class SubmitUploadParameters(object):
    """ Describes the minimum available parameters when submitting a file for upload, such as the path of the upload file. """

    def __init__(self,
                 upload_file_path,
                 compress_upload_file=True,
                 response_mode='ErrorsAndResults',
                 timeout_in_milliseconds=None,
                 rename_upload_file_to_match_request_id=True):
        """ Initialize a new instance of this class.

        :param upload_file_path: The fully qualified local path of the upload file.
        :type upload_file_path: str
        :param compress_upload_file: (optional) Determines whether the upload file should be compressed before uploading. The default value is True.
        :type compress_upload_file: bool
        :param response_mode: (optional) Determines whether the bulk service should return upload errors with the corresponding entity data.
                                If not specified, this property is set by default to ErrorsAndResults.
        :type response_mode: str
        :param timeout_in_milliseconds: (optional) timeout for submit upload operations in milliseconds
        :type timeout_in_milliseconds: int
        """

        self._upload_file_path = upload_file_path
        self._compress_upload_file = compress_upload_file
        self._response_mode = response_mode
        self._timeout_in_milliseconds = timeout_in_milliseconds
        self._rename_upload_file_to_match_request_id=rename_upload_file_to_match_request_id

    @property
    def rename_upload_file_to_match_request_id(self):
        """ rename the upload file to request id or not.

        :rtype: boolean
        """
        return self._rename_upload_file_to_match_request_id;

    @property
    def upload_file_path(self):
        """ The fully qualified local path of the upload file.

        :rtype: str
        """

        return self._upload_file_path

    @property
    def compress_upload_file(self):
        """ Determines whether the upload file should be compressed before uploading. The default value is True.

        :rtype: bool
        """

        return self._compress_upload_file

    @upload_file_path.setter
    def upload_file_path(self, upload_file_path):
        self._upload_file_path = upload_file_path

    @compress_upload_file.setter
    def compress_upload_file(self, compress):
        self._compress_upload_file = compress

    @property
    def response_mode(self):
        """ Determines whether the bulk service should return upload errors with the corresponding entity data.

        If not specified, this property is set by default to ErrorsAndResults.

        :rtype: str
        """

        return self._response_mode

    @response_mode.setter
    def response_mode(self, value):
        self._response_mode = value

    @property
    def timeout_in_milliseconds(self):
        return self._timeout_in_milliseconds

    @timeout_in_milliseconds.setter
    def timeout_in_milliseconds(self, value):
        self._timeout_in_milliseconds = value


class EntityUploadParameters(object):
    """ Describes the available parameters when submitting entities for upload, such as the entities that you want to upload. """

    def __init__(self,
                 entities,
                 result_file_directory=None,
                 result_file_name=None,
                 overwrite_result_file=False,
                 response_mode='ErrorsAndResults',
                 timeout_in_milliseconds=None):
        """ Initializes a new instance of this class.

        :param entities: The list of bulk entities that you want to upload.
        :type entities: collections.Iterable[BulkEntity]
        :param result_file_directory: (optional) The directory where the file will be downloaded.
        :type result_file_directory: str
        :param result_file_name: (optional) The name of the download result file.
        :type result_file_name: str
        :param overwrite_result_file: (optional) Whether the local result file should be overwritten if it already exists.
        :type overwrite_result_file: bool
        :param response_mode: (optional) Determines whether the bulk service should return upload errors with the corresponding entity data.
                              If not specified, this property is set by default to ErrorsAndResults.
        :type response_mode: str
        :param timeout_in_milliseconds: (optional) timeout for entity upload operations in milliseconds
        :type timeout_in_milliseconds: int
        """

        self._result_file_directory = result_file_directory
        self._result_file_name = result_file_name
        self._decompress_result_file = True
        if result_file_name is not None:
            _, ext = path.splitext(result_file_name)
            if ext == '.zip':
                self._decompress_result_file = False
        self._entities = entities
        self._overwrite_result_file = overwrite_result_file
        self._response_mode = response_mode
        self._timeout_in_milliseconds = timeout_in_milliseconds

    @property
    def decompress_result_file(self):
        return self._decompress_result_file

    @property
    def entities(self):
        """ The list of bulk entities that you want to upload.

        :rtype: collections.Iterable[BulkEntity]
        """

        return self._entities

    @entities.setter
    def entities(self, value):
        self._entities = value

    @property
    def response_mode(self):
        """ Determines whether the bulk service should return upload errors with the corresponding entity data.

        If not specified, this property is set by default to ErrorsAndResults.

        :rtype: str
        """

        return self._response_mode

    @response_mode.setter
    def response_mode(self, value):
        self._response_mode = value

    @property
    def result_file_directory(self):
        """ The directory where the file will be downloaded.

        :rtype: str
        """

        return self._result_file_directory

    @result_file_directory.setter
    def result_file_directory(self, result_file_directory):
        self._result_file_directory = result_file_directory

    @property
    def result_file_name(self):
        """ The name of the download result file.

        :rtype: str
        """

        return self._result_file_name

    @result_file_name.setter
    def result_file_name(self, result_file_name):
        self._result_file_name = result_file_name

    @property
    def overwrite_result_file(self):
        """ Whether the local result file should be overwritten if it already exists.

        :rtype: bool
        """

        return self._overwrite_result_file

    @overwrite_result_file.setter
    def overwrite_result_file(self, overwrite):
        self._overwrite_result_file = overwrite

    @property
    def timeout_in_milliseconds(self):
        return self._timeout_in_milliseconds

    @timeout_in_milliseconds.setter
    def timeout_in_milliseconds(self, value):
        self._timeout_in_milliseconds = value
