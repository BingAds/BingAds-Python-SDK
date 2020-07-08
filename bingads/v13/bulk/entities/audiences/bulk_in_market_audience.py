from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_audience import BulkAudience

class BulkInMarketAudience(BulkAudience):
    """ Represents an In Market Audience that can be read or written in a bulk file.

    This class exposes the :attr:`in_market_audience` property that can be read and written as fields of the
    In Market Audience record in a bulk file.

    For more information, see In Market Audience at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 in_market_audience=None,
                 status=None,):
        super(BulkInMarketAudience, self).__init__(audience = in_market_audience, status = status)

    @property
    def in_market_audience(self):
        """ Defines an In Market Audience """

        return self._audience

    @in_market_audience.setter
    def in_market_audience(self, in_market_audience):
        self._audience = in_market_audience

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.in_market_audience, 'in_market_audience')
        super(BulkInMarketAudience, self).process_mappings_to_row_values(row_values, exclude_readonly_data)

    def process_mappings_from_row_values(self, row_values):
        self.in_market_audience = _CAMPAIGN_OBJECT_FACTORY_V13.create('InMarketAudience')
        super(BulkInMarketAudience, self).process_mappings_from_row_values(row_values)
