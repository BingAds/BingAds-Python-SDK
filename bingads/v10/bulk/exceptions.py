from bingads.exceptions import SdkException


class BulkException(SdkException):
    def __init__(self, message, errors):
        super(BulkException, self).__init__(message)
        self._errors = errors

    @property
    def errors(self):
        """ The list of operation errors returned by the bulk service.

        :rtype: list[OperationError]
        """
        return self._errors


class BulkUploadException(SdkException):
    def __init__(self, message):
        super(BulkUploadException, self).__init__(message)


class BulkDownloadException(SdkException):
    def __init__(self, message):
        super(BulkDownloadException, self).__init__(message)


class EntityReadException(SdkException):
    def __init__(self, message, row_values=None, inner_exception=None):
        super(EntityReadException, self).__init__(message)
        self._row_values = row_values
        self._inner_exception = inner_exception

    @property
    def row_values(self):
        return self._row_values

    @property
    def inner_exception(self):
        return self._inner_exception


class EntityWriteException(SdkException):
    def __init__(self, message, inner_exception=None):
        super(EntityWriteException, self).__init__(message)
        self._inner_exception = inner_exception

    @property
    def inner_exception(self):
        return self._inner_exception


class OperationError:
    """ Defines an error object that contains the details that explain why the service operation failed. """

    def __init__(self,
                 code=None,
                 details=None,
                 error_code=None,
                 message=None,):
        self._code = code
        self._details = details
        self._error_code = error_code
        self._message = message

    @property
    def code(self):
        """ A numeric error code that identifies the error

        :rtype: int
        """

        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def details(self):
        """ A message that provides additional details about the error. This string can be empty.

        :rtype: str
        """

        return self._details

    @details.setter
    def details(self, value):
        self._details = value

    @property
    def error_code(self):
        """ A symbolic string constant that identifies the error. For example, UserIsNotAuthorized.

        :rtype: str
        """

        return self._error_code

    @error_code.setter
    def error_code(self, value):
        self._error_code = value

    @property
    def message(self):
        """ A message that describes the error.

        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
