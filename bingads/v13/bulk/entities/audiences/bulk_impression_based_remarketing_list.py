from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_audience import BulkAudience

class BulkImpressionBasedRemarketingList(BulkAudience):
    """ Represents a Impression Based Remarketing List that can be read or written in a bulk file.

    This class exposes the :attr:`impression_based_remarketing_list` property that can be read and written as fields of the
    Impression Based Remarketing List record in a bulk file.

    For more information, see Impression Based Remarketing List at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 impression_based_remarketing_list=None,
                 status=None,):
        super(BulkImpressionBasedRemarketingList, self).__init__(audience = impression_based_remarketing_list, status = status)

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.ImpressionCampaignId,
            field_to_csv=lambda c: bulk_str(c.impression_based_remarketing_list.CampaignId),
            csv_to_field=lambda c, v: setattr(c.impression_based_remarketing_list, 'CampaignId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ImpressionAdGroupId,
            field_to_csv=lambda c: bulk_str(c.impression_based_remarketing_list.AdGroupId),
            csv_to_field=lambda c, v: setattr(c.impression_based_remarketing_list, 'AdGroupId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EntityType,
            field_to_csv=lambda c: bulk_str(c.impression_based_remarketing_list.EntityType),
            csv_to_field=lambda c, v: setattr(c.impression_based_remarketing_list, 'EntityType', v)
        ),
    ]

    @property
    def impression_based_remarketing_list(self):
        """ Defines a Impression Based Remarketing List """

        return self._audience

    @impression_based_remarketing_list.setter
    def impression_based_remarketing_list(self, impression_based_remarketing_list):
        self._audience = impression_based_remarketing_list

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.impression_based_remarketing_list, 'impression_based_remarketing_list')
        super(BulkImpressionBasedRemarketingList, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkImpressionBasedRemarketingList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.impression_based_remarketing_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('ImpressionBasedRemarketingList')
        super(BulkImpressionBasedRemarketingList, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkImpressionBasedRemarketingList._MAPPINGS)

