from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *


class BulkAdGroupNegativeDynamicSearchAdTarget(_SingleRecordBulkEntity):
    """ Represents a Ad Group Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Negative Dynamic Search Ad Target record in a bulk file.

    For more information, see Ad Group Negative Dynamic Search Ad Target at https://go.microsoft.com/fwlink/?linkid=836838.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 campaign_name=None,
                 ad_group_name=None,
                 status=None,
                 negative_ad_group_criterion=None):
        super(BulkAdGroupNegativeDynamicSearchAdTarget, self).__init__()

        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name
        self._status = status
        self._negative_ad_group_criterion = negative_ad_group_criterion


    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.status,
            csv_to_field=lambda c, v: setattr(c, 'status', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.negative_ad_group_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.negative_ad_group_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.negative_ad_group_criterion.AdGroupId),
            csv_to_field=lambda c, v: setattr(c.negative_ad_group_criterion, 'AdGroupId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdGroup,
            field_to_csv=lambda c: c.ad_group_name,
            csv_to_field=lambda c, v: setattr(c, 'ad_group_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: field_to_csv_WebpageParameter_CriterionName(c.negative_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_WebpageParameter_CriterionName(c.negative_ad_group_criterion, v)
        ),
        _ComplexBulkMapping(
            entity_to_csv=lambda c, v: entity_to_csv_DSAWebpageParameter(c.negative_ad_group_criterion, v),
            csv_to_entity=lambda v, c: csv_to_entity_DSAWebpageParameter(v, c.negative_ad_group_criterion)
        ),
    ]

    @property
    def campaign_name(self):
        """ The name of the Campaign

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    @property
    def ad_group_name(self):
        """ The name of the Ad Group

        :rtype: str
        """

        return self._ad_group_name

    @ad_group_name.setter
    def ad_group_name(self, ad_group_name):
        self._ad_group_name = ad_group_name

    @property
    def status(self):
        """ The status of the Ad Group Criterion

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def negative_ad_group_criterion(self):
        """ Defines a Ad Group Criterion """

        return self._negative_ad_group_criterion

    @negative_ad_group_criterion.setter
    def negative_ad_group_criterion(self, negative_ad_group_criterion):
        self._negative_ad_group_criterion = negative_ad_group_criterion

    def process_mappings_from_row_values(self, row_values):
        self._negative_ad_group_criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('NegativeAdGroupCriterion')
        self._negative_ad_group_criterion.Type = 'NegativeAdGroupCriterion'
        self._negative_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('Webpage')
        self._negative_ad_group_criterion.Criterion.Type = 'Webpage'

        row_values.convert_to_entity(self, BulkAdGroupNegativeDynamicSearchAdTarget._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.negative_ad_group_criterion, 'negative_ad_group_criterion')
        self.convert_to_values(row_values, BulkAdGroupNegativeDynamicSearchAdTarget._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupNegativeDynamicSearchAdTarget, self).read_additional_data(stream_reader)
