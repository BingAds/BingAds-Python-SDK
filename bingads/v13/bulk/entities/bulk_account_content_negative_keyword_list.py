from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import bulk_str
from bingads.v13.bulk.entities.bulk_negative_keywords import _BulkNegativeKeyword


class BulkAccountContentNegativeKeywordList(_SingleRecordBulkEntity):
    """ Represents an account content negative keyword list that can be read or written in a bulk file.

    This class exposes the :attr:`.BulkAccountContentNegativeKeywordList.account_content_negative_keyword_list`
    property that can be read and written as fields of the Account Content Negative Keyword List record in a bulk file.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, account_content_negative_keyword_list=None):
        super(BulkAccountContentNegativeKeywordList, self).__init__()

        self._status = status
        self._account_content_negative_keyword_list = account_content_negative_keyword_list

    @property
    def account_content_negative_keyword_list(self):
        return self._account_content_negative_keyword_list

    @account_content_negative_keyword_list.setter
    def account_content_negative_keyword_list(self, account_content_negative_keyword_list):
        self._account_content_negative_keyword_list = account_content_negative_keyword_list

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.account_content_negative_keyword_list.Id),
            csv_to_field=lambda c, v: setattr(c.account_content_negative_keyword_list, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: c.account_content_negative_keyword_list.Name,
            csv_to_field=lambda c, v: setattr(c.account_content_negative_keyword_list, 'Name', v)
        ),
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._account_content_negative_keyword_list, 'account_content_negative_keyword_list')
        self.convert_to_values(row_values, BulkAccountContentNegativeKeywordList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._account_content_negative_keyword_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('AccountContentNegativeKeywordList')
        self._account_content_negative_keyword_list.Type = 'AccountContentNegativeKeywordList'
        row_values.convert_to_entity(self, BulkAccountContentNegativeKeywordList._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAccountContentNegativeKeywordList, self).read_additional_data(stream_reader)


class BulkAccountContentNegativeKeywordListAssociation(_SingleRecordBulkEntity):
    """ Represents an account content negative keyword list association that can be read or written in a bulk file.

    This class exposes the :attr:`BulkAccountContentNegativeKeywordListAssociation.shared_entity_association`
    property that can be read and written as fields of the Account Content Negative Keyword List Association
    record in a bulk file.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, shared_entity_association=None):
        super(BulkAccountContentNegativeKeywordListAssociation, self).__init__()

        self._shared_entity_association = shared_entity_association
        self._status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def shared_entity_association(self):
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
        self.convert_to_values(row_values, BulkAccountContentNegativeKeywordListAssociation._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._shared_entity_association = _CAMPAIGN_OBJECT_FACTORY_V13.create('SharedEntityAssociation')
        self._shared_entity_association.EntityType = 'Account'
        self._shared_entity_association.SharedEntityType = 'AccountContentNegativeKeywordList'
        row_values.convert_to_entity(self, BulkAccountContentNegativeKeywordListAssociation._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAccountContentNegativeKeywordListAssociation, self).read_additional_data(stream_reader)


class BulkAccountContentSharedNegativeKeyword(_BulkNegativeKeyword):
    """ Represents an account content negative keyword that is shared in a content negative keyword list.

    Each shared negative keyword can be read or written in a bulk file.
    This class exposes the :attr:`.BulkNegativeKeyword.NegativeKeyword` property that
    can be read and written as fields of the Account Content Shared Negative Keyword record in a bulk file.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, negative_keyword=None, negative_keyword_list_id=None):
        super(BulkAccountContentSharedNegativeKeyword, self).__init__(status, negative_keyword, negative_keyword_list_id)

    @property
    def negative_keyword_list_id(self):
        return self._parent_id

    @negative_keyword_list_id.setter
    def negative_keyword_list_id(self, value):
        self._parent_id = value
