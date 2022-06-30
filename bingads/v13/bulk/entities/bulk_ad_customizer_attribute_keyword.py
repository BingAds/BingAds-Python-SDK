from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

from. import BulkAdCustomizerAttributeEntityBase

class BulkKeywordAdCustomizerAttribute(BulkAdCustomizerAttributeEntityBase):
    """ Represents a KeywordAdCustomizerAttribute.
    
    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, id = None, name=None, parent_id=None, attribute_value=None, editorial_status = None):
        super(BulkKeywordAdCustomizerAttribute, self).__init__(id, name, parent_id, attribute_value, editorial_status)


    @property
    def keyword_id(self):
        """ the keyword id of bulk record
        Corresponds to the 'ParentId' field in the bulk file.

        :rtype: str
        """
        return self._parent_id

    @keyword_id.setter
    def keyword_id(self, value):
        self._parent_id = value        

