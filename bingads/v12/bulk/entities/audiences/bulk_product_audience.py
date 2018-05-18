from bingads.v12.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V12
from bingads.v12.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v12.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v12.internal.bulk.string_table import _StringTable
from bingads.v12.internal.extensions import *

class BulkProductAudience(_SingleRecordBulkEntity):
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
        super(BulkProductAudience, self).__init__()

        self._product_audience = product_audience
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.product_audience.Id),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.product_audience.ParentId),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'ParentId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Audience,
            field_to_csv=lambda c: bulk_str(c.product_audience.Name),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'Name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Description,
            field_to_csv=lambda c: bulk_str(c.product_audience.Description),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'Description', v)
        ),
        _SimpleBulkMapping(
            _StringTable.MembershipDuration,
            field_to_csv=lambda c: bulk_str(c.product_audience.MembershipDuration),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'MembershipDuration', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Scope,
            field_to_csv=lambda c: bulk_str(c.product_audience.Scope),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'Scope', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.AudienceSearchSize,
            field_to_csv=lambda c: bulk_str(c.product_audience.SearchSize),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'SearchSize', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AudienceNetworkSize,
            field_to_csv=lambda c: bulk_str(c.product_audience.AudienceNetworkSize),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'AudienceNetworkSize', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.SupportedCampaignTypes,
            field_to_csv=lambda c: field_to_csv_SupportedCampaignTypes(c.product_audience.SupportedCampaignTypes),
            csv_to_field=lambda c, v: csv_to_field_SupportedCampaignTypes(c.product_audience.SupportedCampaignTypes, v)
        ),
        _SimpleBulkMapping(
            _StringTable.TagId,
            field_to_csv=lambda c: bulk_str(c.product_audience.TagId),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'TagId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Audience,
            field_to_csv=lambda c: bulk_str(c.product_audience.ProductAudienceType),
            csv_to_field=lambda c, v: setattr(c.product_audience, 'ProductAudienceType', v)
        ),
    ]

    @property
    def product_audience(self):
        """ Defines a Product Audience """

        return self._product_audience

    @product_audience.setter
    def product_audience(self, product_audience):
        self._product_audience = product_audience

    @property
    def status(self):
        """ The status of the Product Audience

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.product_audience, 'product_audience')
        self.convert_to_values(row_values, BulkProductAudience._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._product_audience = _CAMPAIGN_OBJECT_FACTORY_V12.create('ProductAudience')
        row_values.convert_to_entity(self, BulkProductAudience._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkProductAudience, self).read_additional_data(stream_reader)
