from bingads.v12.bulk.entities import *
from bingads.v12.internal.bulk.string_table import _StringTable
from bingads.v12.internal.bulk.entity_info import _EntityInfo
from bingads.v12.bulk.entities.bulk_negative_sites import _BulkAdGroupNegativeSitesIdentifier, \
    _BulkCampaignNegativeSitesIdentifier
from bingads.v12.internal.bulk.format_version import _FormatVersion


class _BulkObjectFactory():
    INDIVIDUAL_ENTITY_MAP = {
        _StringTable.Account: _EntityInfo(lambda: BulkAccount()),
        _StringTable.Budget: _EntityInfo(lambda: BulkBudget()),
        _StringTable.Campaign: _EntityInfo(lambda: BulkCampaign()),
        _StringTable.AdGroup: _EntityInfo(lambda: BulkAdGroup()),
        _StringTable.Keyword: _EntityInfo(lambda: BulkKeyword()),
        _StringTable.CallAdExtension: _EntityInfo(lambda: BulkCallAdExtension()),
        _StringTable.CampaignCallAdExtension: _EntityInfo(lambda: BulkCampaignCallAdExtension()),
        _StringTable.ImageAdExtension: _EntityInfo(lambda: BulkImageAdExtension()),
        _StringTable.AccountImageAdExtension: _EntityInfo(lambda: BulkAccountImageAdExtension()),
        _StringTable.CampaignImageAdExtension: _EntityInfo(lambda: BulkCampaignImageAdExtension()),
        _StringTable.AdGroupImageAdExtension: _EntityInfo(lambda: BulkAdGroupImageAdExtension()),
        _StringTable.CalloutAdExtension: _EntityInfo(lambda: BulkCalloutAdExtension()),
        _StringTable.AccountCalloutAdExtension: _EntityInfo(lambda: BulkAccountCalloutAdExtension()),
        _StringTable.CampaignCalloutAdExtension: _EntityInfo(lambda: BulkCampaignCalloutAdExtension()),
        _StringTable.AdGroupCalloutAdExtension: _EntityInfo(lambda: BulkAdGroupCalloutAdExtension()),
        _StringTable.ReviewAdExtension: _EntityInfo(lambda: BulkReviewAdExtension()),
        _StringTable.AccountReviewAdExtension: _EntityInfo(lambda: BulkAccountReviewAdExtension()),
        _StringTable.CampaignReviewAdExtension: _EntityInfo(lambda: BulkCampaignReviewAdExtension()),
        _StringTable.AdGroupReviewAdExtension: _EntityInfo(lambda: BulkAdGroupReviewAdExtension()),
        _StringTable.LocationAdExtension: _EntityInfo(lambda: BulkLocationAdExtension()),
        _StringTable.AccountLocationAdExtension: _EntityInfo(lambda: BulkAccountLocationAdExtension()),
        _StringTable.CampaignLocationAdExtension: _EntityInfo(lambda: BulkCampaignLocationAdExtension()),
        _StringTable.AppAdExtension: _EntityInfo(lambda: BulkAppAdExtension()),
        _StringTable.AccountAppAdExtension: _EntityInfo(lambda: BulkAccountAppAdExtension()),
        _StringTable.CampaignAppAdExtension: _EntityInfo(lambda: BulkCampaignAppAdExtension()),
        _StringTable.AdGroupAppAdExtension: _EntityInfo(lambda: BulkAdGroupAppAdExtension()),
        _StringTable.StructuredSnippetAdExtension: _EntityInfo(lambda: BulkStructuredSnippetAdExtension()),
        _StringTable.AccountStructuredSnippetAdExtension: _EntityInfo(lambda: BulkAccountStructuredSnippetAdExtension()),
        _StringTable.CampaignStructuredSnippetAdExtension: _EntityInfo(lambda: BulkCampaignStructuredSnippetAdExtension()),
        _StringTable.AdGroupStructuredSnippetAdExtension: _EntityInfo(lambda: BulkAdGroupStructuredSnippetAdExtension()),
        _StringTable.SitelinkAdExtension: _EntityInfo(lambda: BulkSitelinkAdExtension()),
        _StringTable.AccountSitelinkAdExtension: _EntityInfo(lambda: BulkAccountSitelinkAdExtension()),
        _StringTable.CampaignSitelinkAdExtension: _EntityInfo(lambda: BulkCampaignSitelinkAdExtension()),
        _StringTable.AdGroupSitelinkAdExtension: _EntityInfo(lambda: BulkAdGroupSitelinkAdExtension()),
        _StringTable.PriceAdExtension: _EntityInfo(lambda: BulkPriceAdExtension()),
        _StringTable.AccountPriceAdExtension: _EntityInfo(lambda: BulkAccountPriceAdExtension()),
        _StringTable.CampaignPriceAdExtension: _EntityInfo(lambda: BulkCampaignPriceAdExtension()),
        _StringTable.AdGroupPriceAdExtension: _EntityInfo(lambda: BulkAdGroupPriceAdExtension()),
        _StringTable.ProductAd: _EntityInfo(lambda: BulkProductAd()),
        _StringTable.TextAd: _EntityInfo(lambda: BulkTextAd()),
        _StringTable.AppInstallAd: _EntityInfo(lambda: BulkAppInstallAd()),
        _StringTable.ExpandedTextAd: _EntityInfo(lambda: BulkExpandedTextAd()),
        _StringTable.DynamicSearchAd: _EntityInfo(lambda: BulkDynamicSearchAd()),
        "Campaign Negative Site": _EntityInfo(
            lambda: BulkCampaignNegativeSite(),
            _StringTable.Website,
            lambda: _BulkCampaignNegativeSitesIdentifier()
        ),
        "Ad Group Negative Site": _EntityInfo(
            lambda: BulkAdGroupNegativeSite(),
            _StringTable.Website,
            lambda: _BulkAdGroupNegativeSitesIdentifier()
        ),

        _StringTable.NegativeKeywordList: _EntityInfo(lambda: BulkNegativeKeywordList()),
        _StringTable.ListNegativeKeyword: _EntityInfo(lambda: BulkSharedNegativeKeyword()),
        _StringTable.CampaignNegativeKeywordList: _EntityInfo(lambda: BulkCampaignNegativeKeywordList()),
        _StringTable.CampaignNegativeKeyword: _EntityInfo(lambda: BulkCampaignNegativeKeyword()),
        _StringTable.AdGroupNegativeKeyword: _EntityInfo(lambda: BulkAdGroupNegativeKeyword()),
        'Campaign Product Scope': _EntityInfo(lambda : BulkCampaignProductScope()),
        'Ad Group Product Partition': _EntityInfo(lambda : BulkAdGroupProductPartition()),
        'Remarketing List': _EntityInfo(lambda : BulkRemarketingList()),
        'Ad Group Remarketing List Association': _EntityInfo(lambda : BulkAdGroupRemarketingListAssociation()),
        'Ad Group Negative Remarketing List Association': _EntityInfo(lambda : BulkAdGroupNegativeRemarketingListAssociation()),
        'Custom Audience': _EntityInfo(lambda : BulkCustomAudience()),
        'Ad Group Custom Audience Association': _EntityInfo(lambda : BulkAdGroupCustomAudienceAssociation()),
        'Ad Group Negative Custom Audience Association': _EntityInfo(lambda : BulkAdGroupNegativeCustomAudienceAssociation()),
        'In Market Audience': _EntityInfo(lambda : BulkInMarketAudience()),
        'Ad Group In Market Audience Association': _EntityInfo(lambda : BulkAdGroupInMarketAudienceAssociation()),
        'Ad Group Negative In Market Audience Association': _EntityInfo(lambda : BulkAdGroupNegativeInMarketAudienceAssociation()),
        'Campaign Negative Dynamic Search Ad Target': _EntityInfo(lambda: BulkCampaignNegativeDynamicSearchAdTarget()),
        'Ad Group Dynamic Search Ad Target': _EntityInfo(lambda: BulkAdGroupDynamicSearchAdTarget()),
        'Ad Group Negative Dynamic Search Ad Target': _EntityInfo(lambda: BulkAdGroupNegativeDynamicSearchAdTarget()),
        'Ad Group Age Criterion': _EntityInfo(lambda: BulkAdGroupAgeCriterion()),
        'Ad Group DayTime Criterion': _EntityInfo(lambda: BulkAdGroupDayTimeCriterion()),
        'Ad Group DeviceOS Criterion': _EntityInfo(lambda: BulkAdGroupDeviceCriterion()),
        'Ad Group Gender Criterion': _EntityInfo(lambda: BulkAdGroupGenderCriterion()),
        'Ad Group Location Criterion': _EntityInfo(lambda: BulkAdGroupLocationCriterion()),
        'Ad Group Location Intent Criterion': _EntityInfo(lambda: BulkAdGroupLocationIntentCriterion()),
        'Ad Group Negative Location Criterion': _EntityInfo(lambda: BulkAdGroupNegativeLocationCriterion()),
        'Ad Group Radius Criterion': _EntityInfo(lambda: BulkAdGroupRadiusCriterion()),
        'Campaign Age Criterion': _EntityInfo(lambda: BulkCampaignAgeCriterion()),
        'Campaign DayTime Criterion': _EntityInfo(lambda: BulkCampaignDayTimeCriterion()),
        'Campaign DeviceOS Criterion': _EntityInfo(lambda: BulkCampaignDeviceCriterion()),
        'Campaign Gender Criterion': _EntityInfo(lambda: BulkCampaignGenderCriterion()),
        'Campaign Location Criterion': _EntityInfo(lambda: BulkCampaignLocationCriterion()),
        'Campaign Location Intent Criterion': _EntityInfo(lambda: BulkCampaignLocationIntentCriterion()),
        'Campaign Negative Location Criterion': _EntityInfo(lambda: BulkCampaignNegativeLocationCriterion()),
        'Campaign Radius Criterion': _EntityInfo(lambda: BulkCampaignRadiusCriterion()),
        _StringTable.Label: _EntityInfo(lambda: BulkLabel()),
        _StringTable.CampaignLabel: _EntityInfo(lambda: BulkCampaignLabel()),
        _StringTable.AdGroupLabel: _EntityInfo(lambda: BulkAdGroupLabel()),
        _StringTable.KeywordLabel: _EntityInfo(lambda: BulkKeywordLabel()),
        _StringTable.AppInstallAdLabel: _EntityInfo(lambda: BulkAppInstallAdLabel()),
        _StringTable.DynamicSearchAdLabel: _EntityInfo(lambda: BulkDynamicSearchAdLabel()),
        _StringTable.ExpandedTextAdLabel: _EntityInfo(lambda: BulkExpandedTextAdLabel()),
        _StringTable.ProductAdLabel: _EntityInfo(lambda: BulkProductAdLabel()),
        _StringTable.OfflineConversion: _EntityInfo(lambda: BulkOfflineConversion()),
    }

    ADDITIONAL_OBJECT_MAP = {
        'Format Version': lambda: _FormatVersion(),
        'Keyword Best Position Bid': lambda: BulkKeywordBestPositionBid(),
        'Keyword Main Line Bid': lambda: BulkKeywordMainLineBid(),
        'Keyword First Page Bid': lambda: BulkKeywordFirstPageBid(),
    }

    TYPE_REVERSE_MAP = {}
    TARGET_IDENTIFIER_TYPE_REVERSE_MAP = {}

    @staticmethod
    def create_bulk_object(row_values):
        type_column = row_values[_StringTable.Type]

        if type_column.endswith('Error'):
            return BulkError()
        elif type_column in _BulkObjectFactory.ADDITIONAL_OBJECT_MAP:
            return _BulkObjectFactory.ADDITIONAL_OBJECT_MAP[type_column]()
        elif type_column in _BulkObjectFactory.INDIVIDUAL_ENTITY_MAP:
            info = _BulkObjectFactory.INDIVIDUAL_ENTITY_MAP[type_column]
            if row_values[_StringTable.Status] == 'Deleted' \
                    and info.delete_all_column_name \
                    and not row_values[info.delete_all_column_name]:
                return info.create_identifier_func()
            return info.create_func()
        else:
            return UnknownBulkEntity()

    @staticmethod
    def get_bulk_row_type(bulk_object):
        if isinstance(bulk_object, BulkError):
            return '{0} Error'.format(_BulkObjectFactory.get_bulk_row_type(bulk_object.entity))
        return _BulkObjectFactory.TYPE_REVERSE_MAP[type(bulk_object)]


for (k, v) in _BulkObjectFactory.INDIVIDUAL_ENTITY_MAP.items():
    _BulkObjectFactory.TYPE_REVERSE_MAP[type(v.create_func())] = k

    if v.create_identifier_func is not None:
        identifier = v.create_identifier_func()
        _BulkObjectFactory.TYPE_REVERSE_MAP[type(identifier)] = k
