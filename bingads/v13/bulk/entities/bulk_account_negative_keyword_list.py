from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import bulk_str

class BulkAccountNegativeKeywordList(_SingleRecordBulkEntity):
    """ Represents an account negative keyword list association that can be read or written in a bulk file.

    This class exposes the :attr:`.BulkAccountNegativeKeywordList.account_negative_keyword_list` property that can be read and
    written as fields of the account negative keyword list association record in a bulk file.

    For more information, see account negative keyword list association at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, account_negative_keyword_list=None):
        super(BulkAccountNegativeKeywordList, self).__init__()

        self._status = status
        self._account_negative_keyword_list = account_negative_keyword_list

    @property
    def account_negative_keyword_list(self):
        """ The account negative keyword list association.

        see account negative keyword list association at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._account_negative_keyword_list

    @account_negative_keyword_list.setter
    def account_negative_keyword_list(self, account_negative_keyword_list):
        self._account_negative_keyword_list = account_negative_keyword_list

    @property
    def status(self):
        """ The status of the account negative keyword list association.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.account_negative_keyword_list.Id),
            csv_to_field=lambda c, v: setattr(c.account_negative_keyword_list, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: c.account_negative_keyword_list.Name,
            csv_to_field=lambda c, v: setattr(c.account_negative_keyword_list, 'Name', v)
        )
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._account_negative_keyword_list, 'account_negative_keyword_list')
        self.convert_to_values(row_values, BulkAccountNegativeKeywordList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._account_negative_keyword_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('AccountNegativeKeywordList')
        self._account_negative_keyword_list.Type = 'AccountNegativeKeywordList'
        row_values.convert_to_entity(self, BulkAccountNegativeKeywordList._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAccountNegativeKeywordList, self).read_additional_data(stream_reader)

class BulkAccountNegativeKeywordListAssociation(_SingleRecordBulkEntity):
    """ Represents an account negative keyword list association that is assigned to a campaign. Each account negative keyword list association can be read or written in a bulk file.

    This class exposes the :attr:`BulkAccountNegativeKeywordListAssociation.SharedEntityAssociation` property that can be read
    and written as fields of the account negative keyword list association record in a bulk file.

    For more information, see account negative keyword list association at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, shared_entity_association=None):
        super(BulkAccountNegativeKeywordListAssociation, self).__init__()

        self._shared_entity_association = shared_entity_association
        self._status = status

    @property
    def status(self):
        """ The status of the account negative keyword list association.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def shared_entity_association(self):
        """ The campaign and account negative keyword list association identifiers.

        see Campaign account negative keyword list association at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._shared_entity_association

    @shared_entity_association.setter
    def shared_entity_association(self, shared_entity_association):
        self._shared_entity_association = shared_entity_association

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.shared_entity_association.SharedEntityId),
            csv_to_field=lambda c, v: setattr(c.shared_entity_association, 'SharedEntityId', int(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.shared_entity_association.EntityId),
            csv_to_field=lambda c, v: setattr(c.shared_entity_association, 'EntityId', int(v))
        ),
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._shared_entity_association, 'shared_entity_association')
        self.convert_to_values(row_values, BulkAccountNegativeKeywordListAssociation._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._shared_entity_association = _CAMPAIGN_OBJECT_FACTORY_V13.create('SharedEntityAssociation')
        self._shared_entity_association.EntityType = 'Account'
        self._shared_entity_association.SharedEntityType = 'NegativeKeywordList'
        row_values.convert_to_entity(self, BulkAccountNegativeKeywordListAssociation._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAccountNegativeKeywordListAssociation, self).read_additional_data(stream_reader)


