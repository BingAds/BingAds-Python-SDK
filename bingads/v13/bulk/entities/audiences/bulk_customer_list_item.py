from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *
from decimal import Decimal


class BulkCustomerListItem(_SingleRecordBulkEntity):
    """ Represents a customer list item that can be read or written in a bulk file.

    Properties of this class and of classes that it is derived from, correspond to fields of the Customer List Item record in a bulk file.
    For more information, see Budget at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, audience=None, parent_id=None, sub_type=None, text = None):
        super(BulkCustomerListItem, self).__init__()
        self._audience = audience
        self._parent_id = parent_id
        self._sub_type = sub_type
        self._text = text

    @property
    def audience(self):
        """
        the audience, see more detail at: https://go.microsoft.com/fwlink/?linkid=846127
        
        :rtype: str
        """
        return self._audience

    @audience.setter
    def audience(self, value):
        self._audience = value

    @property
    def parent_id(self):
        """ the parent id of bulk record
        Corresponds to the 'parent id' field in the bulk file.

        :rtype: long
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id = value

    @property
    def sub_type(self):
        """ the sub type of bulk record
        Corresponds to the 'Sub Type' field in the bulk file.

        :rtype: str
        """
        return self._sub_type

    @sub_type.setter
    def sub_type(self, value):
        self._sub_type = value
        
    @property
    def text(self):
        """ the text of bulk record
        Corresponds to the 'Text' field in the bulk file.

        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, value):
        self._text = value


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.parent_id),
            csv_to_field=lambda c, v: setattr(c, 'parent_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Audience,
            field_to_csv=lambda c: bulk_str(c.audience),
            csv_to_field=lambda c, v: setattr(c, 'audience', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SubType,
            field_to_csv=lambda c: c.sub_type,
            csv_to_field=lambda c, v: setattr(c, 'sub_type', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Text,
            field_to_csv=lambda c: bulk_str(c.text),
            csv_to_field=lambda c, v: setattr(c, 'text', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkCustomerListItem._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkCustomerListItem._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCustomerListItem, self).read_additional_data(stream_reader)
