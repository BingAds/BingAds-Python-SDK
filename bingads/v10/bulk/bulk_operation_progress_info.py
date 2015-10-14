class BulkOperationProgressInfo(object):
    """ Contains percent complete progress information for the bulk operation."""

    def __init__(self, percent_complete=0):
        """ Initialize a new instance of this class.

        :param percent_complete: (optional) Percent complete progress information for the bulk operation.
        :type percent_complete: int
        """

        self._percent_complete = percent_complete

    @property
    def percent_complete(self):
        """ Percent complete progress information for the bulk operation.

        :rtype: int
        """

        return self._percent_complete
