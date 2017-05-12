from bingads.v11.internal.bulk.string_table import _StringTable
from bingads.v11.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v11.internal.bulk.bulk_object import _BulkObject
from bingads.v11.internal.extensions import *

from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V11


class _ProductConditionHelper:
    def __init__(self):
        pass

    MAX_NUMBER_OF_CONDITIONS = 8

    @staticmethod
    def add_conditions_from_row_values(row_values, conditions):
        """

        :param row_values:
        :type row_values: _RowValues
        :param conditions:
        :type conditions: list[ProductCondition]
        :rtype: None
        """

        condition_header_prefix = _StringTable.ProductCondition1[:-1]
        value_header_prefix = _StringTable.ProductValue1[:-1]

        for i in range(1, _ProductConditionHelper.MAX_NUMBER_OF_CONDITIONS + 1):
            condition_success, product_condition = row_values.try_get_value(condition_header_prefix + str(i))
            value_success, product_value = row_values.try_get_value(value_header_prefix + str(i))

            if product_condition and product_value:
                condition = _CAMPAIGN_OBJECT_FACTORY_V11.create('ProductCondition')
                condition.Operand = product_condition
                condition.Attribute = product_value
                conditions.append(condition)

    @staticmethod
    def add_row_values_from_conditions(conditions, row_values):
        """

        :param conditions:
        :type conditions: list[ProductCondition]
        :param row_values:
        :type row_values: _RowValues
        :rtype: None
        """

        condition_header_prefix = _StringTable.ProductCondition1[:-1]
        value_header_prefix = _StringTable.ProductValue1[:-1]

        for i in range(1, len(conditions) + 1):
            row_values[condition_header_prefix + str(i)] = conditions[i - 1].Operand
            row_values[value_header_prefix + str(i)] = conditions[i - 1].Attribute


class PerformanceData(_BulkObject):
    """ Represents a subset of the fields available in bulk records that support historical performance data.

    For example :class:`.BulkKeyword`.
    For more information, see Bulk File Schema at https://go.microsoft.com/fwlink/?linkid=846127.
    """

    def __init__(self):
        self._spend = None
        self._impressions = None
        self._clicks = None
        self._click_through_rate = None
        self._average_cost_per_click = None
        self._average_cost_per_thousand_impressions = None
        self._average_position = None
        self._conversions = None
        self._cost_per_conversion = None

    @property
    def spend(self):
        """ Corresponds to the 'Spend' field in the bulk file.

        :rtype: float
        """

        return self._spend

    @property
    def impressions(self):
        """ Corresponds to the 'Impressions' field in the bulk file.

        :rtype: int
        """

        return self._impressions

    @property
    def clicks(self):
        """ Corresponds to the 'Clicks' field in the bulk file.

        :rtype: int
        """

        return self._clicks

    @property
    def click_through_rate(self):
        """ Corresponds to the 'CTR' field in the bulk file.

        :rtype: float
        """

        return self._click_through_rate

    @property
    def average_cost_per_click(self):
        """ Corresponds to the 'Avg CPC' field in the bulk file.

        :rtype: float
        """

        return self._average_cost_per_click

    @property
    def average_cost_per_thousand_impressions(self):
        """ Corresponds to the 'Avg CPM' field in the bulk file.

        :rtype: float
        """

        return self._average_cost_per_thousand_impressions

    @property
    def average_position(self):
        """ Corresponds to the 'Avg position' field in the bulk file.

        :rtype: float
        """

        return self._average_position

    @property
    def conversions(self):
        """ Corresponds to the 'Conversions' field in the bulk file.

        :rtype: int
        """

        return self._conversions

    @property
    def cost_per_conversion(self):
        """ Corresponds to the 'CPA' field in the bulk file.

        :rtype: float
        """

        return self._cost_per_conversion

    _MAPPINGS = [
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
            field_to_csv=lambda c: bulk_str(c.click_through_rate),
            csv_to_field=lambda c, v: setattr(c, '_click_through_rate', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgCPC,
            field_to_csv=lambda c: bulk_str(c.average_cost_per_click),
            csv_to_field=lambda c, v: setattr(c, '_average_cost_per_click', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgCPM,
            field_to_csv=lambda c: bulk_str(c.average_cost_per_thousand_impressions),
            csv_to_field=lambda c, v: setattr(
                c,
                '_average_cost_per_thousand_impressions',
                float(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.AvgPosition,
            field_to_csv=lambda c: bulk_str(c.average_position),
            csv_to_field=lambda c, v: setattr(c, '_average_position', float(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Conversions,
            field_to_csv=lambda c: bulk_str(c.conversions),
            csv_to_field=lambda c, v: setattr(c, '_conversions', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CPA,
            field_to_csv=lambda c: bulk_str(c.cost_per_conversion),
            csv_to_field=lambda c, v: setattr(c, '_cost_per_conversion', float(v) if v else None)
        )
    ]

    @staticmethod
    def read_from_row_values_or_null(row_values):
        performance_data = PerformanceData()
        performance_data.read_from_row_values(row_values)
        return performance_data if performance_data.has_any_values else None

    @staticmethod
    def write_to_row_values_if_not_null(performance_data, row_values):
        if performance_data is not None:
            performance_data.write_to_row_values(row_values, False)

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, PerformanceData._MAPPINGS)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, PerformanceData._MAPPINGS)

    @property
    def has_any_values(self):
        return \
            self.average_cost_per_click \
            or self.average_cost_per_thousand_impressions \
            or self.average_position \
            or self.click_through_rate \
            or self.clicks \
            or self.conversions \
            or self.cost_per_conversion \
            or self.impressions \
            or self.spend

    def write_to_stream(self, row_writer, exclude_readonly_data):
        pass

    def read_related_data_from_stream(self, stream_reader):
        super(PerformanceData, self).read_related_data_from_stream(stream_reader)

    def enclose_in_multiline_entity(self):
        pass

    @property
    def can_enclose_in_multiline_entity(self):
        return super(PerformanceData, self).can_enclose_in_multiline_entity()


class QualityScoreData(_BulkObject):
    """ Represents a subset of the fields available in bulk records that support quality score data.

    For example :class:`.BulkKeyword`. For more information, see Bulk File Schema at https://go.microsoft.com/fwlink/?linkid=846127.
    """

    def __init__(self):
        self._quality_score = None
        self._keyword_relevance = None
        self._landing_page_relevance = None
        self._landing_page_user_experience = None

    @property
    def quality_score(self):
        """ Corresponds to the 'Quality Score' field in the bulk file.

        :rtype: int
        """

        return self._quality_score

    @property
    def keyword_relevance(self):
        """ Corresponds to the 'Keyword Relevance' field in the bulk file.

        :rtype: int
        """

        return self._keyword_relevance

    @property
    def landing_page_relevance(self):
        """ Corresponds to the 'Landing Page Relevance' field in the bulk file.

        :rtype: int
        """

        return self._landing_page_relevance

    @property
    def landing_page_user_experience(self):
        """ Corresponds to the 'Landing Page User Experience' field in the bulk file.

        :rtype: int
        """

        return self._landing_page_user_experience

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.QualityScore,
            field_to_csv=lambda c: bulk_str(c.quality_score),
            csv_to_field=lambda c, v: setattr(c, '_quality_score', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.KeywordRelevance,
            field_to_csv=lambda c: bulk_str(c.keyword_relevance),
            csv_to_field=lambda c, v: setattr(c, '_keyword_relevance', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.LandingPageRelevance,
            field_to_csv=lambda c: bulk_str(c.landing_page_relevance),
            csv_to_field=lambda c, v: setattr(c, '_landing_page_relevance', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.LandingPageUserExperience,
            field_to_csv=lambda c: bulk_str(c.landing_page_user_experience),
            csv_to_field=lambda c, v: setattr(c, '_landing_page_user_experience', int(v) if v else None)
        ),
    ]

    @staticmethod
    def read_from_row_values_or_null(row_values):
        quality_score_data = QualityScoreData()
        quality_score_data.read_from_row_values(row_values)
        return quality_score_data if quality_score_data.has_any_values else None

    @staticmethod
    def write_to_row_values_if_not_null(quality_score_data, row_values):
        if quality_score_data is not None:
            quality_score_data.write_to_row_values(row_values, False)

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, QualityScoreData._MAPPINGS)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, QualityScoreData._MAPPINGS)

    @property
    def has_any_values(self):
        return \
            self.quality_score \
            or self.keyword_relevance \
            or self.landing_page_relevance \
            or self.landing_page_user_experience

    def write_to_stream(self, row_writer, exclude_readonly_data):
        pass

    def read_related_data_from_stream(self, stream_reader):
        super(QualityScoreData, self).read_related_data_from_stream(stream_reader)

    def enclose_in_multiline_entity(self):
        pass

    @property
    def can_enclose_in_multiline_entity(self):
        return super(QualityScoreData, self).can_enclose_in_multiline_entity()
