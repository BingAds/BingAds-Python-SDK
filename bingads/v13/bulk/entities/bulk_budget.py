from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *
from decimal import Decimal


class BulkBudget(_SingleRecordBulkEntity):
    """ Represents a budget that can be read or written in a bulk file.

    Properties of this class and of classes that it is derived from, correspond to fields of the Budget record in a bulk file.
    For more information, see Budget at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, budget=None, status=None, account_id=None):
        super(BulkBudget, self).__init__()
        self._budget = budget
        self._status = status
        self._account_id = account_id

    @property
    def budget(self):
        """
        the Budget object, see more detail at: https://go.microsoft.com/fwlink/?linkid=846127
        """
        return self._budget

    @budget.setter
    def budget(self, value):
        self._budget = value

    @property
    def status(self):
        """ the status of bulk record
        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def account_id(self):
        """ the id of the account which contains the budget
        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: long
        """
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.budget.Id),
            csv_to_field=lambda c, v: setattr(c.budget, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, 'account_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BudgetName,
            field_to_csv=lambda c: bulk_str(c.budget.Name),
            csv_to_field=lambda c, v: setattr(c.budget, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BudgetType,
            field_to_csv=lambda c: bulk_str(c.budget.BudgetType),
            csv_to_field=lambda c, v: csv_to_field_BudgetType(c.budget, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Budget,
            field_to_csv=lambda c: bulk_str(c.budget.Amount),
            csv_to_field=lambda c, v: setattr(c.budget, 'Amount', Decimal(v) if v else None)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self._budget = _CAMPAIGN_OBJECT_FACTORY_V13.create('Budget')
        row_values.convert_to_entity(self, BulkBudget._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.budget, 'budget')
        self.convert_to_values(row_values, BulkBudget._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkBudget, self).read_additional_data(stream_reader)
