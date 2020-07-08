from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_audience import BulkAudience

class BulkCustomAudience(BulkAudience):
    """ Represents a Custom Audience that can be read or written in a bulk file.

    This class exposes the :attr:`custom_audience` property that can be read and written as fields of the
    Custom Audience record in a bulk file.

    For more information, see Custom Audience at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 custom_audience=None,
                 status=None):
        super(BulkCustomAudience, self).__init__(audience = custom_audience, status = status)

    @property
    def custom_audience(self):
        """ Defines a Custom Audience """

        return self._audience

    @custom_audience.setter
    def custom_audience(self, custom_audience):
        self._audience = custom_audience

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.custom_audience, 'custom_audience')
        super(BulkCustomAudience, self).process_mappings_to_row_values(row_values, exclude_readonly)

    def process_mappings_from_row_values(self, row_values):
        self.custom_audience = _CAMPAIGN_OBJECT_FACTORY_V13.create('CustomAudience')
        super(BulkCustomAudience, self).process_mappings_from_row_values(row_values)

