from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *
from decimal import Decimal


class BulkImage(_SingleRecordBulkEntity):
    """ Represents a image that can be read or written in a bulk file.

    Properties of this class and of classes that it is derived from, correspond to fields of the Image record in a bulk file.
    For more information, see Image at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status = None):
        super(BulkImage, self).__init__()
        self._id = None
        self._status = status
        self._account_id = None
        self._text = None
        self._subtype = None
        self._url = None
        self._width = None
        self._height = None
        

    @property
    def id(self):
        """
        the Id object, see more detail at: https://go.microsoft.com/fwlink/?linkid=846127
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
        """ the id of the account which contains the image
        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: long
        """
        return self._account_id
    
    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
       
    @property
    def subtype(self):
        return self._subtype 
    
    @subtype.setter
    def subtype(self, value):
        self._subtype = value

    @property
    def url(self):
        return self._url
     
    @url.setter
    def url(self, value):
        self._url = value

    @property
    def width(self):
        return self._width 

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height    
  
    @height.setter
    def height(self, value):
        self._height = value

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
            header=_StringTable.SubType,
            field_to_csv=lambda c: bulk_str(c.subtype),
            csv_to_field=lambda c, v: setattr(c, 'subtype', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Url,
            field_to_csv=lambda c: bulk_str(c.url),
            csv_to_field=lambda c, v: setattr(c, 'url', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Text,
            field_to_csv=lambda c: bulk_str(c.text),
            csv_to_field=lambda c, v: setattr(c, 'text', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Width,
            field_to_csv=lambda c: bulk_str(c.width),
            csv_to_field=lambda c, v: setattr(c, 'width', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Height,
            field_to_csv=lambda c: bulk_str(c.height),
            csv_to_field=lambda c, v: setattr(c, 'height', int(v) if v else None)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkImage._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkImage._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkImage, self).read_additional_data(stream_reader)
