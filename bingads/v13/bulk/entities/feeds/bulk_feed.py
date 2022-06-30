from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


class BulkFeed(_SingleRecordBulkEntity):
    """ Represents a feed.

    Properties of this class and of classes that it is derived from, correspond to fields of the Feed record in a bulk file.
    For more information, see Feed at https://go.microsoft.com/fwlink/?linkid=846127
    
    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, id = None, status=None, account_id=None, sub_type=None, feed_name = None, custom_attr=None, schedule=None):
        super(BulkFeed, self).__init__()
        self._status = status
        self._account_id = account_id
        self._id = id
        self._sub_type = sub_type
        self._name = feed_name
        self._custom_attributes = custom_attr
        self._schedule = schedule


    @property
    def id(self):
        """ the status of bulk record
        Corresponds to the 'Id' field in the bulk file.

        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, value):
        self._id = value        

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
        """ the id of the account which contains the feed
        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: long
        """
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value
          
    @property
    def name(self):
        """ the id of the account which contains the feed
        Corresponds to the 'Feed Name' field in the bulk file.

        :rtype: long
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def sub_type(self):
        """ the id of the account which contains the feed
        Corresponds to the 'Sub Type' field in the bulk file.

        :rtype: long
        """
        return self._sub_type

    @sub_type.setter
    def sub_type(self, value):
        self._sub_type = value
 
    @property
    def custom_attributes(self):
        """ the id of the account which contains the feed
        Corresponds to the 'Custom Attributes' field in the bulk file.

        :rtype: long
        """
        return self._custom_attributes
    
    @custom_attributes.setter
    def custom_attributes(self, value):
        self._custom_attributes = value

    @property
    def schedule(self):
        """ the schedule of the feed
        Corresponds to the 'Schedule' field in the bulk file.

        :rtype: string
        """
        return self._schedule

    @schedule.setter
    def schedule(self, value):
        self._schedule = value
 
    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.id),
            csv_to_field=lambda c, v: setattr(c, 'id', int(v) if v else None)
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
            header=_StringTable.FeedName,
            field_to_csv=lambda c: bulk_str(c.name),
            csv_to_field=lambda c, v: setattr(c, 'name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SubType,
            field_to_csv=lambda c: bulk_str(c.sub_type),
            csv_to_field=lambda c, v: setattr(c, 'sub_type', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomAttributes,
            field_to_csv=lambda c: field_to_csv_CustomAttributes(c.custom_attributes),
            csv_to_field=lambda c, v: csv_to_field_CustomAttributes(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Schedule,
            field_to_csv=lambda c: c.schedule,
            csv_to_field=lambda c, v: setattr(c, 'schedule', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkFeed._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkFeed._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkFeed, self).read_additional_data(stream_reader)
