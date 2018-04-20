from bingads.v12.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V12
from bingads.v12.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v12.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v12.internal.bulk.string_table import _StringTable
from bingads.v12.internal.extensions import *

class BulkInMarketAudience(_SingleRecordBulkEntity):
    """ Represents an In Market Audience that can be read or written in a bulk file.

    This class exposes the :attr:`in_market_audience` property that can be read and written as fields of the
    In Market Audience record in a bulk file.

    For more information, see In Market Audience at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 in_market_audience=None,
                 status=None,):
        super(BulkInMarketAudience, self).__init__()

        self._in_market_audience = in_market_audience
        self._status = status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.in_market_audience.Id),
            csv_to_field=lambda c, v: setattr(c.in_market_audience, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.in_market_audience.ParentId),
            csv_to_field=lambda c, v: setattr(c.in_market_audience, 'ParentId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Audience,
            field_to_csv=lambda c: bulk_str(c.in_market_audience.Name),
            csv_to_field=lambda c, v: setattr(c.in_market_audience, 'Name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Description,
            field_to_csv=lambda c: bulk_str(c.in_market_audience.Description),
            csv_to_field=lambda c, v: setattr(c.in_market_audience, 'Description', v)
        ),
        _SimpleBulkMapping(
            _StringTable.MembershipDuration,
            field_to_csv=lambda c: bulk_str(c.in_market_audience.MembershipDuration),
            csv_to_field=lambda c, v: setattr(c.in_market_audience, 'MembershipDuration', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Scope,
            field_to_csv=lambda c: bulk_str(c.in_market_audience.Scope),
            csv_to_field=lambda c, v: setattr(c.in_market_audience, 'Scope', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.AudienceSearchSize,
            field_to_csv=lambda c: bulk_str(c.in_market_audience.SearchSize),
            csv_to_field=lambda c, v: setattr(c.in_market_audience, 'SearchSize', int(v) if v else None)
        ),
    ]

    @property
    def in_market_audience(self):
        """ Defines an In Market Audience """

        return self._in_market_audience

    @in_market_audience.setter
    def in_market_audience(self, in_market_audience):
        self._in_market_audience = in_market_audience

    @property
    def status(self):
        """ The status of the In Market Audience

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.in_market_audience, 'in_market_audience')
        self.convert_to_values(row_values, BulkInMarketAudience._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._in_market_audience = _CAMPAIGN_OBJECT_FACTORY_V12.create('InMarketAudience')
        row_values.convert_to_entity(self, BulkInMarketAudience._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkInMarketAudience, self).read_additional_data(stream_reader)
