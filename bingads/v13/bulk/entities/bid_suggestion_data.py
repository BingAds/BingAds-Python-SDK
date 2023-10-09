from bingads.v13.internal.bulk.bulk_object import _BulkObject
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *


class BidSuggestionData:
    """ The best position, main line, and first page bid suggestion data corresponding to one keyword.

    If the requested DataScope includes BidSuggestionsData, the download will include bulk records corresponding to the
    properties of this class.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    """

    def __init__(self):
        self._best_position = None
        self._main_line = None
        self._first_page = None

    @property
    def best_position(self):
        """ Represents a best position bid suggestion that is derived from :class:`_BulkObject`.

        It can only be read from a bulk file by the :class:`.BulkFileReader` when reading the
        corresponding :class:`.BulkKeyword`. An instance of this class can represent
        a single best position bid, and thus one record in the bulk file. Properties of this class and of classes that
        it is derived from, correspond to fields of the Keyword Best Position Bid record in a bulk file.

        For more information, see Keyword Best Position Bid at https://go.microsoft.com/fwlink/?linkid=846127.

        :return: The best position bid suggestion.
        :rtype: BulkKeywordBidSuggestion
        """

        return self._best_position

    @best_position.setter
    def best_position(self, best_position):
        self._best_position = best_position

    @property
    def main_line(self):
        """ Represents a main line bid suggestion that is derived from :class:`_BulkObject`.

        It can only be read from a bulk file by the :class:`BulkFileReader` when reading the corresponding
        :class:`BulkKeyword`. An instance of this class can represent a single main line bid, and thus one record in
        the bulk file. Properties of this class and of classes that it is derived from, correspond to fields of the
        Keyword Main Line Bid record in a bulk file.

        For more information, see Keyword Main Line Bid at https://go.microsoft.com/fwlink/?linkid=846127.

        :return: The main line bid suggestion.
        :rtype: BulkKeywordBidSuggestion
        """

        return self._main_line

    @main_line.setter
    def main_line(self, main_line):
        self._main_line = main_line

    @property
    def first_page(self):
        """ Represents a first page bid suggestion that is derived from :class:`_BulkObject`. can only be read from a bulk
        file by the :class:`BulkFileReader` when reading the corresponding :class:`BulkKeyword`. An instance of this
        class can represent a single first page bid, and thus one record in the bulk file. Properties of this class and
        of classes that it is derived from, correspond to fields of the Keyword First Page Bid record in a bulk file.

        For more information, see Keyword First Page Bid at https://go.microsoft.com/fwlink/?linkid=846127.

        :return: The first page bid suggestion.
        :rtype: BulkKeywordBidSuggestion
        """

        return self._first_page

    @first_page.setter
    def first_page(self, first_page):
        self._first_page = first_page


class BulkKeywordBidSuggestion(_BulkObject):
    """ Represents a best position bid suggestion.

    It can only be read from a bulk file by the :class:`.BulkFileReader` when reading the corresponding :class:`.BulkKeyword`.
    An instance of this class can represent a single keyword bid position, and thus one record in the bulk file.
    """

    def __init__(self):
        self._keyword_text = None
        self._bid = None
        self._performance_data = None

    @property
    def keyword_text(self):
        """ The keyword corresponding to the suggested bid.

        Corresponds to the 'Keyword' field in the bulk file.
        :rtype: str
        """

        return self._keyword_text

    @property
    def bid(self):
        """ The suggested bid for the keyword.

        :rtype: float
        """

        return self._bid

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Keyword,
            field_to_csv=lambda c: bulk_str(c.keyword_text),
            csv_to_field=lambda c, v: setattr(c, '_keyword_text', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Bid,
            field_to_csv=lambda c: bulk_str(c.bid),
            csv_to_field=lambda c, v: setattr(c, '_bid', float(v) if v else None)
        ),
    ]

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkKeywordBidSuggestion._MAPPINGS)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkKeywordBidSuggestion._MAPPINGS)

    @staticmethod
    def write_if_not_null(keyword_bid_suggestion, row_writer):
        if keyword_bid_suggestion is not None:
            row_writer.write_object_row(keyword_bid_suggestion)


class BulkKeywordBestPositionBid(BulkKeywordBidSuggestion):
    def __init__(self):
        super().__init__()
        self._spend = None
        self._impressions = None
        self._clicks = None
        self._ctr = None
        self._avgcpc = None
        self._avgcpm = None
        self._avgposition = None
        self._conversions = None
        self._cpa = None

    @property
    def keyword_text(self):
        """ The keyword corresponding to the suggested bid.

        Corresponds to the 'Keyword' field in the bulk file.
        :rtype: str
        """

        return self._keyword_text

    @property
    def bid(self):
        """ The suggested bid value for the best position in search results.

        :rtype: float
        """

        return self._bid

    @property
    def spend(self):
        """ The estimated average cost per week.

        :rtype: float
        """
        return self._spend

    @property
    def impressions(self):
        """ The estimated average number of impressions per week.

        :rtype: int
        """
        return self._impressions

    @property
    def clicks(self):
        """ The estimated average number of clicks per week.

        :rtype: int
        """
        return self._clicks

    @property
    def ctr(self):
        """ The estimated CTR.
            The formula used to calculate the CTR is (maximum number of clicks / maximum number of impressions) * 100.

        :rtype: float
        """
        return self._ctr

    @property
    def avgcpc(self):
        """ The estimated average CPC.
            The formula used to calculate the average CPC is (maximum total cost / maximum number of clicks).

        :rtype: float
        """
        return self._avgcpc

    @property
    def avgcpm(self):
        """ The average of the cost per thousand impressions (CPM) of the ad.
            The value will be 0 (zero) if the ad group to which the ad belongs does not specify the
            Content ad distribution medium or if the user does not belong to the CPM pilot program.

        :rtype: float
        """
        return self._avgcpm

    @property
    def avgposition(self):
        """ The position in the search results given the specified bid.

        :rtype: float
        """
        return self._avgposition

    @property
    def conversions(self):
        """ The estimated number of conversions per week.

        :rtype: float
        """
        return self._conversions

    @property
    def cpa(self):
        """ The estimated cost per conversion.
            The formula for calculating the cost per conversion is (spend / conversions).

        :rtype: float
        """
        return self._cpa

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkKeywordBestPositionBid._MAPPINGS)

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Keyword,
            field_to_csv=lambda c: bulk_str(c.keyword_text),
            csv_to_field=lambda c, v: setattr(c, '_keyword_text', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Bid,
            field_to_csv=lambda c: bulk_str(c.bid),
            csv_to_field=lambda c, v: setattr(c, '_bid', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Spend,
            field_to_csv=lambda c: bulk_str(c.spend),
            csv_to_field=lambda c, v: setattr(c, '_spend', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Impressions,
            field_to_csv=lambda c: bulk_str(c.impressions),
            csv_to_field=lambda c, v: setattr(c, '_impressions', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Clicks,
            field_to_csv=lambda c: bulk_str(c.clicks),
            csv_to_field=lambda c, v: setattr(c, '_clicks', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CTR,
            field_to_csv=lambda c: bulk_str(c.ctr),
            csv_to_field=lambda c, v: setattr(c, '_ctr', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgCPC,
            field_to_csv=lambda c: bulk_str(c.avgcpc),
            csv_to_field=lambda c, v: setattr(c, '_avgcpc', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgCPM,
            field_to_csv=lambda c: bulk_str(c.avgcpm),
            csv_to_field=lambda c, v: setattr(c, '_avgcpm', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgPosition,
            field_to_csv=lambda c: bulk_str(c.avgposition),
            csv_to_field=lambda c, v: setattr(c, '_avgposition', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Conversions,
            field_to_csv=lambda c: bulk_str(c.conversions),
            csv_to_field=lambda c, v: setattr(c, '_conversions', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CPA,
            field_to_csv=lambda c: bulk_str(c.cpa),
            csv_to_field=lambda c, v: setattr(c, '_cpa', float(v) if v else None)
        ),

    ]

    def read_related_data_from_stream(self, stream_reader):
        return super(BulkKeywordBestPositionBid, self).read_related_data_from_stream(stream_reader)

    def write_to_stream(self, row_writer, exclude_readonly_data):
        return super(BulkKeywordBestPositionBid, self).write_to_stream(row_writer, exclude_readonly_data)

    @property
    def can_enclose_in_multiline_entity(self):
        return super(BulkKeywordBestPositionBid, self).can_enclose_in_multiline_entity

    def enclose_in_multiline_entity(self):
        return super(BulkKeywordBestPositionBid, self).enclose_in_multiline_entity()


class BulkKeywordFirstPageBid(BulkKeywordBidSuggestion):
    def __init__(self):
        super().__init__()
        self._spend = None
        self._impressions = None
        self._clicks = None
        self._ctr = None
        self._avgcpc = None
        self._avgcpm = None
        self._avgposition = None
        self._conversions = None
        self._cpa = None

    @property
    def keyword_text(self):
        """ The keyword corresponding to the suggested bid.

        Corresponds to the 'Keyword' field in the bulk file.
        :rtype: str
        """

        return self._keyword_text

    @property
    def bid(self):
        """ The suggested bid value for first page side bar positioning in search results.

        :rtype: float
        """

        return self._bid

    @property
    def spend(self):
        """ The estimated average cost per week.

        :rtype: float
        """
        return self._spend

    @property
    def impressions(self):
        """ The estimated average number of impressions per week.

        :rtype: int
        """
        return self._impressions

    @property
    def clicks(self):
        """ The estimated average number of clicks per week.

        :rtype: int
        """
        return self._clicks

    @property
    def ctr(self):
        """ The estimated CTR.
            The formula used to calculate the CTR is (maximum number of clicks / maximum number of impressions) * 100.

        :rtype: float
        """
        return self._ctr

    @property
    def avgcpc(self):
        """ The estimated average CPC.
            The formula used to calculate the average CPC is (maximum total cost / maximum number of clicks).

        :rtype: float
        """
        return self._avgcpc

    @property
    def avgcpm(self):
        """ The average of the cost per thousand impressions (CPM) of the ad.
            The value will be 0 (zero) if the ad group to which the ad belongs does not specify the
            Content ad distribution medium or if the user does not belong to the CPM pilot program.

        :rtype: float
        """
        return self._avgcpm

    @property
    def avgposition(self):
        """ The position in the search results given the specified bid.

        :rtype: float
        """
        return self._avgposition

    @property
    def conversions(self):
        """ The estimated number of conversions per week.

        :rtype: float
        """
        return self._conversions

    @property
    def cpa(self):
        """ The estimated cost per conversion.
            The formula for calculating the cost per conversion is (spend / conversions).

        :rtype: float
        """
        return self._cpa

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkKeywordFirstPageBid._MAPPINGS)

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Keyword,
            field_to_csv=lambda c: bulk_str(c.keyword_text),
            csv_to_field=lambda c, v: setattr(c, '_keyword_text', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Bid,
            field_to_csv=lambda c: bulk_str(c.bid),
            csv_to_field=lambda c, v: setattr(c, '_bid', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Spend,
            field_to_csv=lambda c: bulk_str(c.spend),
            csv_to_field=lambda c, v: setattr(c, '_spend', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Impressions,
            field_to_csv=lambda c: bulk_str(c.impressions),
            csv_to_field=lambda c, v: setattr(c, '_impressions', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Clicks,
            field_to_csv=lambda c: bulk_str(c.clicks),
            csv_to_field=lambda c, v: setattr(c, '_clicks', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CTR,
            field_to_csv=lambda c: bulk_str(c.ctr),
            csv_to_field=lambda c, v: setattr(c, '_ctr', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgCPC,
            field_to_csv=lambda c: bulk_str(c.avgcpc),
            csv_to_field=lambda c, v: setattr(c, '_avgcpc', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgCPM,
            field_to_csv=lambda c: bulk_str(c.avgcpm),
            csv_to_field=lambda c, v: setattr(c, '_avgcpm', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgPosition,
            field_to_csv=lambda c: bulk_str(c.avgposition),
            csv_to_field=lambda c, v: setattr(c, '_avgposition', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Conversions,
            field_to_csv=lambda c: bulk_str(c.conversions),
            csv_to_field=lambda c, v: setattr(c, '_conversions', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CPA,
            field_to_csv=lambda c: bulk_str(c.cpa),
            csv_to_field=lambda c, v: setattr(c, '_cpa', float(v) if v else None)
        ),

    ]

    def read_related_data_from_stream(self, stream_reader):
        return super(BulkKeywordFirstPageBid, self).read_related_data_from_stream(stream_reader)

    def write_to_stream(self, row_writer, exclude_readonly_data):
        return super(BulkKeywordFirstPageBid, self).write_to_stream(row_writer, exclude_readonly_data)

    @property
    def can_enclose_in_multiline_entity(self):
        return super(BulkKeywordFirstPageBid, self).can_enclose_in_multiline_entity

    def enclose_in_multiline_entity(self):
        return super(BulkKeywordFirstPageBid, self).enclose_in_multiline_entity()


class BulkKeywordMainLineBid(BulkKeywordBidSuggestion):
    def __init__(self):
        super().__init__()
        self._spend = None
        self._impressions = None
        self._clicks = None
        self._ctr = None
        self._avgcpc = None
        self._avgcpm = None
        self._avgposition = None
        self._conversions = None
        self._cpa = None

    @property
    def keyword_text(self):
        """ The keyword corresponding to the suggested bid.

        Corresponds to the 'Keyword' field in the bulk file.
        :rtype: str
        """

        return self._keyword_text

    @property
    def bid(self):
        """ The suggested bid value for main line positioning in search results.

        :rtype: float
        """

        return self._bid

    @property
    def spend(self):
        """ The estimated average cost per week.

        :rtype: float
        """
        return self._spend

    @property
    def impressions(self):
        """ The estimated average number of impressions per week.

        :rtype: int
        """
        return self._impressions

    @property
    def clicks(self):
        """ The estimated average number of clicks per week.

        :rtype: int
        """
        return self._clicks

    @property
    def ctr(self):
        """ The estimated CTR.
            The formula used to calculate the CTR is (maximum number of clicks / maximum number of impressions) * 100.

        :rtype: float
        """
        return self._ctr

    @property
    def avgcpc(self):
        """ The estimated average CPC.
            The formula used to calculate the average CPC is (maximum total cost / maximum number of clicks).

        :rtype: float
        """
        return self._avgcpc

    @property
    def avgcpm(self):
        """ The average of the cost per thousand impressions (CPM) of the ad.
            The value will be 0 (zero) if the ad group to which the ad belongs does not specify the
            Content ad distribution medium or if the user does not belong to the CPM pilot program.

        :rtype: float
        """
        return self._avgcpm

    @property
    def avgposition(self):
        """ The position in the search results given the specified bid.

        :rtype: float
        """
        return self._avgposition

    @property
    def conversions(self):
        """ The estimated number of conversions per week.

        :rtype: float
        """
        return self._conversions

    @property
    def cpa(self):
        """ The estimated cost per conversion.
            The formula for calculating the cost per conversion is (spend / conversions).

        :rtype: float
        """
        return self._cpa

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkKeywordMainLineBid._MAPPINGS)

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Keyword,
            field_to_csv=lambda c: bulk_str(c.keyword_text),
            csv_to_field=lambda c, v: setattr(c, '_keyword_text', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Bid,
            field_to_csv=lambda c: bulk_str(c.bid),
            csv_to_field=lambda c, v: setattr(c, '_bid', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Spend,
            field_to_csv=lambda c: bulk_str(c.spend),
            csv_to_field=lambda c, v: setattr(c, '_spend', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Impressions,
            field_to_csv=lambda c: bulk_str(c.impressions),
            csv_to_field=lambda c, v: setattr(c, '_impressions', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Clicks,
            field_to_csv=lambda c: bulk_str(c.clicks),
            csv_to_field=lambda c, v: setattr(c, '_clicks', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CTR,
            field_to_csv=lambda c: bulk_str(c.ctr),
            csv_to_field=lambda c, v: setattr(c, '_ctr', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgCPC,
            field_to_csv=lambda c: bulk_str(c.avgcpc),
            csv_to_field=lambda c, v: setattr(c, '_avgcpc', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgCPM,
            field_to_csv=lambda c: bulk_str(c.avgcpm),
            csv_to_field=lambda c, v: setattr(c, '_avgcpm', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgPosition,
            field_to_csv=lambda c: bulk_str(c.avgposition),
            csv_to_field=lambda c, v: setattr(c, '_avgposition', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Conversions,
            field_to_csv=lambda c: bulk_str(c.conversions),
            csv_to_field=lambda c, v: setattr(c, '_conversions', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CPA,
            field_to_csv=lambda c: bulk_str(c.cpa),
            csv_to_field=lambda c, v: setattr(c, '_cpa', float(v) if v else None)
        ),

    ]

    def read_related_data_from_stream(self, stream_reader):
        return super(BulkKeywordMainLineBid, self).read_related_data_from_stream(stream_reader)

    def write_to_stream(self, row_writer, exclude_readonly_data):
        return super(BulkKeywordMainLineBid, self).write_to_stream(row_writer, exclude_readonly_data)

    @property
    def can_enclose_in_multiline_entity(self):
        return super(BulkKeywordMainLineBid, self).can_enclose_in_multiline_entity

    def enclose_in_multiline_entity(self):
        return super(BulkKeywordMainLineBid, self).enclose_in_multiline_entity()
