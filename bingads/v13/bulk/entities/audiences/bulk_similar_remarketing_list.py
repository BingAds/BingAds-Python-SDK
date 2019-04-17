from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *

class BulkSimilarRemarketingList(_SingleRecordBulkEntity):
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
        super(BulkSimilarRemarketingList, self).__init__()

        self._similar_remarketing_list = similar_remarketing_list
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.Id),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.ParentId),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'ParentId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Audience,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.Name),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'Name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Description,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.Description),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'Description', v)
        ),
        _SimpleBulkMapping(
            _StringTable.MembershipDuration,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.MembershipDuration),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'MembershipDuration', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Scope,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.Scope),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'Scope', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.SourceId,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.SourceId),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'SourceId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.AudienceSearchSize,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.SearchSize),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'SearchSize', int(v) if v else None)
        ),       
        _SimpleBulkMapping(
            header=_StringTable.AudienceNetworkSize,
            field_to_csv=lambda c: bulk_str(c.similar_remarketing_list.AudienceNetworkSize),
            csv_to_field=lambda c, v: setattr(c.similar_remarketing_list, 'AudienceNetworkSize', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.SupportedCampaignTypes,
            field_to_csv=lambda c: field_to_csv_SupportedCampaignTypes(c.similar_remarketing_list.SupportedCampaignTypes),
            csv_to_field=lambda c, v: csv_to_field_SupportedCampaignTypes(c.similar_remarketing_list.SupportedCampaignTypes, v)
        ),
    ]

    @property
    def similar_remarketing_list(self):
        """ Defines a Similar Remarketing List """

        return self._similar_remarketing_list

    @similar_remarketing_list.setter
    def similar_remarketing_list(self, similar_remarketing_list):
        self._similar_remarketing_list = similar_remarketing_list

    @property
    def status(self):
        """ The status of the Similar Remarketing List

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.similar_remarketing_list, 'similar_remarketing_list')
        self.convert_to_values(row_values, BulkSimilarRemarketingList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._similar_remarketing_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('SimilarRemarketingList')
        row_values.convert_to_entity(self, BulkSimilarRemarketingList._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkSimilarRemarketingList, self).read_additional_data(stream_reader)
