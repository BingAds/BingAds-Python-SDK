from bingads.v13.internal.bulk.entities.bulk_shared_site import BulkSharedSite


class BulkAccountPlacementInclusionListItem(BulkSharedSite):
    """ Represents an account placement inclusion list item.

    This class exposes the property :attr:`account_placement_inclusion_list` that can be read and written as fields of the account placement inclusion list item record
    in a bulk file.

    For more information, see account placement inclusion list item at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, parent_id=None):
        super(BulkAccountPlacementInclusionListItem, self).__init__()

        self._parent_id = parent_id


    @property
    def account_placement_inclusion_list_id(self):
        """ The status of the account placement inclusion list id.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._parent_id

    @account_placement_inclusion_list_id.setter
    def account_placement_inclusion_list_id(self, account_placement_inclusion_list_id):
        self._parent_id = account_placement_inclusion_list_id

