from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_audience import BulkAudience

class BulkProductAudience(BulkAudience):
    """ Represents a Product Audience that can be read or written in a bulk file.

    This class exposes the :attr:`product_audience` property that can be read and written as fields of the
    Product Audience record in a bulk file.

    For more information, see Product Audience at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 product_audience=None,
                 status=None,):
        super(BulkProductAudience, self).__init__(audience = BulkAudience, status = status)

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.TagId,
            field_to_csv=lambda c: bulk_str(c.product_audience.TagId),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'TagId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ProductAudienceType,
            field_to_csv=lambda c: bulk_str(c.product_audience.ProductAudienceType),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'ProductAudienceType', v)
        ),
    ]

    @property
    def product_audience(self):
        """ Defines a Product Audience """

        return self._audience

    @product_audience.setter
    def product_audience(self, product_audience):
        self._audience = product_audience


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.product_audience, 'product_audience')
        super(BulkProductAudience, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkProductAudience._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.product_audience = _CAMPAIGN_OBJECT_FACTORY_V13.create('ProductAudience')
        super(BulkProductAudience, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkProductAudience._MAPPINGS)

