from bingads.v11.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V11
from bingads.v11.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v11.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v11.internal.bulk.string_table import _StringTable
from bingads.v11.internal.extensions import *

class BulkCampaignRadiusCriterion(_SingleRecordBulkEntity):
    """ Represents an Campaign Radius Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_campaign_criterion` property that can be read and written as fields of the
    Campaign Radius Criterion record in a bulk file.

    For more information, see Campaign Radius Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_campaign_criterion=None,
                 campaign_name=None, ):
        super(BulkCampaignRadiusCriterion, self).__init__()

        self._biddable_campaign_criterion = biddable_campaign_criterion
        self._campaign_name = campaign_name

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.biddable_campaign_criterion.Status),
            csv_to_field=lambda c, v: setattr(c.biddable_campaign_criterion, 'Status', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.biddable_campaign_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.biddable_campaign_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.biddable_campaign_criterion.CampaignId),
            csv_to_field=lambda c, v: setattr(c.biddable_campaign_criterion, 'CampaignId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.BidAdjustment,
            field_to_csv=lambda c: field_to_csv_BidAdjustment(c.biddable_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_BidAdjustment(c.biddable_campaign_criterion, float(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Name,
            field_to_csv=lambda c: field_to_csv_RadiusName(c.biddable_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_RadiusName(c.biddable_campaign_criterion, v)
        ),
        _SimpleBulkMapping(
            _StringTable.Radius,
            field_to_csv=lambda c: field_to_csv_Radius(c.biddable_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_Radius(c.biddable_campaign_criterion, long(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Unit,
            field_to_csv=lambda c: field_to_csv_RadiusUnit(c.biddable_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_RadiusUnit(c.biddable_campaign_criterion, v)
        ),
        _SimpleBulkMapping(
            _StringTable.Latitude,
            field_to_csv=lambda c: field_to_csv_LatitudeDegrees(c.biddable_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_LatitudeDegrees(c.biddable_campaign_criterion, float(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Longitude,
            field_to_csv=lambda c: field_to_csv_LongitudeDegrees(c.biddable_campaign_criterion),
            csv_to_field=lambda c, v: csv_to_field_LongitudeDegrees(c.biddable_campaign_criterion, float(v) if v else None)
        ),
    ]

    @property
    def biddable_campaign_criterion(self):
        """ Defines a Campaign Criterion """

        return self._biddable_campaign_criterion

    @biddable_campaign_criterion.setter
    def biddable_campaign_criterion(self, biddable_campaign_criterion):
        self._biddable_campaign_criterion = biddable_campaign_criterion

    @property
    def campaign_name(self):
        """ The name of the Campaign

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.biddable_campaign_criterion, 'biddable_campaign_criterion')
        self.convert_to_values(row_values, BulkCampaignRadiusCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._biddable_campaign_criterion = _CAMPAIGN_OBJECT_FACTORY_V11.create('BiddableCampaignCriterion')
        self._biddable_campaign_criterion.Type = 'BiddableCampaignCriterion'
        self._biddable_campaign_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V11.create('RadiusCriterion')
        self._biddable_campaign_criterion.Criterion.Type = 'RadiusCriterion'
        self._biddable_campaign_criterion.CriterionBid = _CAMPAIGN_OBJECT_FACTORY_V11.create('BidMultiplier')
        self._biddable_campaign_criterion.CriterionBid.Type = 'BidMultiplier'
        row_values.convert_to_entity(self, BulkCampaignRadiusCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignRadiusCriterion, self).read_additional_data(stream_reader)
