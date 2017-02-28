from bingads.v10.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V10
from bingads.v10.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v10.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v10.internal.bulk.string_table import _StringTable
from bingads.internal.extensions import *

class BulkRemarketingList(_SingleRecordBulkEntity):
    """ Represents an Remarketing List that can be read or written in a bulk file.

    This class exposes the :attr:`remarketing_list` property that can be read and written as fields of the
    Remarketing List record in a bulk file.

    For more information, see Remarketing List at http://go.microsoft.com/fwlink/?LinkId=799352.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 remarketing_list=None,
                 status=None,):
        super(BulkRemarketingList, self).__init__()

        self._remarketing_list = remarketing_list
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.remarketing_list.Id),
            csv_to_field=lambda c, v: setattr(c.remarketing_list, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.remarketing_list.ParentId),
            csv_to_field=lambda c, v: setattr(c.remarketing_list, 'ParentId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.RemarketingList,
            field_to_csv=lambda c: bulk_str(c.remarketing_list.Name),
            csv_to_field=lambda c, v: setattr(c.remarketing_list, 'Name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Description,
            field_to_csv=lambda c: bulk_str(c.remarketing_list.Description),
            csv_to_field=lambda c, v: setattr(c.remarketing_list, 'Description', v)
        ),
        _SimpleBulkMapping(
            _StringTable.MembershipDuration,
            field_to_csv=lambda c: bulk_str(c.remarketing_list.MembershipDuration),
            csv_to_field=lambda c, v: setattr(c.remarketing_list, 'MembershipDuration', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Scope,
            field_to_csv=lambda c: bulk_str(c.remarketing_list.Scope),
            csv_to_field=lambda c, v: setattr(c.remarketing_list, 'Scope', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.TagId,
            field_to_csv=lambda c: bulk_str(c.remarketing_list.TagId),
            csv_to_field=lambda c, v: setattr(c.remarketing_list, 'TagId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.RemarketingRule,
            field_to_csv=lambda c: field_to_csv_RemarketingRule(c.remarketing_list),
            csv_to_field=lambda c, v: csv_to_field_RemarketingRule(c.remarketing_list, v)
        ),
    ]

    @property
    def remarketing_list(self):
        """ Defines a Remarketing List """

        return self._remarketing_list

    @remarketing_list.setter
    def remarketing_list(self, remarketing_list):
        self._remarketing_list = remarketing_list

    @property
    def status(self):
        """ The status of the Remarketing List

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.remarketing_list, 'remarketing_list')
        self.convert_to_values(row_values, BulkRemarketingList._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._remarketing_list = _CAMPAIGN_OBJECT_FACTORY_V10.create('RemarketingList')
        row_values.convert_to_entity(self, BulkRemarketingList._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkRemarketingList, self).read_additional_data(stream_reader)
