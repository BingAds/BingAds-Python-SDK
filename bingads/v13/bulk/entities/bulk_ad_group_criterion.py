from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from abc import abstractmethod

_AdGroupCriterion = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('AdGroupCriterion'))
_NegativeAdGroupCriterion = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeAdGroupCriterion'))
_FixedBid = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('FixedBid'))
_BiddableAdGroupCriterion = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('BiddableAdGroupCriterion'))


def csv_to_bidding(row_values, entity):
    success, exclude = row_values.try_get_value(_StringTable.IsExcluded)
    if exclude is None:
        exclude = ''
    exclude = exclude.lower()
    if exclude == 'yes' or exclude == 'true':
        is_excluded = True
    elif exclude == 'no' or exclude == 'false':
        is_excluded = False
    else:
        raise ValueError('IsExcluded can only be set to TRUE|FALSE in Ad Group Criterion row')
    if is_excluded:
        negative_ad_group_criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeAdGroupCriterion')
        negative_ad_group_criterion.Criterion = entity.create_criterion()
        negative_ad_group_criterion.Type = 'NegativeAdGroupCriterion'

        entity.ad_group_criterion = negative_ad_group_criterion
    else:
        bid = _CAMPAIGN_OBJECT_FACTORY_V13.create('FixedBid')
        bid.Type = 'FixedBid'

        biddable_ad_group_criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('BiddableAdGroupCriterion')
        biddable_ad_group_criterion.Criterion = entity.create_criterion()

        success, bid_value = row_values.try_get_value(_StringTable.Bid)
        if success and bid_value is not None and bid_value != '':
            bid.Amount = float(bid_value)
        else:
            success, bid_value = row_values.try_get_value(_StringTable.BidAdjustment)
            if success and bid_value is not None and bid_value != '':
                bid = _CAMPAIGN_OBJECT_FACTORY_V13.create('BidMultiplier')
                bid.Type = 'BidMultiplier'
                bid.Multiplier = float(bid_value)

        biddable_ad_group_criterion.CriterionBid = bid
        biddable_ad_group_criterion.Type = 'BiddableAdGroupCriterion'

        entity.ad_group_criterion = biddable_ad_group_criterion


def bidding_to_csv(entity, row_values):
    if isinstance(entity.ad_group_criterion, _NegativeAdGroupCriterion):
        row_values[_StringTable.IsExcluded] = 'True'
    else:
        row_values[_StringTable.IsExcluded] = 'False'
        bid = entity.ad_group_criterion.CriterionBid
        if bid is None:
            return
        if isinstance(bid, _FixedBid):
            row_values[_StringTable.Bid] = fixed_bid_bulk_str(bid)
        else:
            row_values[_StringTable.BidAdjustment] = bid_multiplier_bulk_str(bid)

class BulkAdGroupCriterion(_SingleRecordBulkEntity):
    """ Represents a Ad Group Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`ad_group_criterion` property that can be read and written as fields of the
    Ad Group Criterion record in a bulk file.

    For more information, see Ad Group Criterion at https://go.microsoft.com/fwlink/?linkid=836837.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 campaign_name=None,
                 ad_group_name=None,
                 ad_group_criterion=None):
        super(BulkAdGroupCriterion, self).__init__()

        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name
        self._ad_group_criterion = ad_group_criterion
        self._performance_data = None

    _MAPPINGS = [
        _ComplexBulkMapping(bidding_to_csv, csv_to_bidding),

        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.ad_group_criterion.Status,
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion, 'Status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.ad_group_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.ad_group_criterion.AdGroupId),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion, 'AdGroupId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdGroup,
            field_to_csv=lambda c: c.ad_group_name,
            csv_to_field=lambda c, v: setattr(c, 'ad_group_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.ad_group_criterion.FinalUrls, c.ad_group_criterion.Id)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None,
            csv_to_field=lambda c, v: csv_to_field_Urls(c.ad_group_criterion.FinalUrls, v)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.ad_group_criterion.FinalMobileUrls, c.ad_group_criterion.Id)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None,
            csv_to_field=lambda c, v: csv_to_field_Urls(c.ad_group_criterion.FinalMobileUrls, v)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_optional_str(c.ad_group_criterion.TrackingUrlTemplate, c.ad_group_criterion.Id)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None,
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion, 'TrackingUrlTemplate', v if v else None)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.ad_group_criterion)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None,
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.ad_group_criterion, v)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.ad_group_criterion.FinalUrlSuffix,c.ad_group_criterion.Id)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None,
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion, 'FinalUrlSuffix', v)
            if isinstance(c.ad_group_criterion, _BiddableAdGroupCriterion) else None
        )
    ]

    @property
    def ad_group_criterion(self):
        """ Defines an Ad Group Criterion """

        return self._ad_group_criterion

    @ad_group_criterion.setter
    def ad_group_criterion(self, ad_group_criterion):
        self._ad_group_criterion = ad_group_criterion

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

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkAdGroupCriterion._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.ad_group_criterion, 'ad_group_criterion')
        self.convert_to_values(row_values, BulkAdGroupCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupCriterion, self).read_additional_data(stream_reader)

    @abstractmethod
    def create_criterion(self):
        return None
