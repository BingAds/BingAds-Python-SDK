from bingads.v11.bulk.entities import QualityScoreData, PerformanceData
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V11

from bingads.v11.internal.bulk.string_table import _StringTable
from bingads.v11.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v11.internal.bulk.mappings import _SimpleBulkMapping
from bingads.internal.extensions import *


class BulkAdGroup(_SingleRecordBulkEntity):
    """ Represents an ad group.

    This class exposes the property :attr:`ad_group` that can be read and written as fields of the Ad Group record
    in a bulk file.

    For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, campaign_id=None, campaign_name=None, ad_group=None):
        super(BulkAdGroup, self).__init__()

        self._campaign_id = campaign_id
        self._campaign_name = campaign_name
        self._ad_group = ad_group

        self._is_expired = None
        self._quality_score_data = None
        self._performance_data = None

    @property
    def campaign_id(self):
        """ The identifier of the campaign that contains the ad group.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._campaign_id

    @campaign_id.setter
    def campaign_id(self, campaign_id):
        self._campaign_id = campaign_id

    @property
    def campaign_name(self):
        """ The name of the campaign that contains the ad group.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @property
    def ad_group(self):
        """ The AdGroup Data Object of the Campaign Management Service.

        A subset of AdGroup properties are available in the Ad Group record.
        For more information, see Ad Group at https://go.microsoft.com/fwlink/?linkid=846127.
        """
        return self._ad_group

    @ad_group.setter
    def ad_group(self, ad_group):
        self._ad_group = ad_group

    @property
    def is_expired(self):
        """ Indicates whether the AdGroup is expired.

        :rtype: bool
        """

        return self._is_expired

    @property
    def quality_score_data(self):
        """ The quality score data for the ad group.

        :rtype: QualityScoreData
        """
        return self._quality_score_data

    @property
    def performance_data(self):
        """ The historical performance data for the ad group.

        :rtype: PerformanceData
        """

        return self._performance_data

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.ad_group.Id),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: 'Expired' if c.is_expired else bulk_str(c.ad_group.Status),
            csv_to_field=csv_to_status
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.campaign_id),
            csv_to_field=lambda c, v: setattr(c, 'campaign_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdGroup,
            field_to_csv=lambda c: c.ad_group.Name,
            csv_to_field=lambda c, v: setattr(c.ad_group, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.StartDate,
            field_to_csv=lambda c: bulk_date_str(c.ad_group.StartDate),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'StartDate', parse_date(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.EndDate,
            field_to_csv=lambda c: bulk_date_str(c.ad_group.EndDate),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'EndDate', parse_date(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.NetworkDistribution,
            field_to_csv=lambda c: bulk_str(c.ad_group.Network),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'Network', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.PricingModel,
            field_to_csv=lambda c: bulk_upper_str(c.ad_group.PricingModel),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'PricingModel', v.title() if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdRotation,
            field_to_csv=lambda c: ad_rotation_bulk_str(c.ad_group.AdRotation),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'AdRotation', parse_ad_rotation(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.SearchNetwork,
            field_to_csv=lambda c: None if not c.ad_group.AdDistribution else 'On' if 'Search' in c.ad_group.AdDistribution else 'Off',
            csv_to_field=lambda c, v: v == 'On' and setattr(
                c.ad_group,
                'AdDistribution',
                (c.ad_group.AdDistribution + ' ' + 'Search').strip()
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ContentNetwork,
            field_to_csv=lambda c: None if not c.ad_group.AdDistribution else 'On' if 'Content' in c.ad_group.AdDistribution else 'Off',
            csv_to_field=lambda c, v: v == 'On' and setattr(
                c.ad_group,
                'AdDistribution',
                (c.ad_group.AdDistribution + ' ' + 'Content').strip()
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.SearchBid,
            field_to_csv=lambda c: ad_group_bid_bulk_str(c.ad_group.SearchBid),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'SearchBid', parse_ad_group_bid(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.ContentBid,
            field_to_csv=lambda c: ad_group_bid_bulk_str(c.ad_group.ContentMatchBid),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'ContentMatchBid', parse_ad_group_bid(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.Language,
            field_to_csv=lambda c: c.ad_group.Language,
            csv_to_field=lambda c, v: setattr(c.ad_group, 'Language', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.ad_group.NativeBidAdjustment),
            csv_to_field=lambda c, v: setattr(
                c.ad_group,
                'NativeBidAdjustment',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.ad_group.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.ad_group),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.ad_group, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidStrategyType,
            field_to_csv=lambda c: field_to_csv_BidStrategyType(c.ad_group),
            csv_to_field=lambda c, v: csv_to_field_BidStrategyType(c.ad_group, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.RemarketingTargetingSetting,
            field_to_csv=lambda c: bulk_str(c.ad_group.RemarketingTargetingSetting),
            csv_to_field=lambda c, v: setattr(c.ad_group, 'RemarketingTargetingSetting', v if v else None)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.ad_group = _CAMPAIGN_OBJECT_FACTORY_V11.create('AdGroup')
        self.ad_group.AdDistribution = ''

        row_values.convert_to_entity(self, BulkAdGroup._MAPPINGS)

        self._quality_score_data = QualityScoreData.read_from_row_values_or_null(row_values)
        self._performance_data = PerformanceData.read_from_row_values_or_null(row_values)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._ad_group, 'AdGroup')
        self.convert_to_values(row_values, BulkAdGroup._MAPPINGS)
        if not exclude_readonly_data:
            QualityScoreData.write_to_row_values_if_not_null(self.quality_score_data, row_values)
            PerformanceData.write_to_row_values_if_not_null(self.performance_data, row_values)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroup, self).read_additional_data(stream_reader)
