from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.extensions import *

class BulkAudienceGroup(_SingleRecordBulkEntity):
    """ Represents an audience group.

    This class exposes the property :attr:`audience_group` that can be read and written as fields of the Audience Group record
    in a bulk file.

    For more information, see Audience Group at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, status=None, audience_group=None, audience_ids=None):
        super(BulkAudienceGroup, self).__init__()

        self._account_id = account_id
        self._audience_group = audience_group
        self._status = status
        self._audience_ids = audience_ids
        self._age_ranges = None
        self._gender_types = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def audience_ids(self):
        return self._audience_ids

    @audience_ids.setter
    def audience_ids(self, audience_ids):
        self._audience_ids = audience_ids

    @property
    def age_ranges(self):
        return self._age_ranges

    @age_ranges.setter
    def age_ranges(self, age_ranges):
        self._age_ranges = age_ranges

    @property
    def gender_types(self):
        return self._gender_types

    @gender_types.setter
    def gender_types(self, gender_types):
        self._gender_types = gender_types

    @property
    def account_id(self):
        """ The identifier of the account that contains the audience group.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    @property
    def audience_group(self):
        """ The AudienceGroup Data Object of the Campaign Management Service.

        A subset of AudienceGroup properties are available in the Audience Group record.
        For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._audience_group

    @audience_group.setter
    def audience_group(self, audience_group):
        self._audience_group = audience_group

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.audience_group.Id),
            csv_to_field=lambda c, v: setattr(c.audience_group, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, 'account_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AudienceGroupName,
            field_to_csv=lambda c: c.audience_group.Name,
            csv_to_field=lambda c, v: setattr(c.audience_group, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Audiences,
            field_to_csv=lambda c: field_to_csv_AudienceIds(c),
            csv_to_field=lambda c, v: csv_to_field_AudienceIds(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AgeRanges,
            field_to_csv=lambda c: field_to_csv_AgeRanges(c),
            csv_to_field=lambda c, v: csv_to_field_AgeRanges(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.GenderTypes,
            field_to_csv=lambda c: field_to_csv_GenderTypes(c),
            csv_to_field=lambda c, v: csv_to_field_GenderTypes(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Description,
            field_to_csv=lambda c: bulk_str(c.audience_group.Description),
            csv_to_field=lambda c, v: setattr(c.audience_group, 'Description', v)
        ),
    ]


    def process_mappings_from_row_values(self, row_values):
        self.audience_group = _CAMPAIGN_OBJECT_FACTORY_V13.create('AudienceGroup')

        row_values.convert_to_entity(self, BulkAudienceGroup._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._audience_group, 'AudienceGroup')
        self.convert_to_values(row_values, BulkAudienceGroup._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAudienceGroup, self).read_additional_data(stream_reader)
