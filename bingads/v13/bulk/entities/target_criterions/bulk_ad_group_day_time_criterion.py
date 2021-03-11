from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_biddable_criterion import BulkAdGroupBiddableCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *

class BulkAdGroupDayTimeCriterion(BulkAdGroupBiddableCriterion):
    """ Represents an Ad Group Day Time Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Day Time Criterion record in a bulk file.

    For more information, see Ad Group Day Time Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupDayTimeCriterion, self).__init__(biddable_ad_group_criterion, campaign_name, ad_group_name)

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Target,
            field_to_csv=lambda c: field_to_csv_DayTimeTarget(c.biddable_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_DayTimeTarget(c.biddable_ad_group_criterion, v)
        ),
        _SimpleBulkMapping(
            _StringTable.FromHour,
            field_to_csv=lambda c: field_to_csv_FromHour(c.biddable_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_FromHour(c.biddable_ad_group_criterion, int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.FromMinute,
            field_to_csv=lambda c: field_to_csv_FromMinute(c.biddable_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_FromMinute(c.biddable_ad_group_criterion, v)
        ),
        _SimpleBulkMapping(
            _StringTable.ToHour,
            field_to_csv=lambda c: field_to_csv_ToHour(c.biddable_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_ToHour(c.biddable_ad_group_criterion, int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ToMinute,
            field_to_csv=lambda c: field_to_csv_ToMinute(c.biddable_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_ToMinute(c.biddable_ad_group_criterion, v)
        ),
    ]
    
    def create_criterion(self):
        self._biddable_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('DayTimeCriterion')
        self._biddable_ad_group_criterion.Criterion.Type = 'DayTimeCriterion'

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkAdGroupDayTimeCriterion, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAdGroupDayTimeCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkAdGroupDayTimeCriterion, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAdGroupDayTimeCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupDayTimeCriterion, self).read_additional_data(stream_reader)
