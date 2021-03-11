from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *

class BulkCampaignNegativeCriterion(_SingleRecordBulkEntity):
    """ Represents an Campaign Negative Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_campaign_criterion` property that can be read and written as fields of the
    Campaign Negative Criterion record in a bulk file.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 negative_campaign_criterion=None,
                 campaign_name=None, ):
        super(BulkCampaignNegativeCriterion, self).__init__()

        self._negative_campaign_criterion = negative_campaign_criterion
        self._campaign_name = campaign_name

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
    ]

    @property
    def negative_campaign_criterion(self):
        """ Defines a Campaign Criterion """

        return self._negative_campaign_criterion

    @negative_campaign_criterion.setter
    def negative_campaign_criterion(self, negative_campaign_criterion):
        self._negative_campaign_criterion = negative_campaign_criterion

    @property
    def campaign_name(self):
        """ The name of the Campaign

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name
        
    def create_criterion(self):
        raise NotImplementedError()

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.negative_campaign_criterion, 'negative_campaign_criterion')
        self.convert_to_values(row_values, BulkCampaignNegativeCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._negative_campaign_criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeCampaignCriterion')
        self._negative_campaign_criterion.Type = 'NegativeCampaignCriterion'
        self.create_criterion()
        row_values.convert_to_entity(self, BulkCampaignNegativeCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignNegativeCriterion, self).read_additional_data(stream_reader)
