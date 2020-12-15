from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *


class BulkCampaignNegativeStoreCriterion(_SingleRecordBulkEntity):
    """ Represents a Campaign Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_campaign_criterion` property that can be read and written as fields of the
    Campaign Negative Store Criterion record in a bulk file.

    For more information, see Campaign Negative Store Criterion at https://go.microsoft.com/fwlink/?linkid=836839.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 campaign_name=None,
                 status=None,
                 negative_campaign_criterion=None):
        super(BulkCampaignNegativeStoreCriterion, self).__init__()

        self._campaign_name = campaign_name
        self._status = status
        self._negative_campaign_criterion = negative_campaign_criterion


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.negative_campaign_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.negative_campaign_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.negative_campaign_criterion.CampaignId),
            csv_to_field=lambda c, v: setattr(c.negative_campaign_criterion, 'CampaignId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MerchantCenterId,
            field_to_csv=lambda c: bulk_str(c.negative_campaign_criterion.Criterion.StoreId),
            csv_to_field=lambda c, v: setattr(c.negative_campaign_criterion.Criterion,'StoreId', int(v) if v else None)
        ),
    ]

    @property
    def campaign_name(self):
        """ The name of the Campaign

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @property
    def status(self):
        """ The status of the Campaign Criterion

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def negative_campaign_criterion(self):
        """ Defines a Campaign Criterion """

        return self._negative_campaign_criterion

    @negative_campaign_criterion.setter
    def negative_campaign_criterion(self, negative_campaign_criterion):
        self._negative_campaign_criterion = negative_campaign_criterion

    def process_mappings_from_row_values(self, row_values):
        self._negative_campaign_criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeCampaignCriterion')
        self._negative_campaign_criterion.Type = 'NegativeCampaignCriterion'
        self._negative_campaign_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('StoreCriterion')
        self._negative_campaign_criterion.Criterion.Type = 'StoreCriterion'

        row_values.convert_to_entity(self, BulkCampaignNegativeStoreCriterion._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.negative_campaign_criterion, 'negative_campaign_criterion')
        self.convert_to_values(row_values, BulkCampaignNegativeStoreCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignNegativeStoreCriterion, self).read_additional_data(stream_reader)
