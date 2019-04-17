from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.bulk_object import _BulkObject
from bingads.v13.internal.extensions import *

from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13


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
                condition = _CAMPAIGN_OBJECT_FACTORY_V13.create('ProductCondition')
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
