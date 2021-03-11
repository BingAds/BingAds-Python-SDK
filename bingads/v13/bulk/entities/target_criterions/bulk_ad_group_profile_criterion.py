from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_biddable_criterion import BulkAdGroupBiddableCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from abc import ABCMeta, abstractmethod

class BulkAdGroupProfileCriterion(BulkAdGroupBiddableCriterion):
    """ The base class for Ad Group level profile criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_ad_group_criterion` property that can be read and written in a bulk file.

    For more information, see Bulk File Schema at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupProfileCriterion, self).__init__(biddable_ad_group_criterion, campaign_name, ad_group_name)

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Profile,
            field_to_csv=lambda c: c.profile_name,
            csv_to_field=lambda c, v: setattr(c, 'profile_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.ProfileId,
            field_to_csv=lambda c: bulk_str(c.biddable_ad_group_criterion.Criterion.ProfileId),
            csv_to_field=lambda c, v: setattr(c.biddable_ad_group_criterion.Criterion, 'ProfileId', int(v) if v else None)
        ),
    ]


    def create_criterion(self):
        self._biddable_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('ProfileCriterion')
        self._biddable_ad_group_criterion.Criterion.ProfileType = self.profile_type()
        self._biddable_ad_group_criterion.Criterion.Type = 'ProfileCriterion'

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkAdGroupProfileCriterion, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAdGroupProfileCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkAdGroupProfileCriterion, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAdGroupProfileCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupProfileCriterion, self).read_additional_data(stream_reader)


class BulkAdGroupCompanyNameCriterion(BulkAdGroupProfileCriterion):
    """ Represents an Ad Group CompanyName Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_ad_group_criterion` property that can be read and written as fields of the
    Ad Group CompanyName Criterion record in a bulk file.

    For more information, see Ad Group CompanyName Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupCompanyNameCriterion, self).__init__()

        self._biddable_ad_group_criterion = biddable_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name =ad_group_name
        
    def profile_type(self):
        return 'CompanyName'
    
    
class BulkAdGroupIndustryCriterion(BulkAdGroupProfileCriterion):
    """ Represents an Ad Group Industry Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Industry Criterion record in a bulk file.

    For more information, see Ad Group Industry Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupIndustryCriterion, self).__init__()

        self._biddable_ad_group_criterion = biddable_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name =ad_group_name
        
    def profile_type(self):
        return 'Industry'
    
    
class BulkAdGroupJobFunctionCriterion(BulkAdGroupProfileCriterion):
    """ Represents an Ad Group JobFunction Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_ad_group_criterion` property that can be read and written as fields of the
    Ad Group JobFunction Criterion record in a bulk file.

    For more information, see Ad Group JobFunction Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_ad_group_criterion=None,
                 campaign_name=None,
                 ad_group_name=None, ):
        super(BulkAdGroupJobFunctionCriterion, self).__init__()

        self._biddable_ad_group_criterion = biddable_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name =ad_group_name
        
    def profile_type(self):
        return 'JobFunction'