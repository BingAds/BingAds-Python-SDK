from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkAssetGroupSearchTheme(_SingleRecordBulkEntity):
    """ Represents an asset group search theme.

    This class exposes the property :attr:`asset_group_search_theme` that can be read and written as fields of the asset group search theme record
    in a bulk file.

    For more information, see asset group search theme at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, asset_group_id=None, asset_group_search_theme=None):
        super(BulkAssetGroupSearchTheme, self).__init__()

        self._asset_group_search_theme = asset_group_search_theme
        self._asset_group_id = asset_group_id

    @property
    def asset_group_search_theme(self):
        """ The AssetGroupSearchTheme Data Object of the Campaign Management Service.

        A subset of AssetGroupSearchTheme properties are available in the Ad Group record.
        For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._asset_group_search_theme

    @asset_group_search_theme.setter
    def asset_group_search_theme(self, asset_group_search_theme):
        self._asset_group_search_theme = asset_group_search_theme

    @property
    def asset_group_id(self):
        """ The identifier of the asset group that contains the search theme.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._asset_group_id

    @asset_group_id.setter
    def asset_group_id(self, asset_group_id):
        self._asset_group_id = asset_group_id


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.asset_group_search_theme.Id),
            csv_to_field=lambda c, v: setattr(c.asset_group_search_theme, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.asset_group_id),
            csv_to_field=lambda c, v: setattr(c, 'asset_group_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SearchTheme,
            field_to_csv=lambda c: bulk_str(c.asset_group_search_theme.SearchTheme),
            csv_to_field=lambda c, v: setattr(c.asset_group_search_theme, 'SearchTheme', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.asset_group_search_theme = _CAMPAIGN_OBJECT_FACTORY_V13.create('AssetGroupSearchTheme')

        row_values.convert_to_entity(self, BulkAssetGroupSearchTheme._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._asset_group_search_theme, 'AssetGroupSearchTheme')
        self.convert_to_values(row_values, BulkAssetGroupSearchTheme._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAssetGroupSearchTheme, self).read_additional_data(stream_reader)
