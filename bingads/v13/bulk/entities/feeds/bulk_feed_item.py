from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *
from datetime import datetime

class BulkFeedItem(_SingleRecordBulkEntity):
    """ Represents a feed item.

    Properties of this class and of classes that it is derived from, correspond to fields of the Feed Item record in a bulk file.
    For more information, see Feed at https://go.microsoft.com/fwlink/?linkid=846127
    
    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """
    
    @staticmethod
    def _bulk_datetime_optional_str(value, id):
        if value is None:
            return None
        
        if not value:
            return "delete_value" if id > 0 else None
        
        return value.strftime('%Y/%m/%d %H:%M:%S')
    
    @staticmethod
    def _parse_datetime(value):
        
        if not value:
            return None
        try:
            if value == 'delete_value':
                return None
            else:
                return datetime.strptime(value, '%Y/%m/%d %H:%M:%S')
        except Exception:
            return parse_datetime(value)
        

    def __init__(self):
        super(BulkFeedItem, self).__init__()
        self._id = None
        self._feed_id = None
        self._campaign = None
        self._ad_group = None
        self._audience_id = None
        self._custom_attributes = None
        self._status = None
        self._start_date = None
        self._end_date = None
        self._keyword = None
        self._daytime_ranges = None
        self._match_type = None
        self._location_id = None
        self._intent_option = None
        self._device_preference = None
        self._adgroup_id = None
        self._campaign_id = None



    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.id),
            csv_to_field=lambda c, v: setattr(c, 'id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.feed_id),
            csv_to_field=lambda c, v: setattr(c, 'feed_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AudienceId,
            field_to_csv=lambda c: bulk_str(c.audience_id),
            csv_to_field=lambda c, v: setattr(c, 'audience_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Target,
            field_to_csv=lambda c: bulk_str(c.location_id),
            csv_to_field=lambda c, v: setattr(c, 'location_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MatchType,
            field_to_csv=lambda c: c.match_type,
            csv_to_field=lambda c, v: setattr(c, 'match_type', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.PhysicalIntent,
            field_to_csv=lambda c: c.intent_option,
            csv_to_field=lambda c, v: setattr(c, 'intent_option', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: bulk_str(c.campaign),
            csv_to_field=lambda c, v: setattr(c, 'campaign', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdGroup,
            field_to_csv=lambda c: bulk_str(c.ad_group),
            csv_to_field=lambda c, v: setattr(c, 'ad_group', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Keyword,
            field_to_csv=lambda c: bulk_str(c.keyword),
            csv_to_field=lambda c, v: setattr(c, 'keyword', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomAttributes,
            field_to_csv=lambda c: bulk_str(c.custom_attributes),
            csv_to_field=lambda c, v: setattr(c, 'custom_attributes', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DevicePreference,
            field_to_csv=lambda c: bulk_device_preference_str(c.device_preference),
            csv_to_field=lambda c, v: setattr(c, 'device_preference', parse_device_preference(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.StartDate,
            field_to_csv=lambda c: BulkFeedItem._bulk_datetime_optional_str(c.start_date, c.id),
            csv_to_field=lambda c, v: setattr(c, 'start_date', BulkFeedItem._parse_datetime(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.EndDate,
            field_to_csv=lambda c: BulkFeedItem._bulk_datetime_optional_str(c.end_date, c.id),
            csv_to_field=lambda c, v: setattr(c, 'end_date', BulkFeedItem._parse_datetime(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdSchedule,
            field_to_csv=lambda c: field_to_csv_FeedItemAdSchedule(c, c.id),
            csv_to_field=lambda c, v: csv_to_field_FeedItemAdSchedule(c, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TargetAdGroupId,
            field_to_csv=lambda c: bulk_optional_str(c.adgroup_id, c.id),
            csv_to_field=lambda c, v: setattr(c, 'adgroup_id', int(v) if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.TargetCampaignId,
            field_to_csv=lambda c: bulk_optional_str(c.campaign_id, c.id),
            csv_to_field=lambda c, v: setattr(c, 'campaign_id', int(v) if v else '')
        ),
    ]
    

    @property
    def device_preference(self):
        """ the id of the account which contains the feed
        Corresponds to the 'Device Preference' field in the bulk file.

        :rtype: long
        """
        return self._device_preference

    @device_preference.setter
    def device_preference(self, value):
        self._device_preference = value

    @property
    def intent_option(self):
        """ the id of the account which contains the feed
        Corresponds to the 'Physical Intent' field in the bulk file.

        :rtype: str
        """
        return self._intent_option

    @intent_option.setter
    def intent_option(self, value):
        self._intent_option = value
        
    @property
    def location_id(self):
        """ the id of the account which contains the feed
        Corresponds to the 'Target' field in the bulk file.

        :rtype: long
        """
        return self._location_id

    @location_id.setter
    def location_id(self, value):
        self._location_id = value
        
        
    @property
    def adgroup_id(self):
        """ the id of the account which contains the feed
        Corresponds to the 'Target Ad Group Id' field in the bulk file.

        :rtype: long
        """
        return self._adgroup_id

    @adgroup_id.setter
    def adgroup_id(self, value):
        self._adgroup_id = value

    @property
    def campaign_id(self):
        """ the id of the account which contains the feed
        Corresponds to the 'Target Campaign Id' field in the bulk file.

        :rtype: long
        """
        return self._campaign_id

    @campaign_id.setter
    def campaign_id(self, value):
        self._campaign_id = value

    @property
    def match_type(self):
        """ the match type of bulk record
        Corresponds to the 'Match Type' field in the bulk file.

        :rtype: str
        """
        return self._match_type

    @match_type.setter
    def match_type(self, value):
        self._match_type = value  
  
    @property
    def keyword(self):
        """ the status of bulk record
        Corresponds to the 'Keyword' field in the bulk file.

        :rtype: str
        """
        return self._keyword

    @keyword.setter
    def keyword(self, value):
        self._keyword = value
              
    @property
    def daytime_ranges(self):
        """ the status of bulk record
        Corresponds to the 'Ad Schedule' field in the bulk file.

        :rtype: str
        """
        return self._daytime_ranges

    @daytime_ranges.setter
    def daytime_ranges(self, value):
        self._daytime_ranges = value  
              
    @property
    def end_date(self):
        """ the status of bulk record
        Corresponds to the 'End Date' field in the bulk file.

        :rtype: str
        """
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value    
        
    @property
    def start_date(self):
        """ the status of bulk record
        Corresponds to the 'Start Date' field in the bulk file.

        :rtype: str
        """
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value


    @property
    def custom_attributes(self):
        """ the status of bulk record
        Corresponds to the 'Custom Attributes' field in the bulk file.

        :rtype: str
        """
        return self._custom_attributes

    @custom_attributes.setter
    def custom_attributes(self, value):
        self._custom_attributes = value

    @property
    def audience_id(self):
        """ the status of bulk record
        Corresponds to the 'Audience Id' field in the bulk file.

        :rtype: long
        """
        return self._audience_id

    @audience_id.setter
    def audience_id(self, value):
        self._audience_id = value

    @property
    def ad_group(self):
        """ the status of bulk record
        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """
        return self._ad_group

    @ad_group.setter
    def ad_group(self, value):
        self._ad_group = value

    @property
    def id(self):
        """ the status of bulk record
        Corresponds to the 'Id' field in the bulk file.

        :rtype: long
        """
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        

    @property
    def feed_id(self):
        """ the status of bulk record
        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: long
        """
        return self._feed_id

    @feed_id.setter
    def feed_id(self, value):
        self._feed_id = value    

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
    def campaign(self):
        """ the id of the account which contains the feed
        Corresponds to the 'campaign' field in the bulk file.

        :rtype: str
        """
        return self._campaign

    @campaign.setter
    def campaign(self, value):
        self._campaign = value
 
    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkFeedItem._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkFeedItem._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkFeedItem, self).read_additional_data(stream_reader)
