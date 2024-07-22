from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkBrandList(_SingleRecordBulkEntity):
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

    def __init__(self, account_id=None, brand_list=None):
        super(BulkBrandList, self).__init__()

        self._account_id = account_id
        self._brand_list = brand_list

    @property
    def brand_list(self):
        """ The BrandList Data Object of the Campaign Management Service.

        A subset of BrandList properties are available in the Brand List record.
        For more information, see Brand Item at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._brand_list

    @brand_list.setter
    def brand_list(self, brand_list):
        self._brand_list = brand_list

    @property
    def account_id(self):
        """ The identifier of the account that contains the brand list.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.brand_list.Id),
            csv_to_field=lambda c, v: setattr(c.brand_list, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: bulk_str(c.brand_list.Name),
            csv_to_field=lambda c, v: setattr(c.brand_list, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, 'account_id', int(v) if v else None)
        ),

    ]

    def process_mappings_from_row_values(self, row_values):
        self.brand_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('BrandList')

        row_values.convert_to_entity(self, BulkBrandList._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.brand_list, 'BrandList')
        self.convert_to_values(row_values, BulkBrandList._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkBrandList, self).read_additional_data(stream_reader)
