from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *

LinkedInSegmentStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('LinkedInSegmentStatus')


class BulkCompanyList(_SingleRecordBulkEntity):
    """Represents a company list that can be read or written in a bulk file."""

    def __init__(self, account_id=None, audience_size=None, company_list=None, status=None):
        super(BulkCompanyList, self).__init__()
        self._account_id = account_id
        self._audience_size = audience_size
        self._company_list = company_list
        self._status = status

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def audience_size(self):
        return self._audience_size

    @audience_size.setter
    def audience_size(self, value):
        self._audience_size = value

    @property
    def company_list(self):
        return self._company_list

    @company_list.setter
    def company_list(self, value):
        self._company_list = value

    @property
    def status(self):
        """Bulk upload status ('Active' or 'Deleted'), written to the Status column.

        Downloaded processing status remains on company_list.Status.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def _read_status(self, value):
        if value in (_StringTable.EntityActiveStatus, _StringTable.EntityDeletedStatus):
            self.status = value
            self.company_list.Status = None
        else:
            self.company_list.Status = getattr(LinkedInSegmentStatus, value) if value else None

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: c._read_status(v)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.company_list.Id),
            csv_to_field=lambda c, v: setattr(c.company_list, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, 'account_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Name,
            field_to_csv=lambda c: bulk_str(c.company_list.Name),
            csv_to_field=lambda c, v: setattr(c.company_list, 'Name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.AudienceSize,
            field_to_csv=lambda c: bulk_str(c.audience_size),
            csv_to_field=lambda c, v: setattr(c, 'audience_size', int(v) if v else None)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.company_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('CompanyList')
        self.status = None
        row_values.convert_to_entity(self, BulkCompanyList._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.company_list, 'CompanyList')
        self.convert_to_values(row_values, BulkCompanyList._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCompanyList, self).read_additional_data(stream_reader)
