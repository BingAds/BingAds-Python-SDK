from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


class BulkAdCustomizerAttributeEntityBase(_SingleRecordBulkEntity):
    """ Represents an AdCustomizerAttributeEntity.
    
    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, id = None, name=None, parent_id=None, attribute_value=None, editorial_status = None):
        super(BulkAdCustomizerAttributeEntityBase, self).__init__()
        self._id = id
        self._name = name
        self._attribute_value = attribute_value
        self._parent_id = parent_id
        self._editorial_status = editorial_status


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
        """ the name of the ad customizer attribute entity
        Corresponds to the 'Name' field in the bulk file.

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
         
    @property
    def attribute_value(self):
        """ the value of ad customizer attribute 
        Corresponds to the 'AdCustomizer AttributeValue' field in the bulk file.

        :rtype: str
        """
        return self._attribute_value

    @attribute_value.setter
    def attribute_value(self, value):
        self._attribute_value = value
        
    @property
    def parent_id(self):
        """ the parent id of bulk record
        Corresponds to the 'ParentId' field in the bulk file.

        :rtype: long
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id = value   
          
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
            field_to_csv=lambda c: bulk_str(c.attribute_value),
            csv_to_field=lambda c, v: setattr(c, 'attribute_value', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.parent_id),
            csv_to_field=lambda c, v: setattr(c, 'parent_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialStatus,
            field_to_csv=lambda c: bulk_str(c.editorial_status),
            csv_to_field=lambda c, v: setattr(c, 'editorial_status', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkAdCustomizerAttributeEntityBase._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkAdCustomizerAttributeEntityBase._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdCustomizerAttributeEntityBase, self).read_additional_data(stream_reader)
