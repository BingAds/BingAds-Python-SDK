from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

from. import BulkAdCustomizerAttributeEntityBase


class BulkCampaignAdCustomizerAttribute(BulkAdCustomizerAttributeEntityBase):
    """ Represents a CampaignAdCustomizerAttribute.
    
    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, id = None, name=None, parent_id=None, attribute_value=None, editorial_status = None):
        super(BulkCampaignAdCustomizerAttribute, self).__init__(id, name, parent_id, attribute_value, editorial_status)


    @property
    def campaign_id(self):
        """ the campaign id of bulk record
        Corresponds to the 'ParentId' field in the bulk file.

        :rtype: str
        """
        return self._parent_id

    @campaign_id.setter
    def campaign_id(self, value):
        self._parent_id = value        

