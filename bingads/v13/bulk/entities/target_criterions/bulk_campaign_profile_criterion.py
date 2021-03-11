from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities.target_criterions.bulk_campaign_biddable_criterion import BulkCampaignBiddableCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from abc import ABCMeta, abstractmethod

class BulkCampaignProfileCriterion(BulkCampaignBiddableCriterion):
    """ The base class for campaign level profile criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_campaign_criterion` property that can be read and written in a bulk file.

    For more information, see Bulk File Schema at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_campaign_criterion=None,
                 campaign_name=None, ):
        super(BulkCampaignProfileCriterion, self).__init__(biddable_campaign_criterion, campaign_name)

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Profile,
            field_to_csv=lambda c: c.profile_name,
            csv_to_field=lambda c, v: setattr(c, 'profile_name', v)
        ),
        _SimpleBulkMapping(
            _StringTable.ProfileId,
            field_to_csv=lambda c: bulk_str(c.biddable_campaign_criterion.Criterion.ProfileId),
            csv_to_field=lambda c, v: setattr(c.biddable_campaign_criterion.Criterion, 'ProfileId', int(v) if v else None)
        ),
    ]
    
    def create_criterion(self):
        self._biddable_campaign_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V13.create('ProfileCriterion')
        self._biddable_campaign_criterion.Criterion.ProfileType = self.profile_type()
        self._biddable_campaign_criterion.Criterion.Type = 'ProfileCriterion'

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkCampaignProfileCriterion, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkCampaignProfileCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkCampaignProfileCriterion, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkCampaignProfileCriterion._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignProfileCriterion, self).read_additional_data(stream_reader)

    @abstractmethod
    def profile_type(self):
        pass

class BulkCampaignCompanyNameCriterion(BulkCampaignProfileCriterion):
    """ Represents an Campaign CompanyName Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_campaign_criterion` property that can be read and written as fields of the
    Campaign CompanyName Criterion record in a bulk file.

    For more information, see Campaign CompanyName Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_campaign_criterion=None,
                 campaign_name=None):
        super(BulkCampaignCompanyNameCriterion, self).__init__()

        self._biddable_campaign_criterion = biddable_campaign_criterion
        self._campaign_name = campaign_name

    def profile_type(self):
        return 'CompanyName'

class BulkCampaignIndustryCriterion(BulkCampaignProfileCriterion):
    """ Represents an Campaign Industry Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_campaign_criterion` property that can be read and written as fields of the
    Campaign Industry Criterion record in a bulk file.

    For more information, see Campaign Industry Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_campaign_criterion=None,
                 campaign_name=None):
        super(BulkCampaignIndustryCriterion, self).__init__()

        self._biddable_campaign_criterion = biddable_campaign_criterion
        self._campaign_name = campaign_name

    def profile_type(self):
        return 'Industry'

class BulkCampaignJobFunctionCriterion(BulkCampaignProfileCriterion):
    """ Represents an Campaign JobFunction Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_campaign_criterion` property that can be read and written as fields of the
    Campaign JobFunction Criterion record in a bulk file.

    For more information, see Campaign JobFunction Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 biddable_campaign_criterion=None,
                 campaign_name=None):
        super(BulkCampaignJobFunctionCriterion, self).__init__()

        self._biddable_campaign_criterion = biddable_campaign_criterion
        self._campaign_name = campaign_name

    def profile_type(self):
        return 'JobFunction'