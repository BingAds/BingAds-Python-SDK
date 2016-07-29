from bingads.v10.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V10
from bingads.v10.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v10.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v10.internal.bulk.string_table import _StringTable
from bingads.internal.extensions import *

class BulkAdGroupRemarketingListAssociation(_SingleRecordBulkEntity):
    """ Represents an Ad Group Remarketing List Association that can be read or written in a bulk file.

    This class exposes the :attr:`ad_group_remarketing_list_association` property that can be read and written as fields of the
    Ad Group Remarketing List Association record in a bulk file.

    For more information, see Ad Group Remarketing List Association at http://go.microsoft.com/fwlink/?LinkId=799353.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 ad_group_remarketing_list_association=None,
                 campaign_name=None,
                 ad_group_name=None,
                 remarketing_list_name=None):
        super(BulkAdGroupRemarketingListAssociation, self).__init__()

        self._ad_group_remarketing_list_association = ad_group_remarketing_list_association
        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name
        self._remarketing_list_name = remarketing_list_name

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.ad_group_remarketing_list_association.Status),
            csv_to_field=lambda c, v: setattr(c.ad_group_remarketing_list_association, 'Status', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.ad_group_remarketing_list_association.Id),
            csv_to_field=lambda c, v: setattr(c.ad_group_remarketing_list_association, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.ad_group_remarketing_list_association.AdGroupId),
            csv_to_field=lambda c, v: setattr(c.ad_group_remarketing_list_association, 'AdGroupId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.AdGroup,
            field_to_csv=lambda c: c.ad_group_name,
            csv_to_field=lambda c, v: setattr(c, 'ad_group_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.RemarketingList,
            field_to_csv=lambda c: c.remarketing_list_name,
            csv_to_field=lambda c, v: setattr(c, 'remarketing_list_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.ad_group_remarketing_list_association.BidAdjustment),
            csv_to_field=lambda c, v: setattr(c.ad_group_remarketing_list_association, 'BidAdjustment', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.RemarketingListId,
            field_to_csv=lambda c: bulk_str(c.ad_group_remarketing_list_association.RemarketingListId),
            csv_to_field=lambda c, v: setattr(c.ad_group_remarketing_list_association, 'RemarketingListId', int(v) if v else None)
        ),
    ]

    @property
    def ad_group_remarketing_list_association(self):
        """ Defines an Ad Group Remarketing List Association """

        return self._ad_group_remarketing_list_association

    @ad_group_remarketing_list_association.setter
    def ad_group_remarketing_list_association(self, ad_group_remarketing_list_association):
        self._ad_group_remarketing_list_association = ad_group_remarketing_list_association

    @property
    def campaign_name(self):
        """ Defines the name of the Campaign.

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @property
    def ad_group_name(self):
        """ Defines the name of the Ad Group

        :rtype: str
        """

        return self._ad_group_name

    @ad_group_name.setter
    def ad_group_name(self, ad_group_name):
        self._ad_group_name = ad_group_name

    @property
    def remarketing_list_name(self):
        """ Defines the name of the Remarketing List

        :rtype: str
        """

        return self._remarketing_list_name

    @remarketing_list_name.setter
    def remarketing_list_name(self, remarketing_list_name):
        self._remarketing_list_name = remarketing_list_name

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.ad_group_remarketing_list_association, 'ad_group_remarketing_list_association')
        self.convert_to_values(row_values, BulkAdGroupRemarketingListAssociation._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._ad_group_remarketing_list_association = _CAMPAIGN_OBJECT_FACTORY_V10.create('AdGroupRemarketingListAssociation')
        row_values.convert_to_entity(self, BulkAdGroupRemarketingListAssociation._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupRemarketingListAssociation, self).read_additional_data(stream_reader)
