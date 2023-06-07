from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.extensions import *

class BulkAudienceGroupAssetGroupAssociation(_SingleRecordBulkEntity):
    """ Represents an audience group asset group association.

    This class exposes the property :attr:`audience_group_asset_group_association` that can be read and written as fields of the audience group asset group association record
    in a bulk file.

    For more information, see audience group asset group association at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None, audience_group_asset_group_association=None):
        super(BulkAudienceGroupAssetGroupAssociation, self).__init__()

        self._status = status
        self._audience_group_asset_group_association = audience_group_asset_group_association
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
    def audience_group_asset_group_association(self):
        """ The AudienceGroupAssetGroupAssociation Data Object of the Campaign Management Service.

        A subset of AudienceGroupAssetGroupAssociation properties are available in the Ad Group record.
        For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._audience_group_asset_group_association

    @audience_group_asset_group_association.setter
    def audience_group_asset_group_association(self, audience_group_asset_group_association):
        self._audience_group_asset_group_association = audience_group_asset_group_association

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.audience_group_asset_group_association.AudienceGroupId),
            csv_to_field=lambda c, v: setattr(c.audience_group_asset_group_association, 'AudienceGroupId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.audience_group_asset_group_association.AssetGroupId),
            csv_to_field=lambda c, v: setattr(c.audience_group_asset_group_association, 'AssetGroupId', int(v) if v else None)
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
    ]


    def process_mappings_from_row_values(self, row_values):
        self.audience_group_asset_group_association = _CAMPAIGN_OBJECT_FACTORY_V13.create('AudienceGroupAssetGroupAssociation')

        row_values.convert_to_entity(self, BulkAudienceGroupAssetGroupAssociation._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._audience_group_asset_group_association, 'AudienceGroupAssetGroupAssociation')
        self.convert_to_values(row_values, BulkAudienceGroupAssetGroupAssociation._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAudienceGroupAssetGroupAssociation, self).read_additional_data(stream_reader)
