from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities.bulk_ad_group_criterion import BulkAdGroupCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
# from bingads.v13.internal.extensions import bulk_str
from bingads.v13.internal.extensions import *

_BiddableAdGroupCriterion = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('BiddableAdGroupCriterion'))

class BulkAdGroupProductPartition(BulkAdGroupCriterion):
    """ Represents an Ad Group Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`ad_group_criterion` property that can be read and written as fields of the
    Ad Group Product Partition record in a bulk file.

    For more information, see Ad Group Product Scope at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 campaign_name=None,
                 ad_group_name=None,
                 ad_group_criterion=None
                 ):
        super(BulkAdGroupProductPartition, self).__init__(campaign_name, ad_group_name, ad_group_criterion)

    @classmethod
    def _write_bid(cls, entity):
        criterion = entity.ad_group_criterion
        if isinstance(criterion, _BiddableAdGroupCriterion) and \
                criterion.CriterionBid is not None:
            return fixed_bid_bulk_str(entity.ad_group_criterion.CriterionBid)

    @classmethod
    def _read_bid(cls, entity, row_value):
        if isinstance(entity.ad_group_criterion, _BiddableAdGroupCriterion):
            entity.ad_group_criterion.CriterionBid = parse_fixed_bid(row_value)
        else:
            pass

    @classmethod
    def _write_destination_url(cls, entity):
        if isinstance(entity.ad_group_criterion, _BiddableAdGroupCriterion):
            return entity.ad_group_criterion.DestinationUrl
        else:
            return None

    @classmethod
    def _get_partition_type(cls, entity):
        if entity.ad_group_criterion.Criterion is not None and \
                hasattr(entity.ad_group_criterion.Criterion, 'PartitionType'):
            return entity.ad_group_criterion.Criterion.PartitionType
        return None

    @classmethod
    def _get_parent_criterion_id(cls, entity):
        if entity.ad_group_criterion.Criterion is not None and \
                hasattr(entity.ad_group_criterion.Criterion, 'ParentCriterionId'):
            return bulk_str(entity.ad_group_criterion.Criterion.ParentCriterionId)
        return None

    @classmethod
    def _get_condition_operand(cls, entity):
        if entity.ad_group_criterion.Criterion is not None and \
                hasattr(entity.ad_group_criterion.Criterion, 'Condition') and \
                entity.ad_group_criterion.Criterion.Condition is not None and \
                hasattr(entity.ad_group_criterion.Criterion.Condition, 'Operand'):
            return entity.ad_group_criterion.Criterion.Condition.Operand
        return None

    @classmethod
    def _get_condition_attribute(cls, entity):
        if entity.ad_group_criterion.Criterion is not None and \
                hasattr(entity.ad_group_criterion.Criterion, 'Condition') and \
                entity.ad_group_criterion.Criterion.Condition is not None and \
                hasattr(entity.ad_group_criterion.Criterion.Condition, 'Attribute'):
            return entity.ad_group_criterion.Criterion.Condition.Attribute
        return None

    @classmethod
    def _read_destination_url(cls, entity, row_value):
        if isinstance(entity.ad_group_criterion, _BiddableAdGroupCriterion):
            entity.ad_group_criterion.DestinationUrl = row_value
        else:
            pass

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.SubType,
            field_to_csv=lambda c: BulkAdGroupProductPartition._get_partition_type(c),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion.Criterion, 'PartitionType', v)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentAdGroupCriterionId,
            field_to_csv=lambda c: BulkAdGroupProductPartition._get_parent_criterion_id(c),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion.Criterion, 'ParentCriterionId',
                                              int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ProductCondition1,
            field_to_csv=lambda c: BulkAdGroupProductPartition._get_condition_operand(c),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion.Criterion.Condition, 'Operand', v)
        ),
        _SimpleBulkMapping(
            _StringTable.ProductValue1,
            field_to_csv=lambda c: BulkAdGroupProductPartition._get_condition_attribute(c),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion.Criterion.Condition, 'Attribute', v)
        ),
        _SimpleBulkMapping(
            _StringTable.DestinationUrl,
            field_to_csv=lambda c: BulkAdGroupProductPartition._write_destination_url(c),
            csv_to_field=lambda c, v: BulkAdGroupProductPartition._read_destination_url(c, v)
        )
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkAdGroupProductPartition, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAdGroupProductPartition._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkAdGroupProductPartition, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAdGroupProductPartition._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupProductPartition, self).read_additional_data(stream_reader)

    def create_criterion(self):
        product_partition = _CAMPAIGN_OBJECT_FACTORY_V13.create('ProductPartition')
        product_partition.Condition = _CAMPAIGN_OBJECT_FACTORY_V13.create('ProductCondition')
        product_partition.Type = 'ProductPartition'
        return product_partition
