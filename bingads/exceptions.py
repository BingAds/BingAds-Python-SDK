class SdkException(Exception):
    """ Base Exception for exceptions in SDK. """

    def __init__(self, message):
        """ Initialize a new instance of this class with detailed message.

        :param message: Detailed exception message.
        :type message: str
        """

        self._message = message

    def __str__(self):
        return self.message

    @property
    def message(self):
        """ Detailed exception message.

        :rtype: str
        """
        return self._message


class OAuthTokenRequestException(SdkException):
    """ This exception is thrown if an error was returned from the Microsoft Account authorization server. """

    def __init__(self, error_code, description):
        """ Initializes a new instance of this class with the specified error code and OAuth error details.

        :param error_code: The error code of the OAuth error.
        :type error_code: str
        :param description: The description of the OAuth error.
        :type description: str
        """

        super(OAuthTokenRequestException, self).__init__(
            str.format("error_code: {0}, error_description: {1}", error_code, description))
        self._error_code = error_code
        self._error_description = description

    @property
    def error_code(self):
        """ The error code of the OAuth error.

        :rtype: str
        """

        return self._error_code

    @property
    def error_description(self):
        """ The description of the OAuth error.

        :rtype: str
        """

        return self._error_description


class FileUploadException(SdkException):
    """ This exception is thrown if timeout occurs """

    def __init__(self, description):
        """ Initializes a new instance of this class with the specified error messages.

        :param description: The description of the file upload error.
        :type description: str
        """
        super(FileUploadException, self).__init__(str(description))


class FileDownloadException(SdkException):
    """ This exception is thrown if timeout occurs """

    def __init__(self, description):
        """ Initializes a new instance of this class with the specified error messages.

        :param description: The description of the file download error.
        :type description: str
        """
        super(FileDownloadException, self).__init__(str(description))


class TimeoutException(SdkException):
    """ This exception is thrown if timeout occurs """

    def __init__(self, description):
        """ Initializes a new instance of this class with the specified error messages.

        :param description: The description of the file download error.
        :type description: str
        """
        super(TimeoutException, self).__init__(str(description))