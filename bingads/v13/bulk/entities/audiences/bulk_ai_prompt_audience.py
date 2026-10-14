from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import bulk_str


class BulkAIPromptAudience(_SingleRecordBulkEntity):
    """An AI Prompt Audience row that can be read or deleted through Bulk.

    Bulk upload supports deletion only; creating or updating AI Prompt Audiences
    is not supported.
    """

    def __init__(self):
        super(BulkAIPromptAudience, self).__init__()
        self._id = None
        self._account_id = None
        self._audience = None
        self._scope = None
        self._status = None

    @property
    def id(self):
        """The identifier in the bulk file's Id field."""
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def account_id(self):
        """The account identifier in the bulk file's Parent Id field."""
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def audience(self):
        """The audience name in the bulk file's Audience field."""
        return self._audience

    @audience.setter
    def audience(self, value):
        self._audience = value

    @property
    def scope(self):
        """The audience scope in the bulk file's Scope field."""
        return self._scope

    @scope.setter
    def scope(self, value):
        self._scope = value

    @property
    def status(self):
        """The status; set Deleted to remove an audience through Bulk."""
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda entity: entity.status,
            csv_to_field=lambda entity, value: setattr(entity, "status", value)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda entity: bulk_str(entity.id),
            csv_to_field=lambda entity, value: setattr(entity, "id", int(value) if value else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda entity: bulk_str(entity.account_id),
            csv_to_field=lambda entity, value: setattr(entity, "account_id", int(value) if value else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Audience,
            field_to_csv=lambda entity: entity.audience,
            csv_to_field=lambda entity, value: setattr(entity, "audience", value)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Scope,
            field_to_csv=lambda entity: entity.scope,
            csv_to_field=lambda entity, value: setattr(entity, "scope", value)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkAIPromptAudience._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkAIPromptAudience._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAIPromptAudience, self).read_additional_data(stream_reader)
