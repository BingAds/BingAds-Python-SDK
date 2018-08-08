from bingads.v11.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V11
from bingads.v11.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v11.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v11.internal.bulk.string_table import _StringTable
from bingads.v11.internal.extensions import *
from abc import ABCMeta, abstractmethod

class BulkAdGroupNegativeProfileCriterion(_SingleRecordBulkEntity):
    """ The base class for Ad group level negative profile criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_ad_group_criterion` property that can be read and written in a bulk file.

    For more information, see Bulk File Schema at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManProfiler`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 negative_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupNegativeProfileCriterion, self).__init__()

        self._negative_ad_group_criterion = negative_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.negative_ad_group_criterion.Status),
            csv_to_field=lambda c, v: setattr(c.negative_ad_group_criterion, 'Status', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.negative_ad_group_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.negative_ad_group_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.negative_ad_group_criterion.AdGroupId),
            csv_to_field=lambda c, v: setattr(c.negative_ad_group_criterion, 'AdGroupId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.AdGroup,
            field_to_csv=lambda c: c.ad_group_name,
            csv_to_field=lambda c, v: setattr(c, 'ad_group_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.Profile,
            field_to_csv=lambda c: c.profile_name,
            csv_to_field=lambda c, v: setattr(c, 'profile_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.ProfileId,
            field_to_csv=lambda c: bulk_str(c.negative_ad_group_criterion.Criterion.ProfileId),
            csv_to_field=lambda c, v: setattr(c.negative_ad_group_criterion.Criterion, 'ProfileId', int(v) if v else None)
        ),
    ]

    @property
    def negative_ad_group_criterion(self):
        """ Defines a Ad Group Criterion """

        return self._negative_ad_group_criterion

    @negative_ad_group_criterion.setter
    def negative_ad_group_criterion(self, negative_ad_group_criterion):
        self._negative_ad_group_criterion = negative_ad_group_criterion

    @property
    def campaign_name(self):
        """ The name of the Campaign

        :rtype: str
        """

        return self._campaign_name

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


    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.negative_ad_group_criterion, 'negative_ad_group_criterion')
        self.convert_to_values(row_values, BulkAdGroupNegativeProfileCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._negative_ad_group_criterion = _CAMPAIGN_OBJECT_FACTORY_V11.create('NegativeAdGroupCriterion')
        self._negative_ad_group_criterion.Type = 'NegativeAdGroupCriterion'
        self._negative_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V11.create('ProfileCriterion')
        self._negative_ad_group_criterion.Criterion.Type = 'ProfileCriterion'
        self._negative_ad_group_criterion.Criterion.ProfileType = self.profile_type()
        row_values.convert_to_entity(self, BulkAdGroupNegativeProfileCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupNegativeProfileCriterion, self).read_additional_data(stream_reader)

    @abstractmethod
    def profile_type(self):
        pass

class BulkAdGroupNegativeCompanyNameCriterion(BulkAdGroupNegativeProfileCriterion):
    """ Represents an Ad Group Negative CompanyName Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Negative CompanyName Criterion record in a bulk file.

    For more information, see Ad Group Negative CompanyName Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManCompanyNamer`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 negative_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupNegativeCompanyNameCriterion, self).__init__()

        self._negative_ad_group_criterion = negative_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name
        
    def profile_type(self):
        return 'CompanyName'
    
    
class BulkAdGroupNegativeIndustryCriterion(BulkAdGroupNegativeProfileCriterion):
    """ Represents an Ad Group Negative Industry Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Negative Industry Criterion record in a bulk file.

    For more information, see Ad Group Negative Industry Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManIndustryr`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 negative_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupNegativeIndustryCriterion, self).__init__()

        self._negative_ad_group_criterion = negative_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name
 
    def profile_type(self):
        return 'Industry'
    
    
class BulkAdGroupNegativeJobFunctionCriterion(BulkAdGroupNegativeProfileCriterion):
    """ Represents an Ad Group Negative JobFunction Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Negative JobFunction Criterion record in a bulk file.

    For more information, see Ad Group Negative JobFunction Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManJobFunctionr`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 negative_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupNegativeJobFunctionCriterion, self).__init__()

        self._negative_ad_group_criterion = negative_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name = ad_group_name

    def profile_type(self):
        return 'JobFunction'