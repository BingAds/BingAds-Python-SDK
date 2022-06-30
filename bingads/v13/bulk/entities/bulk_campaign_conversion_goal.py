from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


class BulkCampaignConversionGoal(_SingleRecordBulkEntity):
    """ Represents a CampaignConversionGoal.

    Properties of this class and of classes that it is derived from, correspond to fields of the CampaignConversionGoal record in a bulk file.
    For more information, see CampaignConversionGoal at https://go.microsoft.com/fwlink/?linkid=846127
    
    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, campaign_conversion_goal = None):
        super(BulkCampaignConversionGoal, self).__init__()
        self._campaign_conversion_goal = campaign_conversion_goal


    @property
    def campaign_conversion_goal(self):
        """ define a campaign conversion goal association

        :rtype: CampaignConversionGoal
        """
        return self._campaign_conversion_goal

    @campaign_conversion_goal.setter
    def campaign_conversion_goal(self, value):
        self._campaign_conversion_goal = value        


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.campaign_conversion_goal.CampaignId),
            csv_to_field=lambda c, v: setattr(c.campaign_conversion_goal, 'CampaignId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.GoalId,
            field_to_csv=lambda c: bulk_str(c.campaign_conversion_goal.GoalId),
            csv_to_field=lambda c, v: setattr(c.campaign_conversion_goal, 'GoalId', int(v) if v else None)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self._campaign_conversion_goal = _CAMPAIGN_OBJECT_FACTORY_V13.create('CampaignConversionGoal')
        row_values.convert_to_entity(self, BulkCampaignConversionGoal._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkCampaignConversionGoal._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignConversionGoal, self).read_additional_data(stream_reader)
