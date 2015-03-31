from bingads.bulk.entities.common import _ProductConditionHelper  # noqa
from bingads.internal.bulk.string_table import _StringTable
from bingads.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.internal.extensions import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY


class BulkAdGroupProductTarget(_SingleRecordBulkEntity):
    """ Represents an ad group product target.

    This class exposes the :attr:`biddable_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Product Target record in a bulk file.

    For more information, see Ad Group Product Target at http://go.microsoft.com/fwlink/?LinkID=511550.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupProductTarget, self).__init__()

        self._biddable_ad_group_criterion = biddable_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name

    @property
    def biddable_ad_group_criterion(self):
        """ The BiddableAdGroupCriterion Data Object of the Campaign Management Service.

        A subset of BiddableAdGroupCriterion properties are available in the Ad Group Product Target record.
        For more information, see Ad Group Product Target at http://go.microsoft.com/fwlink/?LinkID=511550.

        see BiddableAdGroupCriterion at: https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-biddableadgroupcriterion.aspx
        """

        return self._biddable_ad_group_criterion

    @biddable_ad_group_criterion.setter
    def biddable_ad_group_criterion(self, value):
        self._biddable_ad_group_criterion = value

    @property
    def campaign_name(self):
        """ The name of the campaign that contains the ad group product target.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._campaign_name = value

    @property
    def ad_group_name(self):
        """ The name of the ad group that contains the ad group product target.

        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """

        return self._ad_group_name

    @ad_group_name.setter
    def ad_group_name(self, value):
        self._ad_group_name = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.biddable_ad_group_criterion.Status),
            csv_to_field=lambda c, v: setattr(
                c.biddable_ad_group_criterion,
                'Status',
                v if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.biddable_ad_group_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.biddable_ad_group_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.biddable_ad_group_criterion.AdGroupId),
            csv_to_field=lambda c, v: setattr(
                c.biddable_ad_group_criterion,
                'AdGroupId',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, '_campaign_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdGroup,
            field_to_csv=lambda c: c.ad_group_name,
            csv_to_field=lambda c, v: setattr(c, '_ad_group_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialStatus,
            field_to_csv=lambda c: bulk_str(c.biddable_ad_group_criterion.EditorialStatus),
            csv_to_field=lambda c, v: setattr(
                c.biddable_ad_group_criterion,
                'EditorialStatus',
                v if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Bid,
            field_to_csv=lambda c: ad_group_bid_bulk_str(c.biddable_ad_group_criterion.CriterionBid.Bid),
            csv_to_field=lambda c, v: setattr(
                c.biddable_ad_group_criterion.CriterionBid,
                'Bid',
                parse_ad_group_bid(v)
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.DestinationUrl,
            field_to_csv=lambda c: bulk_optional_str(c.biddable_ad_group_criterion.DestinationUrl),
            csv_to_field=lambda c, v: setattr(
                c.biddable_ad_group_criterion,
                'DestinationUrl',
                v if v else ''
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Param1,
            field_to_csv=lambda c: bulk_optional_str(c.biddable_ad_group_criterion.Param1),
            csv_to_field=lambda c, v: setattr(
                c.biddable_ad_group_criterion,
                'Param1',
                v if v else ''
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Param2,
            field_to_csv=lambda c: bulk_optional_str(c.biddable_ad_group_criterion.Param2),
            csv_to_field=lambda c, v: setattr(
                c.biddable_ad_group_criterion,
                'Param2',
                v if v else ''
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Param3,
            field_to_csv=lambda c: bulk_optional_str(c.biddable_ad_group_criterion.Param3),
            csv_to_field=lambda c, v: setattr(
                c.biddable_ad_group_criterion,
                'Param3',
                v if v else ''
            )
        ),
        _ComplexBulkMapping(
            entity_to_csv=lambda entity, row_values: _ProductConditionHelper.add_row_values_from_conditions(
                entity.biddable_ad_group_criterion.Criterion.Conditions.ProductCondition,
                row_values
            ),
            csv_to_entity=lambda row_values, entity: _ProductConditionHelper.add_conditions_from_row_values(
                row_values,
                entity.biddable_ad_group_criterion.Criterion.Conditions.ProductCondition,
            )
        )
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkAdGroupProductTarget._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.biddable_ad_group_criterion = _CAMPAIGN_OBJECT_FACTORY.create('BiddableAdGroupCriterion')
        self.biddable_ad_group_criterion.Type = 'BiddableAdGroupCriterion'
        self.biddable_ad_group_criterion.CriterionBid = _CAMPAIGN_OBJECT_FACTORY.create('FixedBid')
        self.biddable_ad_group_criterion.CriterionBid.Type = 'FixedBid'
        self.biddable_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY.create('Product')
        self.biddable_ad_group_criterion.Criterion.Type = 'Product'

        row_values.convert_to_entity(self, BulkAdGroupProductTarget._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupProductTarget, self).read_additional_data(stream_reader)
