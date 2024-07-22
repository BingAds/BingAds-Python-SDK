from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


class BulkAccount(_SingleRecordBulkEntity):
    """ Represents an account that can be read or written in a bulk file.

    Properties of this class and of classes that it is derived from, correspond to fields of the Account record in a bulk file.
    For more information, see Account at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, customer_id=None, sync_time=None):
        super(BulkAccount, self).__init__()
        self._id = account_id
        self._customer_id = customer_id
        self._sync_time = sync_time
        self._msclkid_auto_tagging_enabled = None
        self._include_view_through_conversions = None
        self._profile_expansion_enabled = None
        self._tracking_url_template = None
        self._final_url_suffix = None
        self._ad_click_parallel_tracking=None
        self._auto_apply_recommendations = None
        self._allow_image_auto_retrieve = None
        self._business_attributes = None

    @property
    def id(self):
        """ The identifier of the account.

        Corresponds to the 'Id' field in the bulk file.

        :return: The identifier of the account.
        :rtype: int
        """

        return self._id

    @property
    def customer_id(self):
        """ The identifier of the customer that contains the account.

        Corresponds to the 'Parent Id' field in the bulk file.

        :return: The identifier of the customer that contains the account.
        :rtype: int
        """

        return self._customer_id

    @property
    def sync_time(self):
        """ The date and time that you last synced your account using the bulk service.

        You should keep track of this value in UTC time.
        Corresponds to the 'Sync Time' field in the bulk file.

        :return: The date and time that you last synced your account using the bulk service.
        :rtype: datetime.datetime
        """

        return self._sync_time

    @property
    def msclkid_auto_tagging_enabled(self):
        """ Determines whether auto-tagging of the MSCLKID query string parameter is enabled. The MSCLKID is a 32-character GUID that is unique for each ad click.
        :return: The msclkid autotag setting of the account
        :rtype: bool
        """
        return self._msclkid_auto_tagging_enabled

    @property
    def include_view_through_conversions(self):
        """
        :return: The 'Include View Through Conversions' field of the account
        :rtype: bool
        """
        return self._include_view_through_conversions

    @property
    def profile_expansion_enabled(self):
        """
        :return: The 'Profile Expansion Enabled' field of the account
        :rtype: bool
        """
        return self._profile_expansion_enabled

    @property
    def tracking_url_template(self):
        """ The tracking template to use as a default for all URLs in your account.

        :return: The tracking template of the account
        :rtype: str
        """
        return self._tracking_url_template

    @property
    def final_url_suffix(self):
        """ The final url suffix to use as a default for all URLs in your account.

        :return: The tracking template of the account
        :rtype: str
        """
        return self._final_url_suffix

    @final_url_suffix.setter
    def final_url_suffix(self, v):
        self._final_url_suffix = v

    @property
    def ad_click_parallel_tracking(self):
        """ The setting of parallel tracking in the account.

        :return: The setting of parallel tracking of the account
        :rtype: bool
        """
        return self._ad_click_parallel_tracking

    @ad_click_parallel_tracking.setter
    def ad_click_parallel_tracking(self, v):
        self._ad_click_parallel_tracking = v

    @property
    def allow_image_auto_retrieve(self):
        """ The setting of allowing image auto retrieve in the account.

        :return: The setting of allowing image auto retrieve of the account
        :rtype: bool
        """
        return self._allow_image_auto_retrieve

    @allow_image_auto_retrieve.setter
    def allow_image_auto_retrieve(self, v):
        self._allow_image_auto_retrieve = v

    @property
    def auto_apply_recommendations(self):
        """ The setting of allowing image auto retrieve in the account.

        :return: The setting of allowing image auto retrieve of the account
        :rtype: dict
        """
        return self._auto_apply_recommendations

    @auto_apply_recommendations.setter
    def auto_apply_recommendations(self, v):
        self._auto_apply_recommendations = v

    @property
    def business_attributes(self):
        """ The setting of business attributes in the account.

        :return: The setting of business attributes of the account
        :rtype: dict
        """
        return self._business_attributes

    @business_attributes.setter
    def business_attributes(self, v):
        self._business_attributes = v

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.id),
            csv_to_field=lambda c, v: setattr(c, '_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.customer_id),
            csv_to_field=lambda c, v: setattr(c, '_customer_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SyncTime,
            field_to_csv=lambda c: bulk_datetime_str(c.sync_time),
            csv_to_field=lambda c, v: setattr(c, '_sync_time', parse_datetime(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.MSCLKIDAutoTaggingEnabled,
            field_to_csv=lambda c: bulk_str(c.msclkid_auto_tagging_enabled),
            csv_to_field=lambda c, v: setattr(c, '_msclkid_auto_tagging_enabled', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_optional_str(c.tracking_url_template, c.id),
            csv_to_field=lambda c, v: setattr(c, '_tracking_url_template', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrlSuffix,
            field_to_csv=lambda c: bulk_optional_str(c.final_url_suffix, c.id),
            csv_to_field=lambda c, v: setattr(c, '_final_url_suffix', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.IncludeViewThroughConversions,
            field_to_csv=lambda c: bulk_str(c.include_view_through_conversions),
            csv_to_field=lambda c, v: setattr(c, '_include_view_through_conversions', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.ProfileExpansionEnabled,
            field_to_csv=lambda c: bulk_str(c.profile_expansion_enabled),
            csv_to_field=lambda c, v: setattr(c, '_profile_expansion_enabled', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdClickParallelTracking,
            field_to_csv=lambda c: bulk_str(c.ad_click_parallel_tracking),
            csv_to_field=lambda c, v: setattr(c, 'ad_click_parallel_tracking', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.AllowImageAutoRetrieve,
            field_to_csv=lambda c: bulk_str(c.allow_image_auto_retrieve),
            csv_to_field=lambda c, v: setattr(c, 'allow_image_auto_retrieve', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.AutoApplyRecommendations,
            field_to_csv=lambda c: dict_bulk_str(c.auto_apply_recommendations, ';'),
            csv_to_field=lambda c, v: setattr(c, 'auto_apply_recommendations', parse_dict(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.BusinessAttributes,
            field_to_csv=lambda c: multi_bulk_str(c.business_attributes, ';'),
            csv_to_field=lambda c, v: setattr(c, 'business_attributes', parse_multi(v))
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkAccount._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkAccount._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAccount, self).read_additional_data(stream_reader)
