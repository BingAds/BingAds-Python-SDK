from ...exceptions import SdkException


class ReportingException(SdkException):
    def __init__(self, message, errors):
        super(ReportingException, self).__init__(message)
        self._errors = errors

    @property
    def errors(self):
        """ The list of operation errors returned by the reporting service.

        :rtype: list[OperationError]
        """
        return self._errors


class ReportingDownloadException(SdkException):
    def __init__(self, message):
        super(ReportingDownloadException, self).__init__(message)


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
