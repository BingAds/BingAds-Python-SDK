from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkBrandItem(_SingleRecordBulkEntity):
    """ Represents a brand item.

    This class exposes the property :attr:`brand_item` that can be read and written as fields of the brand item record
    in a bulk file.

    For more information, see brand item at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, id=None, brand_list_id=None, name=None, brand_name=None, brand_url=None, editorial_status=None, editorial_status_date=None, brand_item=None):
        super(BulkBrandItem, self).__init__()

        self._id = id
        self._brand_list_id = brand_list_id
        self._name = name
        self._brand_name = brand_name
        self._brand_url = brand_url
        self._editorial_status = editorial_status
        self._editorial_status_date = editorial_status_date
        self._brand_item = brand_item

    @property
    def brand_item(self):
        """ The BrandItem Data Object of the Campaign Management Service.

        A subset of BrandItem properties are available in the Brand Item record.
        For more information, see Brand Item at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._brand_item

    @brand_item.setter
    def brand_item(self, brand_item):
        self._brand_item = brand_item

    @property
    def id(self):
        """ The identifier of the brand item.

        Corresponds to the 'Id' field in the bulk file.

        :rtype: int
        """

        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def brand_list_id(self):
        """ The identifier of the brand list that contains the brand item.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._brand_list_id

    @brand_list_id.setter
    def brand_list_id(self, brand_list_id):
        self._brand_list_id = brand_list_id

    @property
    def name(self):
        """ The name of the brand item.

        Corresponds to the 'Name' field in the bulk file.

        :rtype: str
        """

        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def brand_name(self):
        """ The name of the brand.

        Corresponds to the 'Brand Name' field in the bulk file.

        :rtype: str
        """

        return self._brand_name

    @brand_name.setter
    def brand_name(self, brand_name):
        self._brand_name = brand_name

    @property
    def brand_url(self):
        """ The url of the brand.

        Corresponds to the 'Brand Url' field in the bulk file.

        :rtype: str
        """

        return self._brand_url

    @brand_url.setter
    def brand_url(self, brand_url):
        self._brand_url = brand_url

    @property
    def editorial_status(self):
        """ The editorial status

        Corresponds to the 'Editorial Status' field in the bulk file.

        :rtype: str
        """

        return self._editorial_status

    @editorial_status.setter
    def editorial_status(self, editorial_status):
        self._editorial_status = editorial_status

    @property
    def editorial_status_date(self):
        """ The editorial status date

        Corresponds to the 'Editorial Status Date' field in the bulk file.

        :rtype: str
        """

        return self._editorial_status_date

    @editorial_status_date.setter
    def editorial_status_date(self, editorial_status_date):
        self._editorial_status_date = editorial_status_date

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
            field_to_csv=lambda c: bulk_str(c.brand_list_id),
            csv_to_field=lambda c, v: setattr(c, 'brand_list_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BrandId,
            field_to_csv=lambda c: bulk_str(c.brand_item.BrandId),
            csv_to_field=lambda c, v: setattr(c.brand_item, 'BrandId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BrandName,
            field_to_csv=lambda c: bulk_str(c.brand_name),
            csv_to_field=lambda c, v: setattr(c, 'brand_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BrandUrl,
            field_to_csv=lambda c: bulk_str(c.brand_url),
            csv_to_field=lambda c, v: setattr(c, 'brand_url', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialStatus,
            field_to_csv=lambda c: bulk_str(c.editorial_status),
            csv_to_field=lambda c, v: setattr(c, 'editorial_status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.StatusDateTime,
            field_to_csv=lambda c: bulk_datetime_str2(c.editorial_status_date),
            csv_to_field=lambda c, v: setattr(c, 'editorial_status_date', parse_datetime2(v))
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.brand_item = _CAMPAIGN_OBJECT_FACTORY_V13.create('BrandItem')

        row_values.convert_to_entity(self, BulkBrandItem._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.brand_item, 'BrandItem')
        self.convert_to_values(row_values, BulkBrandItem._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkBrandItem, self).read_additional_data(stream_reader)
