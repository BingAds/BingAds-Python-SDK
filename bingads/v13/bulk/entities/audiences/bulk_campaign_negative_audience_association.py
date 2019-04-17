from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *


class BulkCampaignNegativeAudienceAssociation(_SingleRecordBulkEntity):
    """ Base class for all Campaign Negative Audience Association subclasses that can be read or written in a bulk file.

    *See also:*

    * :class:`.BulkCampaignNegativeCustomAudienceAssociation`
    * :class:`.BulkCampaignNegativeInMarketAudienceAssociation`
    * :class:`.BulkCampaignNegativeProductAudienceAssociation`
    * :class:`.BulkCampaignNegativeRemarketingListAssociation`
    * :class:`.BulkCampaignNegativeSimilarRemarketingListAssociation`
    """

    def __init__(self,
                 negative_campaign_criterion=None,
                 campaign_name=None,
                 audience_name=None):
        super(BulkCampaignNegativeAudienceAssociation, self).__init__()

        self._negative_campaign_criterion = negative_campaign_criterion
        self._campaign_name = campaign_name
        self._audience_name = audience_name

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.negative_campaign_criterion.Status),
            csv_to_field=lambda c, v: setattr(c.negative_campaign_criterion, 'Status', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.negative_campaign_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.negative_campaign_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.negative_campaign_criterion.CampaignId),
            csv_to_field=lambda c, v: setattr(c.negative_campaign_criterion, 'CampaignId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Audience,
            field_to_csv=lambda c: c.audience_name,
            csv_to_field=lambda c, v: setattr(c, 'audience_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.AudienceId,
            field_to_csv=lambda c: field_to_csv_CriterionAudienceId(c.negative_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_CriterionAudienceId(c.negative_campaign_criterion, int(v) if v else None)
        ),
    ]

    @property
    def negative_campaign_criterion(self):
        """ Defines a Negative Campaign Criterion """

        return self._negative_campaign_criterion

    @negative_campaign_criterion.setter
    def negative_campaign_criterion(self, negative_campaign_criterion):
        self._negative_campaign_criterion = negative_campaign_criterion

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
    def audience_name(self):
        """ Defines the name of the Audience

        :rtype: str
        """

        return self._audience_name

    @audience_name.setter
    def audience_name(self, audience_name):
        self._audience_name = audience_name

    def process_mappings_from_row_values(self, row_values):
        self._negative_campaign_criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeCampaignCriterion')
        self._negative_campaign_criterion.Type = 'NegativeCampaignCriterion'
        self._negative_campaign_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('AudienceCriterion')
        self._negative_campaign_criterion.Criterion.Type = 'AudienceCriterion'
        row_values.convert_to_entity(self, BulkCampaignNegativeAudienceAssociation._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.negative_campaign_criterion, 'negative_campaign_criterion')
        self.convert_to_values(row_values, BulkCampaignNegativeAudienceAssociation._MAPPINGS)
    
    def read_additional_data(self, stream_reader):
        super(BulkCampaignNegativeAudienceAssociation, self).read_additional_data(stream_reader)
