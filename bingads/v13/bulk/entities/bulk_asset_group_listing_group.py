from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.extensions import *

class BulkAssetGroupListingGroup(_SingleRecordBulkEntity):
    """ Represents an asset group listing group.

    This class exposes the property :attr:`asset_group_listing_group` that can be read and written as fields of the Asset Group Listing Group record
    in a bulk file.

    For more information, see Asset Group at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, asset_group_listing_group=None):
        super(BulkAssetGroupListingGroup, self).__init__()

        self._status = status
        self._asset_group_listing_group = asset_group_listing_group
        self._asset_group_name = None
        self._campaign_name = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def asset_group_name(self):
        return self._asset_group_name

    @asset_group_name.setter
    def asset_group_name(self, asset_group_name):
        self._asset_group_name = asset_group_name

    @property
    def campaign_name(self):
        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @property
    def asset_group_listing_group(self):
        """ The AssetGroupListingGroup Data Object of the Campaign Management Service.

        A subset of AssetGroupListingGroup properties are available in the Ad Group record.
        For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._asset_group_listing_group

    @asset_group_listing_group.setter
    def asset_group_listing_group(self, asset_group_listing_group):
        self._asset_group_listing_group = asset_group_listing_group

    @classmethod
    def _get_condition_operand(cls, entity):
        if entity.asset_group_listing_group is not None and \
                hasattr(entity.asset_group_listing_group, 'Dimension') and \
                entity.asset_group_listing_group.Dimension is not None and \
                hasattr(entity.asset_group_listing_group.Dimension, 'Operand'):
            return entity.asset_group_listing_group.Dimension.Operand
        return None

    @classmethod
    def _get_condition_attribute(cls, entity):
        if entity.asset_group_listing_group is not None and \
                hasattr(entity.asset_group_listing_group, 'Dimension') and \
                entity.asset_group_listing_group.Dimension is not None and \
                hasattr(entity.asset_group_listing_group.Dimension, 'Attribute'):
            return entity.asset_group_listing_group.Dimension.Attribute
        return None

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.asset_group_listing_group.Id),
            csv_to_field=lambda c, v: setattr(c.asset_group_listing_group, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.asset_group_listing_group.AssetGroupId),
            csv_to_field=lambda c, v: setattr(c.asset_group_listing_group, 'AssetGroupId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AssetGroup,
            field_to_csv=lambda c: c.asset_group_name,
            csv_to_field=lambda c, v: setattr(c, 'asset_group_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.IsExcluded,
            field_to_csv=lambda c: bulk_str(c.asset_group_listing_group.IsExcluded),
            csv_to_field=lambda c, v: setattr(c.asset_group_listing_group, 'IsExcluded', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentListingGroupId,
            field_to_csv=lambda c: bulk_str(c.asset_group_listing_group.ParentListingGroupId),
            csv_to_field=lambda c, v: setattr(c.asset_group_listing_group, 'ParentListingGroupId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SubType,
            field_to_csv=lambda c: bulk_str(c.asset_group_listing_group.AssetGroupListingType),
            csv_to_field=lambda c, v: setattr(c.asset_group_listing_group, 'AssetGroupListingType', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ProductCondition1,
            field_to_csv=lambda c: BulkAssetGroupListingGroup._get_condition_operand(c),
            csv_to_field=lambda c, v: setattr(c.asset_group_listing_group.Dimension, 'Operand', v)
        ),
        _SimpleBulkMapping(
            _StringTable.ProductValue1,
            field_to_csv=lambda c: BulkAssetGroupListingGroup._get_condition_attribute(c),
            csv_to_field=lambda c, v: setattr(c.asset_group_listing_group.Dimension, 'Attribute', v)
        ),
    ]


    def process_mappings_from_row_values(self, row_values):
        self.asset_group_listing_group = _CAMPAIGN_OBJECT_FACTORY_V13.create('AssetGroupListingGroup')

        row_values.convert_to_entity(self, BulkAssetGroupListingGroup._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._asset_group_listing_group, 'AssetGroupListingGroup')
        self.convert_to_values(row_values, BulkAssetGroupListingGroup._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAssetGroupListingGroup, self).read_additional_data(stream_reader)
