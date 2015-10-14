from bingads.v10.bulk.entities import PerformanceData

from bingads.v10.internal.bulk.bulk_object import _BulkObject
from bingads.v10.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v10.internal.bulk.string_table import _StringTable
from bingads.internal.extensions import *


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

        For more information, see Keyword Best Position Bid at http://go.microsoft.com/fwlink/?LinkID=620266.

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

        For more information, see Keyword Main Line Bid at http://go.microsoft.com/fwlink/?LinkID=620267.

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

        For more information, see Keyword First Page Bid at http://go.microsoft.com/fwlink/?LinkID=620268.

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

    @property
    def performance_data(self):
        """ The historical performance data corresponding to the suggested bid.

        :rtype: PerformanceData
        """

        return self._performance_data

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
        self._performance_data = PerformanceData.read_from_row_values(row_values)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkKeywordBidSuggestion._MAPPINGS)
        if not exclude_readonly_data:
            PerformanceData.write_to_row_values_if_not_null(self.performance_data, row_values)

    @staticmethod
    def write_if_not_null(keyword_bid_suggestion, row_writer):
        if keyword_bid_suggestion is not None:
            row_writer.write_object_row(keyword_bid_suggestion)


class BulkKeywordBestPositionBid(BulkKeywordBidSuggestion):
    pass


class BulkKeywordFirstPageBid(BulkKeywordBidSuggestion):
    pass


class BulkKeywordMainLineBid(BulkKeywordBidSuggestion):
    pass
