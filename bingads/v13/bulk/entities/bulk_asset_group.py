from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.extensions import *

class BulkAssetGroup(_SingleRecordBulkEntity):
    """ Represents an asset group.

    This class exposes the property :attr:`asset_group` that can be read and written as fields of the Asset Group record
    in a bulk file.

    For more information, see Asset Group at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, campaign_id=None, campaign_name=None, asset_group=None):
        super(BulkAssetGroup, self).__init__()

        self._campaign_id = campaign_id
        self._campaign_name = campaign_name
        self._asset_group = asset_group


    @property
    def campaign_id(self):
        """ The identifier of the campaign that contains the asset group.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._campaign_id

    @campaign_id.setter
    def campaign_id(self, campaign_id):
        self._campaign_id = campaign_id

    @property
    def campaign_name(self):
        """ The name of the campaign that contains the asset group.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @property
    def asset_group(self):
        """ The AssetGroup Data Object of the Campaign Management Service.

        A subset of AssetGroup properties are available in the Ad Group record.
        For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._asset_group

    @asset_group.setter
    def asset_group(self, asset_group):
        self._asset_group = asset_group

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.asset_group.Id),
            csv_to_field=lambda c, v: setattr(c.asset_group, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.asset_group.Status),
            csv_to_field=lambda c, v: csv_to_field_enum(c.asset_group, v, 'Status', AssetGroupStatus)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.campaign_id),
            csv_to_field=lambda c, v: setattr(c, 'campaign_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AssetGroup,
            field_to_csv=lambda c: bulk_str(c.asset_group.Name),
            csv_to_field=lambda c, v: setattr(c.asset_group, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.StartDate,
            field_to_csv=lambda c: bulk_date_str(c.asset_group.StartDate),
            csv_to_field=lambda c, v: setattr(c.asset_group, 'StartDate', parse_date(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.EndDate,
            field_to_csv=lambda c: bulk_date_str(c.asset_group.EndDate),
            csv_to_field=lambda c, v: setattr(c.asset_group, 'EndDate', parse_date(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.BusinessName,
            field_to_csv=lambda c: c.asset_group.BusinessName,
            csv_to_field=lambda c, v: setattr(c.asset_group, 'BusinessName', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CallToAction,
            field_to_csv=lambda c: c.asset_group.CallToAction,
            csv_to_field=lambda c, v: csv_to_field_enum(c.asset_group, v, 'CallToAction', CallToAction)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Descriptions,
            field_to_csv=lambda c: field_to_csv_TextAssetLinks(c.asset_group.Descriptions),
            csv_to_field=lambda c, v: csv_to_field_TextAssetLinks(c.asset_group.Descriptions ,v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialStatus,
            field_to_csv=lambda c: c.asset_group.EditorialStatus,
            csv_to_field=lambda c, v: csv_to_field_enum(c.asset_group, v, 'EditorialStatus', AssetGroupEditorialStatus)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.asset_group.FinalMobileUrls, c.asset_group.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.asset_group.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.asset_group.FinalUrls, c.asset_group.Id),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.asset_group.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Headlines,
            field_to_csv=lambda c: field_to_csv_TextAssetLinks(c.asset_group.Headlines),
            csv_to_field=lambda c, v: csv_to_field_TextAssetLinks(c.asset_group.Headlines, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Images,
            field_to_csv=lambda c: field_to_csv_ImageAssetLinks(c.asset_group.Images),
            csv_to_field=lambda c, v: csv_to_field_ImageAssetLinks(c.asset_group.Images, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.LongHeadlines,
            field_to_csv=lambda c: field_to_csv_TextAssetLinks(c.asset_group.LongHeadlines),
            csv_to_field=lambda c, v: csv_to_field_TextAssetLinks(c.asset_group.LongHeadlines ,v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Path1,
            field_to_csv=lambda c: bulk_optional_str(c.asset_group.Path1, c.asset_group.Id),
            csv_to_field=lambda c, v: setattr(c.asset_group, 'Path1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Path2,
            field_to_csv=lambda c: bulk_optional_str(c.asset_group.Path2, c.asset_group.Id),
            csv_to_field=lambda c, v: setattr(c.asset_group, 'Path2', v)
        ),
    ]


    def process_mappings_from_row_values(self, row_values):
        self.asset_group = _CAMPAIGN_OBJECT_FACTORY_V13.create('AssetGroup')

        row_values.convert_to_entity(self, BulkAssetGroup._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._asset_group, 'AssetGroup')
        self.convert_to_values(row_values, BulkAssetGroup._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAssetGroup, self).read_additional_data(stream_reader)
