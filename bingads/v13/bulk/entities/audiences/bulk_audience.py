from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *

class BulkAudience(_SingleRecordBulkEntity):
    """ Represents a Audience that can be read or written in a bulk file.

    This class exposes the :attr:`audience` property that can be read and written as fields of the
    Audience record in a bulk file.

    For more information, see Audience at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 audience=None,
                 status=None,):
        super(BulkAudience, self).__init__()

        self._audience = audience
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.audience.Id),
            csv_to_field=lambda c, v: setattr(c.audience, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.audience.ParentId),
            csv_to_field=lambda c, v: setattr(c.audience, 'ParentId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Audience,
            field_to_csv=lambda c: bulk_str(c.audience.Name),
            csv_to_field=lambda c, v: setattr(c.audience, 'Name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Description,
            field_to_csv=lambda c: bulk_str(c.audience.Description),
            csv_to_field=lambda c, v: setattr(c.audience, 'Description', v)
        ),
        _SimpleBulkMapping(
            _StringTable.MembershipDuration,
            field_to_csv=lambda c: bulk_str(c.audience.MembershipDuration),
            csv_to_field=lambda c, v: setattr(c.audience, 'MembershipDuration', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Scope,
            field_to_csv=lambda c: bulk_str(c.audience.Scope),
            csv_to_field=lambda c, v: csv_to_field_enum(c.audience, v, 'Scope', EntityScope)
        ),
        _SimpleBulkMapping(
            _StringTable.AudienceSearchSize,
            field_to_csv=lambda c: bulk_str(c.audience.SearchSize),
            csv_to_field=lambda c, v: setattr(c.audience, 'SearchSize', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AudienceNetworkSize,
            field_to_csv=lambda c: bulk_str(c.audience.AudienceNetworkSize),
            csv_to_field=lambda c, v: setattr(c.audience, 'AudienceNetworkSize', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.SupportedCampaignTypes,
            field_to_csv=lambda c: field_to_csv_SupportedCampaignTypes(c.audience.SupportedCampaignTypes),
            csv_to_field=lambda c, v: csv_to_field_SupportedCampaignTypes(c.audience.SupportedCampaignTypes, v)
        ),
    ]

    @property
    def audience(self):
        """ Defines a Audience """

        return self._audience

    @audience.setter
    def audience(self, audience):
        self._audience = audience

    @property
    def status(self):
        """ The status of the Audience

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkAudience._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkAudience._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAudience, self).read_additional_data(stream_reader)
