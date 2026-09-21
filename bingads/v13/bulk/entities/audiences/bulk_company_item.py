from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *

CompanyNameStatus = _CAMPAIGN_OBJECT_FACTORY_V13.create('CompanyNameStatus')


class BulkCompanyItem(_SingleRecordBulkEntity):
    """Represents a company item that can be read or written in a bulk file."""

    def __init__(self, company_list_id=None, company_item=None):
        super(BulkCompanyItem, self).__init__()
        self._company_list_id = company_list_id
        self._company_item = company_item

    @property
    def company_list_id(self):
        return self._company_list_id

    @company_list_id.setter
    def company_list_id(self, value):
        self._company_list_id = value

    @property
    def company_item(self):
        return self._company_item

    @company_item.setter
    def company_item(self, value):
        self._company_item = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.company_item.Status),
            csv_to_field=lambda c, v: csv_to_field_enum(c.company_item, v, 'Status', CompanyNameStatus)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.company_item.Id),
            csv_to_field=lambda c, v: setattr(c.company_item, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.company_list_id),
            csv_to_field=lambda c, v: setattr(c, 'company_list_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.CompanyName,
            field_to_csv=lambda c: bulk_str(c.company_item.Name),
            csv_to_field=lambda c, v: setattr(c.company_item, 'Name', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.company_item = _CAMPAIGN_OBJECT_FACTORY_V13.create('CompanyName')
        row_values.convert_to_entity(self, BulkCompanyItem._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.company_item, 'CompanyItem')
        self.convert_to_values(row_values, BulkCompanyItem._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCompanyItem, self).read_additional_data(stream_reader)
