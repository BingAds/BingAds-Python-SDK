from bingads.v11.internal.bulk.string_table import _StringTable
from bingads.v11.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v11.internal.bulk.mappings import _SimpleBulkMapping
from bingads.internal.extensions import *


class BulkAccount(_SingleRecordBulkEntity):
    """ Represents an account that can be read or written in a bulk file.

    Properties of this class and of classes that it is derived from, correspond to fields of the Account record in a bulk file.
    For more information, see Account at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, customer_id=None, sync_time=None):
        super(BulkAccount, self).__init__()
        self._id = account_id
        self._customer_id = customer_id
        self._sync_time = sync_time

    @property
    def id(self):
        """ The identifier of the account.

        Corresponds to the 'Id' field in the bulk file.

        :return: The identifier of the account.
        :rtype: int
        """

        return self._id

    @property
    def customer_id(self):
        """ The identifier of the customer that contains the account.

        Corresponds to the 'Parent Id' field in the bulk file.

        :return: The identifier of the customer that contains the account.
        :rtype: int
        """

        return self._customer_id

    @property
    def sync_time(self):
        """ The date and time that you last synced your account using the bulk service.

        You should keep track of this value in UTC time.
        Corresponds to the 'Sync Time' field in the bulk file.

        :return: The date and time that you last synced your account using the bulk service.
        :rtype: datetime.datetime
        """

        return self._sync_time

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.id),
            csv_to_field=lambda c, v: setattr(c, '_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.customer_id),
            csv_to_field=lambda c, v: setattr(c, '_customer_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SyncTime,
            field_to_csv=lambda c: bulk_datetime_str(c.sync_time),
            csv_to_field=lambda c, v: setattr(c, '_sync_time', parse_datetime(v) if v else None)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkAccount._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkAccount._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAccount, self).read_additional_data(stream_reader)
