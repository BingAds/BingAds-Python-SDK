from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *

class BulkTopic(_SingleRecordBulkEntity):
    """ Represents a topic.

    This class exposes the property :attr:`brand_item` that can be read and written as fields of the topic record
    in a bulk file.

    For more information, see topic at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, id=None, parent_id=None, topic_parent_id=None, name=None, status=None):
        super(BulkTopic, self).__init__()

        self._id = id
        self._parent_id = parent_id
        self._topic_parent_id = topic_parent_id
        self._name = name
        self._status = status

    @property
    def id(self):
        """ The identifier of the topic.

        Corresponds to the 'Id' field in the bulk file.

        :rtype: int
        """

        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def parent_id(self):
        """ The parent identifier of the topic that contains the topic.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        self._parent_id = parent_id

    @property
    def topic_parent_id(self):
        """ The parent identifier of the topic that contains the topic.

        Corresponds to the 'Topic Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._topic_parent_id

    @topic_parent_id.setter
    def topic_parent_id(self, topic_parent_id):
        self._topic_parent_id = topic_parent_id

    @property
    def name(self):
        """ The name of the topic.

        Corresponds to the 'Name' field in the bulk file.

        :rtype: str
        """

        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def status(self):
        """ The status

        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.id),
            csv_to_field=lambda c, v: setattr(c, 'id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: bulk_str(c.name),
            csv_to_field=lambda c, v: setattr(c, 'name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.parent_id),
            csv_to_field=lambda c, v: setattr(c, 'parent_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TopicParentId,
            field_to_csv=lambda c: bulk_str(c.topic_parent_id),
            csv_to_field=lambda c, v: setattr(c, 'topic_parent_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: bulk_str(c.name),
            csv_to_field=lambda c, v: setattr(c, 'name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):

        row_values.convert_to_entity(self, BulkTopic._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkTopic._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkTopic, self).read_additional_data(stream_reader)
