from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkCampaignBrandListAssociation(_SingleRecordBulkEntity):
    """ Represents a campaign brand list association.

    This class exposes the property :attr:`campaign_brand_list_association` that can be read and written as fields of the campaign brand list association record
    in a bulk file.

    For more information, see campaign brand list association at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, id=None, campaign_id=None, name=None, is_excluded=None):
        super(BulkCampaignBrandListAssociation, self).__init__()

        self._id = id
        self._campaign_id = campaign_id
        self._name = name
        self._is_excluded = is_excluded

    @property
    def id(self):
        """ The identifier of the campaign brand list association.

        Corresponds to the 'Id' field in the bulk file.

        :rtype: int
        """

        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def campaign_id(self):
        """ The identifier of the campaign that contains the brand list association.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._campaign_id

    @campaign_id.setter
    def campaign_id(self, campaign_id):
        self._campaign_id = campaign_id

    @property
    def name(self):
        """ The name of the brand list association.

        Corresponds to the 'Name' field in the bulk file.

        :rtype: str
        """

        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def is_excluded(self):
        """ Corresponds to the 'Is Excluded' field in the bulk file.

        :rtype: bool
        """

        return self._is_excluded

    @is_excluded.setter
    def is_excluded(self, is_excluded):
        self._is_excluded = is_excluded

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.id),
            csv_to_field=lambda c, v: setattr(c, 'id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: bulk_str(c.name),
            csv_to_field=lambda c, v: setattr(c, 'name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.campaign_id),
            csv_to_field=lambda c, v: setattr(c, 'campaign_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.IsExcluded,
            field_to_csv=lambda c: bulk_str(c.is_excluded),
            csv_to_field=lambda c, v: setattr(c, 'is_excluded', parse_bool(v))
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkCampaignBrandListAssociation._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkCampaignBrandListAssociation._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignBrandListAssociation, self).read_additional_data(stream_reader)
