from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


class BulkAdCustomizerAttribute(_SingleRecordBulkEntity):
    """ Represents an AdCustomizerAttribute.

    Properties of this class and of classes that it is derived from, correspond to fields of the AdCustomizerAttribute record in a bulk file.
    For more information, see AdCustomizerAttribute at https://go.microsoft.com/fwlink/?linkid=846127
    
    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, id = None, name=None, account_value=None, data_type=None, editorial_status = None, status=None):
        super(BulkAdCustomizerAttribute, self).__init__()
        self._id = id
        self._name = name
        self._account_value = account_value
        self._data_type = data_type
        self._editorial_status = editorial_status
        self._status = status


    @property
    def id(self):
        """ the id of bulk record
        Corresponds to the 'Id' field in the bulk file.

        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, value):
        self._id = value        

    @property
    def name(self):
        """ the name of the ad customizer attribute
        Corresponds to the 'Name' field in the bulk file.

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def account_value(self):
        """ the value of the account of ad customizer attribute
        Corresponds to the 'AdCustomizer AttributeValue' field in the bulk file.

        :rtype: str
        """
        return self._account_value

    @account_value.setter
    def account_value(self, value):
        self._account_value = value
          
    @property
    def data_type(self):
        """ the data type of ad customizer attribute
        Corresponds to the 'AdCustomizer DataType' field in the bulk file.

        :rtype: str
        """
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        self._data_type = value
 
    @property
    def editorial_status(self):
        """ the editorial status of ad customizer attribute
        Corresponds to the 'Editorial Status' field in the bulk file.

        :rtype: str
        """
        return self._editorial_status

    @editorial_status.setter
    def editorial_status(self, value):
        self._editorial_status = value

    @property
    def status(self):
        """ the status of ad customizer attribute
        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.id),
            csv_to_field=lambda c, v: setattr(c, 'id', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: bulk_str(c.name),
            csv_to_field=lambda c, v: setattr(c, 'name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdCustomizerAttributeValue,
            field_to_csv=lambda c: bulk_str(c.account_value),
            csv_to_field=lambda c, v: setattr(c, 'account_value', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdCustomizerDataType,
            field_to_csv=lambda c: bulk_str(c.data_type),
            csv_to_field=lambda c, v: setattr(c, 'data_type', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialStatus,
            field_to_csv=lambda c: bulk_str(c.editorial_status),
            csv_to_field=lambda c, v: setattr(c, 'editorial_status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkAdCustomizerAttribute._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkAdCustomizerAttribute._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdCustomizerAttribute, self).read_additional_data(stream_reader)
