from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.bulk.entities.target_criterions.bulk_campaign_negative_criterion import BulkCampaignNegativeCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *

class BulkCampaignNegativeLocationCriterion(BulkCampaignNegativeCriterion):
    """ Represents an Campaign Negative Location Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_campaign_criterion` property that can be read and written as fields of the
    Campaign Negative Location Criterion record in a bulk file.

    For more information, see Campaign Negative Location Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 negative_campaign_criterion=None,
                 campaign_name=None, ):
        super(BulkCampaignNegativeLocationCriterion, self).__init__(negative_campaign_criterion, campaign_name)


    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Target,
            field_to_csv=lambda c: field_to_csv_LocationTarget(c.negative_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_LocationTarget(c.negative_campaign_criterion, int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.SubType,
            field_to_csv=lambda c: field_to_csv_LocationType(c.negative_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_LocationType(c.negative_campaign_criterion, v)
        ),
        _SimpleBulkMapping(
            _StringTable.Name,
            field_to_csv=lambda c: field_to_csv_LocationName(c.negative_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_LocationName(c.negative_campaign_criterion, v)
        ),
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkCampaignNegativeLocationCriterion, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkCampaignNegativeLocationCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkCampaignNegativeLocationCriterion, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkCampaignNegativeLocationCriterion._MAPPINGS)
        
    def create_criterion(self):
        self._negative_campaign_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('LocationCriterion')
        self._negative_campaign_criterion.Criterion.Type = 'LocationCriterion'

    def read_additional_data(self, stream_reader):
        super(BulkCampaignNegativeLocationCriterion, self).read_additional_data(stream_reader)
