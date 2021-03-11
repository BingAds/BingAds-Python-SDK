from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_negative_criterion import BulkAdGroupNegativeCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from abc import ABCMeta, abstractmethod


class BulkAdGroupNegativeProfileCriterion(BulkAdGroupNegativeCriterion):
    """ Represents an Ad Group Negative Profile Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`negative_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Negative Profile Criterion record in a bulk file.

    For more information, see Ad Group Negative Profile Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

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
        super(BulkAdGroupNegativeProfileCriterion, self).__init__(negative_ad_group_criterion, campaign_name, ad_group_name)

    _MAPPINGS = [
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

    def create_criterion(self):
        self._negative_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('ProfileCriterion')
        self._negative_ad_group_criterion.Criterion.Type = 'ProfileCriterion'
        self._negative_ad_group_criterion.Criterion.ProfileType = self.profile_type()

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkAdGroupNegativeProfileCriterion, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAdGroupNegativeProfileCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkAdGroupNegativeProfileCriterion, self).process_mappings_from_row_values(row_values)
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