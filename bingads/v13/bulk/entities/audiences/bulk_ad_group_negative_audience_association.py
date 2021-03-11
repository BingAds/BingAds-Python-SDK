from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
#from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_negative_criterion import BulkAdGroupNegativeCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *


class BulkAdGroupNegativeAudienceAssociation(BulkAdGroupNegativeCriterion):
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
        super(BulkAdGroupNegativeAudienceAssociation, self).__init__(negative_ad_group_criterion, campaign_name, ad_group_name)
        self._audience_name = audience_name

    _MAPPINGS = [
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
    def audience_name(self):
        """ Defines the name of the Audience

        :rtype: str
        """

        return self._audience_name

    @audience_name.setter
    def audience_name(self, audience_name):
        self._audience_name = audience_name
        
    def create_criterion(self):
        self._negative_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('AudienceCriterion')
        self._negative_ad_group_criterion.Criterion.Type = 'AudienceCriterion'

    def process_mappings_from_row_values(self, row_values):
        super(BulkAdGroupNegativeAudienceAssociation, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAdGroupNegativeAudienceAssociation._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkAdGroupNegativeAudienceAssociation, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAdGroupNegativeAudienceAssociation._MAPPINGS)
    
    def read_additional_data(self, stream_reader):
        super(BulkAdGroupNegativeAudienceAssociation, self).read_additional_data(stream_reader)
