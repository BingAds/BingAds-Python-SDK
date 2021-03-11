from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.extensions import *
from decimal import Decimal


class BulkBidStrategy(_SingleRecordBulkEntity):
    """ Represents a bid strategy that can be read or written in a bulk file.

    Properties of this class and of classes that it is derived from, correspond to fields of the Bid Strategy record in a bulk file.
    For more information, see Bid Strategy at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, bid_strategy=None, status=None, account_id=None):
        super(BulkBidStrategy, self).__init__()
        self._bid_strategy = bid_strategy
        self._status = status
        self._account_id = account_id

    @property
    def bid_strategy(self):
        """
        the Bid Strategy object, see more detail at: https://go.microsoft.com/fwlink/?linkid=846127
        """
        return self._bid_strategy

    @bid_strategy.setter
    def bid_strategy(self, value):
        self._bid_strategy = value

    @property
    def status(self):
        """ the status of bulk record
        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def account_id(self):
        """ the id of the account which contains the bid strategy
        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: long
        """
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.bid_strategy.Id),
            csv_to_field=lambda c, v: setattr(c.bid_strategy, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, 'account_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidStrategyName,
            field_to_csv=lambda c: bulk_str(c.bid_strategy.Name),
            csv_to_field=lambda c, v: setattr(c.bid_strategy, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CampaignType,
            field_to_csv=lambda c: bulk_str(c.bid_strategy.AssociatedCampaignType),
            csv_to_field=lambda c, v: setattr(c.bid_strategy, 'AssociatedCampaignType', v if v else None)
        ),
        _ComplexBulkMapping(bid_strategy_biddingscheme_to_csv, csv_to_bid_strategy_biddingscheme),
    ]

    def process_mappings_from_row_values(self, row_values):
        self._bid_strategy = _CAMPAIGN_OBJECT_FACTORY_V13.create('BidStrategy')
        row_values.convert_to_entity(self, BulkBidStrategy._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.bid_strategy, 'bid_strategy')
        self.convert_to_values(row_values, BulkBidStrategy._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkBidStrategy, self).read_additional_data(stream_reader)
