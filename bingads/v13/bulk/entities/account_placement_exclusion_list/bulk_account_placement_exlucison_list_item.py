from bingads.v13.internal.bulk.entities.bulk_shared_negative_site import BulkSharedNegativeSite


class BulkAccountPlacementExclusionListItem(BulkSharedNegativeSite):
    """ Represents an account placement exclusion list item.

    This class exposes the property :attr:`account_placement_exclusion_list` that can be read and written as fields of the account placement exclusion list item record
    in a bulk file.

    For more information, see account placement exclusion list item at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, parent_id=None):
        super(BulkAccountPlacementExclusionListItem, self).__init__()

        self._parent_id = parent_id


    @property
    def account_placement_exclusion_list_id(self):
        """ The status of the account placement exclusion list id.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._parent_id

    @account_placement_exclusion_list_id.setter
    def account_placement_exclusion_list_id(self, account_placement_exclusion_list_id):
        self._parent_id = account_placement_exclusion_list_id

