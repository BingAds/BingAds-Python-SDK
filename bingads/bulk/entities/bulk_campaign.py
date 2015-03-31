from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY
from bingads.bulk.entities import QualityScoreData, PerformanceData
from bingads.internal.bulk.string_table import _StringTable
from bingads.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.internal.extensions import bulk_str, csv_to_budget, budget_to_csv


class BulkCampaign(_SingleRecordBulkEntity):
    """ Represents a campaign that can be read or written in a bulk file.

    This class exposes the :attr:`campaign` property that can be read and written as fields of the
    Campaign record in a bulk file.

    For more information, see Campaign at http://go.microsoft.com/fwlink/?LinkID=511521.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, campaign=None):
        super(BulkCampaign, self).__init__()

        self._account_id = account_id
        self._campaign = campaign
        self._quality_score_data = None
        self._performance_data = None

    @property
    def account_id(self):
        """ The identifier of the account that contains the campaign.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    @property
    def campaign(self):
        """ Defines a campaign within an account.

        See Campaign at https://msdn.microsoft.com/en-us/library/bing-ads-campaign-management-campaign.aspx
        """

        return self._campaign

    @campaign.setter
    def campaign(self, campaign):
        self._campaign = campaign

    @property
    def quality_score_data(self):
        """ The quality score data for the campaign.

        :rtype: QualityScoreData
        """

        return self._quality_score_data

    @property
    def performance_data(self):
        """ The historical performance data for the campaign

        :rtype: PerformanceData
        """

        return self._performance_data

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.campaign.Status),
            csv_to_field=lambda c, v: setattr(
                c.campaign,
                'Status',
                v if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.campaign.Id),
            csv_to_field=lambda c, v: setattr(
                c.campaign,
                'Id',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, '_account_id', int(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign.Name,
            csv_to_field=lambda c, v: setattr(c.campaign, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TimeZone,
            field_to_csv=lambda c: c.campaign.TimeZone,
            csv_to_field=lambda c, v: setattr(c.campaign, 'TimeZone', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BudgetType,
            field_to_csv=lambda c: bulk_str(c.campaign.BudgetType),
            csv_to_field=lambda c, v: setattr(
                c.campaign,
                'BudgetType',
                v if v else None
            )
        ),
        _ComplexBulkMapping(budget_to_csv, csv_to_budget)
    ]

    def read_additional_data(self, stream_reader):
        super(BulkCampaign, self).read_additional_data(stream_reader)

    def process_mappings_from_row_values(self, row_values):
        self._campaign = _CAMPAIGN_OBJECT_FACTORY.create('Campaign')
        row_values.convert_to_entity(self, BulkCampaign._MAPPINGS)
        self._quality_score_data = QualityScoreData.read_from_row_values_or_null(row_values)
        self._performance_data = PerformanceData.read_from_row_values_or_null(row_values)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.campaign, 'campaign')
        self.convert_to_values(row_values, BulkCampaign._MAPPINGS)
        if not exclude_readonly_data:
            QualityScoreData.write_to_row_values_if_not_null(self.quality_score_data, row_values)
            PerformanceData.write_to_row_values_if_not_null(self.performance_data, row_values)
