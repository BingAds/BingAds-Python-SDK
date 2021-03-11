from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_negative_criterion import BulkAdGroupNegativeCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *

class BulkAdGroupNegativeLocationCriterion(BulkAdGroupNegativeCriterion):
    """ Represents an Ad Group Negative Location Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Negative Location Criterion record in a bulk file.

    For more information, see Ad Group Negative Location Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 negative_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupNegativeLocationCriterion, self).__init__(negative_ad_group_criterion, campaign_name, ad_group_name)

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Target,
            field_to_csv=lambda c: field_to_csv_LocationTarget(c.negative_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_LocationTarget(c.negative_ad_group_criterion, int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.SubType,
            field_to_csv=lambda c: field_to_csv_LocationType(c.negative_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_LocationType(c.negative_ad_group_criterion, v)
        ),
        _SimpleBulkMapping(
            _StringTable.Name,
            field_to_csv=lambda c: field_to_csv_LocationName(c.negative_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_LocationName(c.negative_ad_group_criterion, v)
        ),
    ]
    
    def create_criterion(self):
        self._negative_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('LocationCriterion')
        self._negative_ad_group_criterion.Criterion.Type = 'LocationCriterion'

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkAdGroupNegativeLocationCriterion, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAdGroupNegativeLocationCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkAdGroupNegativeLocationCriterion, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAdGroupNegativeLocationCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupNegativeLocationCriterion, self).read_additional_data(stream_reader)
