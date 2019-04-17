from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *


class BulkAdGroupNegativeAudienceAssociation(_SingleRecordBulkEntity):
    """ Base class for all Ad Group Negative Audience Association subclasses that can be read or written in a bulk file.

    *See also:*

    * :class:`.BulkAdGroupNegativeCustomAudienceAssociation`
    * :class:`.BulkAdGroupNegativeInMarketAudienceAssociation`
    * :class:`.BulkAdGroupNegativeProductAudienceAssociation`
    * :class:`.BulkAdGroupNegativeRemarketingListAssociation`
    * :class:`.BulkAdGroupNegativeSimilarRemarketingListAssociation`
    """

    def __init__(self,
                 negative_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None,
                 audience_name=None):
        super(BulkAdGroupNegativeAudienceAssociation, self).__init__()

        self._negative_ad_group_criterion = negative_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name
        self._audience_name = audience_name

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.negative_ad_group_criterion.Status),
            csv_to_field=lambda c, v: setattr(c.negative_ad_group_criterion, 'Status', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.negative_ad_group_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.negative_ad_group_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.negative_ad_group_criterion.AdGroupId),
            csv_to_field=lambda c, v: setattr(c.negative_ad_group_criterion, 'AdGroupId', int(v) if v else None)
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
            _StringTable.Audience,
            field_to_csv=lambda c: c.audience_name,
            csv_to_field=lambda c, v: setattr(c, 'audience_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.AudienceId,
            field_to_csv=lambda c: field_to_csv_CriterionAudienceId(c.negative_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_CriterionAudienceId(c.negative_ad_group_criterion, int(v) if v else None)
        ),
    ]

    @property
    def negative_ad_group_criterion(self):
        """ Defines a Negative Ad Group Criterion """

        return self._negative_ad_group_criterion

    @negative_ad_group_criterion.setter
    def negative_ad_group_criterion(self, negative_ad_group_criterion):
        self._negative_ad_group_criterion = negative_ad_group_criterion

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
    def audience_name(self):
        """ Defines the name of the Audience

        :rtype: str
        """

        return self._audience_name

    @audience_name.setter
    def audience_name(self, audience_name):
        self._audience_name = audience_name

    def process_mappings_from_row_values(self, row_values):
        self._negative_ad_group_criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeAdGroupCriterion')
        self._negative_ad_group_criterion.Type = 'NegativeAdGroupCriterion'
        self._negative_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('AudienceCriterion')
        self._negative_ad_group_criterion.Criterion.Type = 'AudienceCriterion'
        row_values.convert_to_entity(self, BulkAdGroupNegativeAudienceAssociation._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.negative_ad_group_criterion, 'negative_ad_group_criterion')
        self.convert_to_values(row_values, BulkAdGroupNegativeAudienceAssociation._MAPPINGS)
    
    def read_additional_data(self, stream_reader):
        super(BulkAdGroupNegativeAudienceAssociation, self).read_additional_data(stream_reader)
