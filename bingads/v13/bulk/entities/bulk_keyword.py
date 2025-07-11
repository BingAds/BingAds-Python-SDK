from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities import *
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.extensions import *


def bidding_scheme_to_csv(bulk_keyword, row_values):
    bid_strategy_type = field_to_csv_BidStrategyType(bulk_keyword.keyword)
    if not bid_strategy_type:
        return
    row_values[_StringTable.BidStrategyType] = bid_strategy_type
    if bid_strategy_type == 'InheritFromParent' \
        and hasattr(bulk_keyword.keyword.BiddingScheme, 'InheritedBidStrategyType'):
        row_values[_StringTable.InheritedBidStrategyType] = bulk_keyword.keyword.BiddingScheme.InheritedBidStrategyType


def csv_to_bidding_scheme(row_values, bulk_keyword):
    success, bid_strategy_type = row_values.try_get_value(_StringTable.BidStrategyType)
    if not success or not bid_strategy_type:
        return
    csv_to_field_BidStrategyType(bulk_keyword.keyword, bid_strategy_type)
    if bid_strategy_type == 'InheritFromParent':
        bulk_keyword.keyword.BiddingScheme.Type = "InheritFromParent"
        success, inherited_bid_strategy_type = row_values.try_get_value(_StringTable.InheritedBidStrategyType)
        if success and inherited_bid_strategy_type != '':
            bulk_keyword.keyword.BiddingScheme.InheritedBidStrategyType = inherited_bid_strategy_type
        elif hasattr(bulk_keyword.keyword.BiddingScheme, 'InheritedBidStrategyType'):
            bulk_keyword.keyword.BiddingScheme.InheritedBidStrategyType = None
    else:
        bulk_keyword.keyword.BiddingScheme.Type = bid_strategy_type


class BulkKeyword(_SingleRecordBulkEntity):
    """ Represents a keyword that can be read or written in a bulk file.

    This class exposes the :attr:`keyword` property that can be read and written as fields of the Keyword record in a bulk file.
    Properties of this class and of classes that it is derived from, correspond to fields of the Keyword record in a bulk file.
    For more information, see Keyword at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, ad_group_id=None, campaign_name=None, ad_group_name=None, keyword=None):
        super(BulkKeyword, self).__init__()
        self._ad_group_id = ad_group_id
        self._keyword = keyword
        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name
        self._quality_score_data = None
        self._bid_suggestions = None

    @property
    def ad_group_id(self):
        """ The identifier of the ad group that contains the keyword.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._ad_group_id

    @ad_group_id.setter
    def ad_group_id(self, ad_group_id):
        self._ad_group_id = ad_group_id

    @property
    def keyword(self):
        """ Defines a keyword within an ad group.

        See Keyword at https://docs.microsoft.com/en-us/bingads/campaign-management-service/keyword?view=bingads-13
        """

        return self._keyword

    @keyword.setter
    def keyword(self, keyword):
        self._keyword = keyword

    @property
    def campaign_name(self):
        """ The name of the campaign that contains the keyword.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @property
    def ad_group_name(self):
        """ The name of the ad group that contains the keyword.

        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """

        return self._ad_group_name

    @ad_group_name.setter
    def ad_group_name(self, ad_group_name):
        self._ad_group_name = ad_group_name

    @property
    def quality_score_data(self):
        """ The quality score data for the keyword.

        :rtype: QualityScoreData
        """

        return self._quality_score_data

    @property
    def bid_suggestions(self):
        """ The bid suggestion data for the keyword.

        :rtype: BidSuggestionData
        """

        return self._bid_suggestions

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.keyword.Status),
            csv_to_field=lambda c, v: csv_to_field_enum(c.keyword, v, 'Status', KeywordStatus)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.keyword.Id),
            csv_to_field=lambda c, v: setattr(
                c.keyword,
                'Id',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.ad_group_id),
            csv_to_field=lambda c, v: setattr(
                c,
                '_ad_group_id',
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
            header=_StringTable.Keyword,
            field_to_csv=lambda c: c.keyword.Text,
            csv_to_field=lambda c, v: setattr(c.keyword, 'Text', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialStatus,
            field_to_csv=lambda c: bulk_str(c.keyword.EditorialStatus),
            csv_to_field=lambda c, v: csv_to_field_enum(c.keyword, v, 'EditorialStatus', KeywordEditorialStatus)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MatchType,
            field_to_csv=lambda c: bulk_str(c.keyword.MatchType),
            csv_to_field=lambda c, v: csv_to_field_enum(c.keyword, v, 'MatchType', MatchType)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DestinationUrl,
            field_to_csv=lambda c: bulk_optional_str(c.keyword.DestinationUrl, c.keyword.Id),
            csv_to_field=lambda c, v: setattr(
                c.keyword,
                'DestinationUrl',
                v if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Bid,
            field_to_csv=lambda c: keyword_bid_bulk_str(c.keyword.Bid, c.keyword.Id),
            csv_to_field=lambda c, v: setattr(
                c.keyword,
                'Bid',
                parse_keyword_bid(v)
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Param1,
            field_to_csv=lambda c: bulk_optional_str(c.keyword.Param1, c.keyword.Id),
            csv_to_field=lambda c, v: setattr(
                c.keyword,
                'Param1',
                v if v else ''
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Param2,
            field_to_csv=lambda c: bulk_optional_str(c.keyword.Param2, c.keyword.Id),
            csv_to_field=lambda c, v: setattr(
                c.keyword,
                'Param2',
                v if v else ''
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Param3,
            field_to_csv=lambda c: bulk_optional_str(c.keyword.Param3, c.keyword.Id),
            csv_to_field=lambda c, v: setattr(
                c.keyword,
                'Param3',
                v if v else ''
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.keyword.FinalUrls, c.keyword.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.keyword.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.keyword.FinalMobileUrls, c.keyword.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.keyword.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_optional_str(c.keyword.TrackingUrlTemplate, c.keyword.Id),
            csv_to_field=lambda c, v: setattr(c.keyword, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.keyword),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.keyword, v)
        ),
        _ComplexBulkMapping(bidding_scheme_to_csv, csv_to_bidding_scheme),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.keyword.FinalUrlSuffix, c.keyword.Id),
            csv_to_field=lambda c, v: setattr(c.keyword, 'FinalUrlSuffix', v if v else None)
        ),
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._keyword, 'keyword')
        self.convert_to_values(row_values, BulkKeyword._MAPPINGS)
        if not exclude_readonly_data:
            QualityScoreData.write_to_row_values_if_not_null(self.quality_score_data, row_values)

    def process_mappings_from_row_values(self, row_values):
        self._keyword = _CAMPAIGN_OBJECT_FACTORY_V13.create('Keyword')
        row_values.convert_to_entity(self, BulkKeyword._MAPPINGS)
        self._quality_score_data = QualityScoreData.read_from_row_values_or_null(row_values)

    def read_additional_data(self, stream_reader):
        success, next_bid_suggestion = stream_reader.try_read(BulkKeywordBidSuggestion)

        while success:
            if self._bid_suggestions is None:
                self._bid_suggestions = BidSuggestionData()

            if isinstance(next_bid_suggestion, BulkKeywordBestPositionBid):
                self._bid_suggestions.best_position = next_bid_suggestion
            elif isinstance(next_bid_suggestion, BulkKeywordMainLineBid):
                self._bid_suggestions.main_line = next_bid_suggestion
            elif isinstance(next_bid_suggestion, BulkKeywordFirstPageBid):
                self._bid_suggestions.first_page = next_bid_suggestion

            success, next_bid_suggestion = stream_reader.try_read(BulkKeywordBidSuggestion)

    def write_additional_data(self, row_writer):
        if self.bid_suggestions is not None:
            BulkKeywordBidSuggestion.write_if_not_null(self.bid_suggestions.best_position, row_writer)
            BulkKeywordBidSuggestion.write_if_not_null(self.bid_suggestions.main_line, row_writer)
            BulkKeywordBidSuggestion.write_if_not_null(self.bid_suggestions.first_page, row_writer)
