from bingads.v11.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V11
from bingads.v11.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v11.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v11.internal.bulk.string_table import _StringTable
from bingads.v11.internal.extensions import *
from abc import ABCMeta, abstractmethod

class BulkAdGroupProfileCriterion(_SingleRecordBulkEntity):
    """ Represents an Ad Group Profile Criterion that can be read or written in a bulk file.

    This class exposes the :attr:`biddable_ad_group_criterion` property that can be read and written as fields of the
    Ad Group Profile Criterion record in a bulk file.

    For more information, see Ad Group Profile Criterion at https://go.microsoft.com/fwlink/?linkid=846127.

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
        super(BulkAdGroupProfileCriterion, self).__init__()

        self._biddable_ad_group_criterion = biddable_ad_group_criterion
        self._campaign_name = campaign_name
        self._ad_group_name =ad_group_name

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.biddable_ad_group_criterion.Status),
            csv_to_field=lambda c, v: setattr(c.biddable_ad_group_criterion, 'Status', v if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.biddable_ad_group_criterion.Id),
            csv_to_field=lambda c, v: setattr(c.biddable_ad_group_criterion, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.biddable_ad_group_criterion.AdGroupId),
            csv_to_field=lambda c, v: setattr(c.biddable_ad_group_criterion, 'AdGroupId', int(v) if v else None)
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
            _StringTable.BidAdjustment,
            field_to_csv=lambda c: field_to_csv_BidAdjustment(c.biddable_ad_group_criterion),
            csv_to_field=lambda c, v: csv_to_field_BidAdjustment(c.biddable_ad_group_criterion, float(v) if v else None)
        ),
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
    


    @property
    def biddable_ad_group_criterion(self):
        """ Defines a Ad Group Criterion """

        return self._biddable_ad_group_criterion

    @biddable_ad_group_criterion.setter
    def biddable_ad_group_criterion(self, biddable_ad_group_criterion):
        self._biddable_ad_group_criterion = biddable_ad_group_criterion

    @property
    def campaign_name(self):
        """ The name of the Campaign

        :rtype: str
        """

        return self._campaign_name
    
    @abstractmethod
    def profile_type(self):
        pass

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
        self._validate_property_not_null(self.biddable_ad_group_criterion, 'biddable_ad_group_criterion')
        self.convert_to_values(row_values, BulkAdGroupProfileCriterion._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._biddable_ad_group_criterion = _CAMPAIGN_OBJECT_FACTORY_V11.create('BiddableAdGroupCriterion')
        self._biddable_ad_group_criterion.Type = 'BiddableAdGroupCriterion'
        self._biddable_ad_group_criterion.Criterion = _CAMPAIGN_OBJECT_FACTORY_V11.create('ProfileCriterion')
        self._biddable_ad_group_criterion.Criterion.ProfileType = self.profile_type()
        self._biddable_ad_group_criterion.Criterion.Type = 'ProfileCriterion'
        self._biddable_ad_group_criterion.CriterionBid = _CAMPAIGN_OBJECT_FACTORY_V11.create('BidMultiplier')
        self._biddable_ad_group_criterion.CriterionBid.Type = 'BidMultiplier'
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