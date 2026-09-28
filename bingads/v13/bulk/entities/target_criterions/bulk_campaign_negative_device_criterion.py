from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities.target_criterions.bulk_campaign_negative_criterion import BulkCampaignNegativeCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import (
    csv_to_field_DeviceTarget,
    csv_to_field_OSName,
    field_to_csv_DeviceTarget,
    field_to_csv_OSName,
)


class BulkCampaignNegativeDeviceCriterion(BulkCampaignNegativeCriterion):
    """A campaign negative device criterion in a Bulk file."""

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Target,
            field_to_csv=lambda c: field_to_csv_DeviceTarget(c.negative_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_DeviceTarget(c.negative_campaign_criterion, v)
        ),
        _SimpleBulkMapping(
            _StringTable.OsNames,
            field_to_csv=lambda c: field_to_csv_OSName(c.negative_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_OSName(c.negative_campaign_criterion, v)
        ),
    ]

    def create_criterion(self):
        self._negative_campaign_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('DeviceCriterion')
        self._negative_campaign_criterion.Criterion.Type = 'DeviceCriterion'

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkCampaignNegativeDeviceCriterion, self).process_mappings_to_row_values(
            row_values, exclude_readonly_data
        )
        self.convert_to_values(row_values, BulkCampaignNegativeDeviceCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkCampaignNegativeDeviceCriterion, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkCampaignNegativeDeviceCriterion._MAPPINGS)
