from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_audience import BulkAudience

class BulkSimilarRemarketingList(BulkAudience):
    """ Represents an Similar Remarketing List that can be read or written in a bulk file.

    This class exposes the :attr:`similar_remarketing_list` property that can be read and written as fields of the
    Similar Remarketing List record in a bulk file.

    For more information, see Similar Remarketing List at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 similar_remarketing_list=None,
                 status=None,):
        super(BulkSimilarRemarketingList, self).__init__(audience = similar_remarketing_list, status = status)

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.SourceId,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.SourceId),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'SourceId', int(v) if v else None)
        ),
    ]

    @property
    def similar_remarketing_list(self):
        """ Defines a Similar Remarketing List """

        return self._audience

    @similar_remarketing_list.setter
    def similar_remarketing_list(self, similar_remarketing_list):
        self._audience = similar_remarketing_list

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.similar_remarketing_list, 'similar_remarketing_list')
        super(BulkSimilarRemarketingList, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkSimilarRemarketingList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.similar_remarketing_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('SimilarRemarketingList')
        super(BulkSimilarRemarketingList, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkSimilarRemarketingList._MAPPINGS)

