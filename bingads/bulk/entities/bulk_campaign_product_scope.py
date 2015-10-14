from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY
from bingads.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.internal.bulk.string_table import _StringTable
from bingads.bulk.entities.common import _ProductConditionHelper
from bingads.internal.extensions import bulk_str


class BulkCampaignProductScope(_SingleRecordBulkEntity):
    """ Represents a Campaign Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`campaign_criterion` property that can be read and written as fields of the
    Campaign Product Scope record in a bulk file.

    For more information, see Campaign Product Scope at http://go.microsoft.com/fwlink/?LinkId=618643.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 campaign_name=None,
                 status=None,
                 campaign_criterion=None):
        super(BulkCampaignProductScope, self).__init__()

        self._campaign_name = campaign_name
        self._status = status
        self._campaign_criterion = campaign_criterion

    @classmethod
    def _add_product_condition_to_row_values(cls, entity, value):
        criterion = entity.campaign_criterion.Criterion
        if criterion is not None and hasattr(criterion, 'Conditions') and criterion.Conditions is not None and \
                hasattr(criterion.Conditions, 'ProductCondition'):
            return _ProductConditionHelper.add_row_values_from_conditions(criterion.Conditions.ProductCondition, value)
        return None

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.campaign_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.campaign_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.campaign_criterion.CampaignId),
            csv_to_field=lambda c, v: setattr(c.campaign_criterion, 'CampaignId', int(v))
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
                c.campaign_criterion.Criterion.Conditions.ProductCondition
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
    def campaign_criterion(self):
        """ Defines a Campaign Criterion """

        return self._campaign_criterion

    @campaign_criterion.setter
    def campaign_criterion(self, campaign_criterion):
        self._campaign_criterion = campaign_criterion

    def process_mappings_from_row_values(self, row_values):
        self._campaign_criterion = _CAMPAIGN_OBJECT_FACTORY.create('CampaignCriterion')
        self._campaign_criterion.Type = 'CampaignCriterion'
        self._campaign_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY.create('ProductScope')
        self._campaign_criterion.Criterion.Type = 'ProductScope'

        row_values.convert_to_entity(self, BulkCampaignProductScope._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.campaign_criterion, 'campaign_criterion')
        self.convert_to_values(row_values, BulkCampaignProductScope._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignProductScope, self).read_additional_data(stream_reader)
