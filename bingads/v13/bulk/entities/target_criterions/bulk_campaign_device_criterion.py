from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities.target_criterions.bulk_campaign_biddable_criterion import BulkCampaignBiddableCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *

class BulkCampaignDeviceCriterion(BulkCampaignBiddableCriterion):
    """ Represents an Campaign Device Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_campaign_criterion` property that can be read and written as fields of the
    Campaign Device Criterion record in a bulk file.

    For more information, see Campaign Device Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_campaign_criterion=None,
                 campaign_name=None, ):
        super(BulkCampaignDeviceCriterion, self).__init__(biddable_campaign_criterion, campaign_name)

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Target,
            field_to_csv=lambda c: field_to_csv_DeviceTarget(c.biddable_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_DeviceTarget(c.biddable_campaign_criterion, v)
        ),
        _SimpleBulkMapping(
            _StringTable.OsNames,
            field_to_csv=lambda c: field_to_csv_OSName(c.biddable_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_OSName(c.biddable_campaign_criterion, v)
        ),
    ]

    def create_criterion(self):
        self._biddable_campaign_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('DeviceCriterion')
        self._biddable_campaign_criterion.Criterion.Type = 'DeviceCriterion'
        
    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkCampaignDeviceCriterion, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkCampaignDeviceCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkCampaignDeviceCriterion, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkCampaignDeviceCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignDeviceCriterion, self).read_additional_data(stream_reader)
