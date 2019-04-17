from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.bulk.entities.common import _ProductConditionHelper
from bingads.v13.internal.extensions import bulk_str


class BulkCampaignProductScope(_SingleRecordBulkEntity):
    """ Represents a Campaign Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`campaign_criterion` property that can be read and written as fields of the
    Campaign Product Scope record in a bulk file.

    For more information, see Campaign Product Scope at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 campaign_name=None,
                 status=None,
                 biddable_campaign_criterion=None):
        super(BulkCampaignProductScope, self).__init__()

        self._campaign_name = campaign_name
        self._status = status
        self._biddable_campaign_criterion = biddable_campaign_criterion

    @classmethod
    def _add_product_condition_to_row_values(cls, entity, value):
        criterion = entity.biddable_campaign_criterion.Criterion
        if criterion is not None and hasattr(criterion, 'Conditions') and criterion.Conditions is not None and \
                hasattr(criterion.Conditions, 'ProductCondition'):
            return _ProductConditionHelper.add_row_values_from_conditions(criterion.Conditions.ProductCondition, value)
        return None

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Status,
            field_to_csv=lambda c: c.biddable_campaign_criterion.Status,
            csv_to_field=lambda c, v: setattr(c.biddable_campaign_criterion, 'Status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.biddable_campaign_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.biddable_campaign_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.biddable_campaign_criterion.CampaignId),
            csv_to_field=lambda c, v: setattr(c.biddable_campaign_criterion, 'CampaignId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _ComplexBulkMapping(
            entity_to_csv=lambda c, v: BulkCampaignProductScope._add_product_condition_to_row_values(c, v),
            csv_to_entity=lambda v, c: _ProductConditionHelper.add_conditions_from_row_values(
                v,
                c.biddable_campaign_criterion.Criterion.Conditions.ProductCondition
            )
        )
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
    def biddable_campaign_criterion(self):
        """ Defines a Biddable Campaign Criterion """

        return self._biddable_campaign_criterion

    @biddable_campaign_criterion.setter
    def biddable_campaign_criterion(self, biddable_campaign_criterion):
        self._biddable_campaign_criterion = biddable_campaign_criterion

    def process_mappings_from_row_values(self, row_values):
        self._biddable_campaign_criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('BiddableCampaignCriterion')
        self._biddable_campaign_criterion.Type = 'BiddableCampaignCriterion'
        self._biddable_campaign_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('ProductScope')
        self._biddable_campaign_criterion.Criterion.Type = 'ProductScope'

        row_values.convert_to_entity(self, BulkCampaignProductScope._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.biddable_campaign_criterion, 'biddable_campaign_criterion')
        self.convert_to_values(row_values, BulkCampaignProductScope._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignProductScope, self).read_additional_data(stream_reader)
