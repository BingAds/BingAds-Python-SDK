from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _DynamicColumnNameMapping
from bingads.v13.internal.extensions import *


class _BulkNegativeKeyword(_SingleRecordBulkEntity):
    """ The base class for all bulk negative keywords.

    Either assigned individually to a campaign or ad group entity, or shared in a negative keyword list.

    *See also:*

    * :class:`.BulkAdGroupNegativeKeyword`
    * :class:`.BulkCampaignNegativeKeyword`
    * :class:`.BulkSharedNegativeKeyword`
    """

    def __init__(self, status=None, negative_keyword=None, parent_id=None):
        super(_BulkNegativeKeyword, self).__init__()

        self._negative_keyword = negative_keyword
        self._status = status
        self._parent_id = parent_id

    @property
    def status(self):
        """ The status of the negative keyword association.

        The value is 'Active' if the negative keyword is assigned to the parent entity.
        The value is 'Deleted' if the negative keyword is removed from the parent entity,
                                    or should be removed in a subsequent upload operation.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def negative_keyword(self):
        """ Defines a negative keyword with match type. """

        return self._negative_keyword

    @negative_keyword.setter
    def negative_keyword(self, negative_keyword):
        self._negative_keyword = negative_keyword

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.negative_keyword.Id),
            csv_to_field=lambda c, v: setattr(c.negative_keyword, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, '_status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c._parent_id),
            csv_to_field=lambda c, v: setattr(c, '_parent_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Keyword,
            field_to_csv=lambda c: c.negative_keyword.Text,
            csv_to_field=lambda c, v: setattr(c.negative_keyword, 'Text', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MatchType,
            field_to_csv=lambda c: bulk_str(c.negative_keyword.MatchType),
            csv_to_field=lambda c, v: csv_to_field_enum(c.negative_keyword, v, 'MatchType', MatchType)
        )
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._negative_keyword, 'negative_keyword')
        self.convert_to_values(row_values, _BulkNegativeKeyword._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._negative_keyword = _CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeKeyword')
        self._negative_keyword.Type = 'NegativeKeyword'
        row_values.convert_to_entity(self, _BulkNegativeKeyword._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(_BulkNegativeKeyword, self).read_additional_data(stream_reader)


class _BulkEntityNegativeKeyword(_BulkNegativeKeyword):
    """ This base class for all bulk negative keywords that are assigned individually to a campaign or ad group entity.

    *See also:*

    * :class:`.BulkAdGroupNegativeKeyword`
    * :class:`.BulkCampaignNegativeKeyword`
    """

    def __init__(self,
                 status=None,
                 negative_keyword=None,
                 parent_id=None,
                 entity_name=None):
        super(_BulkEntityNegativeKeyword, self).__init__(
            status,
            negative_keyword,
            parent_id,
        )
        self._entity_name = entity_name

    @property
    def _entity_column_name(self):
        raise NotImplementedError()

    _MAPPINGS = [
        _DynamicColumnNameMapping(
            header_func=lambda c: c._entity_column_name,
            field_to_csv=lambda c: c._entity_name,
            csv_to_field=lambda c, v: setattr(c, '_entity_name', v))
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(_BulkEntityNegativeKeyword, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, _BulkEntityNegativeKeyword._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(_BulkEntityNegativeKeyword, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, _BulkEntityNegativeKeyword._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(_BulkEntityNegativeKeyword, self).read_additional_data(stream_reader)


class BulkAdGroupNegativeKeyword(_BulkEntityNegativeKeyword):
    """ Represents a negative keyword that is assigned to a ad group. Each negative keyword can be read or written in a bulk file.

    This class exposes the :attr:`.BulkNegativeKeyword.negative_keyword` property that can be read and written as
    fields of the Ad Group Negative Keyword record in a bulk file.

    For more information, see Ad Group Negative Keyword at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 status=None,
                 negative_keyword=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None):
        super(BulkAdGroupNegativeKeyword, self).__init__(
            status,
            negative_keyword,
            ad_group_id,
            ad_group_name,
        )
        self._campaign_name = campaign_name

    @property
    def campaign_name(self):
        """ The name of the campaign that the negative keyword is assigned.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @property
    def ad_group_id(self):
        """ Corresponds to the 'Parent Id' field in the bulk file.

        :return: The identifier of the ad group that the negative keyword is assigned.
        :rtype: int
        """

        return self._parent_id

    @ad_group_id.setter
    def ad_group_id(self, value):
        self._parent_id = value

    @property
    def ad_group_name(self):
        """ Corresponds to the 'Ad Group' field in the bulk file.

        :return: The name of the ad group that the negative keyword is assigned.
        :rtype: str
        """

        return self._entity_name

    @ad_group_name.setter
    def ad_group_name(self, value):
        self._entity_name = value

    @property
    def _entity_column_name(self):
        return _StringTable.AdGroup

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        )
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkAdGroupNegativeKeyword, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAdGroupNegativeKeyword._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkAdGroupNegativeKeyword, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAdGroupNegativeKeyword._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupNegativeKeyword, self).read_additional_data(stream_reader)


class BulkCampaignNegativeKeyword(_BulkEntityNegativeKeyword):
    """ Represents a negative keyword that is assigned to a campaign. Each negative keyword can be read or written in a bulk file.

    This class exposes the :attr:`BulkNegativeKeyword.negative_keyword` property that can be read and written as
    fields of the Campaign Negative Keyword record in a bulk file.

    For more information, see Campaign Negative Keyword at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 status=None,
                 negative_keyword=None,
                 campaign_id=None,
                 campaign_name=None):
        super(BulkCampaignNegativeKeyword, self).__init__(
            status,
            negative_keyword,
            campaign_id,
            campaign_name,
        )

    @property
    def campaign_id(self):
        """ The identifier of the campaign that the negative keyword is assigned.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._parent_id

    @campaign_id.setter
    def campaign_id(self, value):
        self._parent_id = value

    @property
    def campaign_name(self):
        """ The name of the campaign that the negative keyword is assigned.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._entity_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._entity_name = value

    @property
    def _entity_column_name(self):
        return _StringTable.Campaign


class BulkCampaignNegativeKeywordList(_SingleRecordBulkEntity):
    """ Represents a negative keyword list that is assigned to a campaign. Each negative keyword list can be read or written in a bulk file.

    This class exposes the :attr:`BulkCampaignNegativeKeywordList.SharedEntityAssociation` property that can be read
    and written as fields of the Campaign Negative Keyword List Association record in a bulk file.

    For more information, see Campaign Negative Keyword List Association at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, shared_entity_association=None):
        super(BulkCampaignNegativeKeywordList, self).__init__()

        self._shared_entity_association = shared_entity_association
        self._status = status

    @property
    def status(self):
        """ The status of the negative keyword list association.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def shared_entity_association(self):
        """ The campaign and negative keyword list identifiers.

        see Campaign Negative Keyword List Association at https://go.microsoft.com/fwlink/?linkid=846127.
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
        self.convert_to_values(row_values, BulkCampaignNegativeKeywordList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._shared_entity_association = _CAMPAIGN_OBJECT_FACTORY_V13.create('SharedEntityAssociation')
        self._shared_entity_association.EntityType = 'Campaign'
        self._shared_entity_association.SharedEntityType = 'NegativeKeywordList'
        row_values.convert_to_entity(self, BulkCampaignNegativeKeywordList._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignNegativeKeywordList, self).read_additional_data(stream_reader)

class BulkNegativeKeywordList(_SingleRecordBulkEntity):
    """ Represents a negative keyword list that can be read or written in a bulk file.

    This class exposes the :attr:`.BulkNegativeKeywordList.negative_keyword_list` property that can be read and
    written as fields of the Negative Keyword List record in a bulk file.

    For more information, see Negative Keyword List at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, negative_keyword_list=None):
        super(BulkNegativeKeywordList, self).__init__()

        self._status = status
        self._negative_keyword_list = negative_keyword_list

    @property
    def negative_keyword_list(self):
        """ The negative keyword list.

        see Negative Keyword List at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._negative_keyword_list

    @negative_keyword_list.setter
    def negative_keyword_list(self, negative_keyword_list):
        self._negative_keyword_list = negative_keyword_list

    @property
    def status(self):
        """ The status of the negative keyword list.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.negative_keyword_list.Id),
            csv_to_field=lambda c, v: setattr(c.negative_keyword_list, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: c.negative_keyword_list.Name,
            csv_to_field=lambda c, v: setattr(c.negative_keyword_list, 'Name', v)
        )
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._negative_keyword_list, 'negative_keyword_list')
        self.convert_to_values(row_values, BulkNegativeKeywordList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._negative_keyword_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeKeywordList')
        self._negative_keyword_list.Type = 'NegativeKeywordList'
        row_values.convert_to_entity(self, BulkNegativeKeywordList._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkNegativeKeywordList, self).read_additional_data(stream_reader)


class BulkSharedNegativeKeyword(_BulkNegativeKeyword):
    """ Represents a negative keyword that is shared in a negative keyword list.

    Each shared negative keyword can be read or written in a bulk file.
    This class exposes the :attr:`.BulkNegativeKeyword.NegativeKeyword` property that
    can be read and written as fields of the Shared Negative Keyword record in a bulk file.

    For more information, see Shared Negative Keyword at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, negative_keyword=None, negative_keyword_list_id=None):
        super(BulkSharedNegativeKeyword, self).__init__(status, negative_keyword, negative_keyword_list_id)

    @property
    def negative_keyword_list_id(self):
        return self._parent_id

    @negative_keyword_list_id.setter
    def negative_keyword_list_id(self, value):
        self._parent_id = value

class BulkAccountSharedNegativeKeyword(_BulkNegativeKeyword):
    """ Represents an account negative keyword that is shared in a negative keyword list.

    Each shared negative keyword can be read or written in a bulk file.
    This class exposes the :attr:`.BulkNegativeKeyword.NegativeKeyword` property that
    can be read and written as fields of the Account Shared Negative Keyword record in a bulk file.

    For more information, see Account Shared Negative Keyword at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, negative_keyword=None, negative_keyword_list_id=None):
        super(BulkAccountSharedNegativeKeyword, self).__init__(status, negative_keyword, negative_keyword_list_id)

    @property
    def negative_keyword_list_id(self):
        return self._parent_id

    @negative_keyword_list_id.setter
    def negative_keyword_list_id(self, value):
        self._parent_id = value
