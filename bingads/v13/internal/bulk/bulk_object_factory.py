from bingads.v13.bulk.entities import *
from bingads.v13.bulk.entities.bulk_ad_group_hotel_listing_group import BulkAdGroupHotelListingGroup
from bingads.v13.bulk.entities.bulk_online_conversion_adjustment import BulkOnlineConversionAdjustment
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_hotel_advance_booking_window_criterion import \
    BulkAdGroupHotelAdvanceBookingWindowCriterion
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_hotel_check_in_date_criterion import \
    BulkAdGroupHotelCheckInDateCriterion
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_hotel_check_in_day_criterion import \
    BulkAdGroupHotelCheckInDayCriterion
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_hotel_date_selection_type_criterion import \
    BulkAdGroupHotelDateSelectionTypeCriterion
from bingads.v13.bulk.entities.target_criterions.bulk_ad_group_hotel_length_of_stay_criterion import \
    BulkAdGroupHotelLengthOfStayCriterion
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entity_info import _EntityInfo
from bingads.v13.bulk.entities.bulk_negative_sites import _BulkAdGroupNegativeSitesIdentifier, \
    _BulkCampaignNegativeSitesIdentifier
from bingads.v13.internal.bulk.format_version import _FormatVersion


class _BulkObjectFactory():
    INDIVIDUAL_ENTITY_MAP = {
        _StringTable.Image: _EntityInfo(lambda: BulkImage()),
        _StringTable.Video: _EntityInfo(lambda: BulkVideo()),
        _StringTable.Account: _EntityInfo(lambda: BulkAccount()),
        _StringTable.Budget: _EntityInfo(lambda: BulkBudget()),
        _StringTable.BidStrategy: _EntityInfo(lambda: BulkBidStrategy()),
        _StringTable.Campaign: _EntityInfo(lambda: BulkCampaign()),
        _StringTable.AdGroup: _EntityInfo(lambda: BulkAdGroup()),
        _StringTable.Keyword: _EntityInfo(lambda: BulkKeyword()),
        _StringTable.VideoAdExtension: _EntityInfo(lambda: BulkVideoAdExtension()),
        _StringTable.AccountVideoAdExtension: _EntityInfo(lambda: BulkAccountVideoAdExtension()),
        _StringTable.CampaignVideoAdExtension: _EntityInfo(lambda: BulkCampaignVideoAdExtension()),
        _StringTable.AdGroupVideoAdExtension: _EntityInfo(lambda: BulkAdGroupVideoAdExtension()),
        _StringTable.CallAdExtension: _EntityInfo(lambda: BulkCallAdExtension()),
        _StringTable.CampaignCallAdExtension: _EntityInfo(lambda: BulkCampaignCallAdExtension()),
        _StringTable.FlyerAdExtension: _EntityInfo(lambda: BulkFlyerAdExtension()),
        _StringTable.AccountFlyerAdExtension: _EntityInfo(lambda: BulkAccountFlyerAdExtension()),
        _StringTable.CampaignFlyerAdExtension: _EntityInfo(lambda: BulkCampaignFlyerAdExtension()),
        _StringTable.AdGroupFlyerAdExtension: _EntityInfo(lambda: BulkAdGroupFlyerAdExtension()),
        _StringTable.DisclaimerAdExtension: _EntityInfo(lambda: BulkDisclaimerAdExtension()),
        _StringTable.CampaignDisclaimerAdExtension: _EntityInfo(lambda: BulkCampaignDisclaimerAdExtension()),
        _StringTable.ImageAdExtension: _EntityInfo(lambda: BulkImageAdExtension()),
        _StringTable.AccountImageAdExtension: _EntityInfo(lambda: BulkAccountImageAdExtension()),
        _StringTable.CampaignImageAdExtension: _EntityInfo(lambda: BulkCampaignImageAdExtension()),
        _StringTable.AdGroupImageAdExtension: _EntityInfo(lambda: BulkAdGroupImageAdExtension()),
        _StringTable.FilterLinkAdExtension: _EntityInfo(lambda: BulkFilterLinkAdExtension()),
        _StringTable.AccountFilterLinkAdExtension: _EntityInfo(lambda: BulkAccountFilterLinkAdExtension()),
        _StringTable.CampaignFilterLinkAdExtension: _EntityInfo(lambda: BulkCampaignFilterLinkAdExtension()),
        _StringTable.AdGroupFilterLinkAdExtension: _EntityInfo(lambda: BulkAdGroupFilterLinkAdExtension()),
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
        _StringTable.PromotionAdExtension: _EntityInfo(lambda: BulkPromotionAdExtension()),
        _StringTable.AccountPromotionAdExtension: _EntityInfo(lambda: BulkAccountPromotionAdExtension()),
        _StringTable.CampaignPromotionAdExtension: _EntityInfo(lambda: BulkCampaignPromotionAdExtension()),
        _StringTable.AdGroupPromotionAdExtension: _EntityInfo(lambda: BulkAdGroupPromotionAdExtension()),
        _StringTable.ProductAd: _EntityInfo(lambda: BulkProductAd()),
        _StringTable.TextAd: _EntityInfo(lambda: BulkTextAd()),
        _StringTable.AppInstallAd: _EntityInfo(lambda: BulkAppInstallAd()),
        _StringTable.ExpandedTextAd: _EntityInfo(lambda: BulkExpandedTextAd()),
        _StringTable.DynamicSearchAd: _EntityInfo(lambda: BulkDynamicSearchAd()),
        _StringTable.ResponsiveAd: _EntityInfo(lambda: BulkResponsiveAd()),
        _StringTable.ResponsiveSearchAd: _EntityInfo(lambda: BulkResponsiveSearchAd()),
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
        'Ad Group Hotel Listing Group': _EntityInfo(lambda : BulkAdGroupHotelListingGroup()),
        _StringTable.RemarketingList: _EntityInfo(lambda : BulkRemarketingList()),
        _StringTable.AdGroupRemarketingListAssociation: _EntityInfo(lambda : BulkAdGroupRemarketingListAssociation()),
        _StringTable.AdGroupNegativeRemarketingListAssociation: _EntityInfo(lambda : BulkAdGroupNegativeRemarketingListAssociation()),
        _StringTable.CampaignRemarketingListAssociation: _EntityInfo(lambda : BulkCampaignRemarketingListAssociation()),
        _StringTable.CampaignNegativeRemarketingListAssociation: _EntityInfo(lambda : BulkCampaignNegativeRemarketingListAssociation()),
        _StringTable.CampaignNegativeStoreCriterion: _EntityInfo(lambda : BulkCampaignNegativeStoreCriterion()),
        _StringTable.CustomAudience: _EntityInfo(lambda : BulkCustomAudience()),
        _StringTable.AdGroupCustomAudienceAssociation: _EntityInfo(lambda : BulkAdGroupCustomAudienceAssociation()),
        _StringTable.AdGroupNegativeCustomAudienceAssociation: _EntityInfo(lambda : BulkAdGroupNegativeCustomAudienceAssociation()),
        _StringTable.CampaignCustomAudienceAssociation: _EntityInfo(lambda : BulkCampaignCustomAudienceAssociation()),
        _StringTable.CampaignNegativeCustomAudienceAssociation: _EntityInfo(lambda : BulkCampaignNegativeCustomAudienceAssociation()),
        _StringTable.InMarketAudience: _EntityInfo(lambda : BulkInMarketAudience()),
        _StringTable.AdGroupInMarketAudienceAssociation: _EntityInfo(lambda : BulkAdGroupInMarketAudienceAssociation()),
        _StringTable.AdGroupNegativeInMarketAudienceAssociation: _EntityInfo(lambda : BulkAdGroupNegativeInMarketAudienceAssociation()),
        _StringTable.CampaignInMarketAudienceAssociation: _EntityInfo(lambda : BulkCampaignInMarketAudienceAssociation()),
        _StringTable.CampaignNegativeInMarketAudienceAssociation: _EntityInfo(lambda : BulkCampaignNegativeInMarketAudienceAssociation()),
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

        _StringTable.AdGroupAdvanceBookingWindowCriterion: _EntityInfo(lambda: BulkAdGroupHotelAdvanceBookingWindowCriterion()),
        _StringTable.AdGroupCheckInDateCriterion: _EntityInfo(lambda: BulkAdGroupHotelCheckInDateCriterion()),
        _StringTable.AdGroupCheckInDayCriterion: _EntityInfo(lambda: BulkAdGroupHotelCheckInDayCriterion()),
        _StringTable.AdGroupHotelDateSelectionTypeCriterion: _EntityInfo(lambda: BulkAdGroupHotelDateSelectionTypeCriterion()),
        _StringTable.AdGroupLengthOfStayCriterion: _EntityInfo(lambda: BulkAdGroupHotelLengthOfStayCriterion()),
        _StringTable.CampaignAgeCriterion: _EntityInfo(lambda: BulkCampaignAgeCriterion()),
        _StringTable.CampaignDayTimeCriterion: _EntityInfo(lambda: BulkCampaignDayTimeCriterion()),
        _StringTable.CampaignDeviceOSCriterion: _EntityInfo(lambda: BulkCampaignDeviceCriterion()),
        _StringTable.CampaignGenderCriterion: _EntityInfo(lambda: BulkCampaignGenderCriterion()),
        _StringTable.CampaignLocationCriterion: _EntityInfo(lambda: BulkCampaignLocationCriterion()),
        _StringTable.CampaignLocationIntentCriterion: _EntityInfo(lambda: BulkCampaignLocationIntentCriterion()),
        _StringTable.CampaignNegativeLocationCriterion: _EntityInfo(lambda: BulkCampaignNegativeLocationCriterion()),
        _StringTable.CampaignRadiusCriterion: _EntityInfo(lambda: BulkCampaignRadiusCriterion()),
        _StringTable.CampaignCompanyNameCriterion: _EntityInfo(lambda: BulkCampaignCompanyNameCriterion()),
        _StringTable.CampaignJobFunctionCriterion: _EntityInfo(lambda: BulkCampaignJobFunctionCriterion()),
        _StringTable.CampaignIndustryCriterion: _EntityInfo(lambda: BulkCampaignIndustryCriterion()),
        _StringTable.CampaignDealCriterion: _EntityInfo(lambda: BulkCampaignDealCriterion()),
        _StringTable.CombinedList: _EntityInfo(lambda: BulkCombinedList()),
        _StringTable.CustomerList: _EntityInfo(lambda: BulkCustomerList()),
        _StringTable.CustomerListItem: _EntityInfo(lambda: BulkCustomerListItem()),
        _StringTable.ProductAudience: _EntityInfo(lambda: BulkProductAudience()),
        _StringTable.AdGroupProductAudienceAssociation: _EntityInfo(lambda: BulkAdGroupProductAudienceAssociation()),
        _StringTable.AdGroupNegativeProductAudienceAssociation: _EntityInfo(lambda: BulkAdGroupNegativeProductAudienceAssociation()),
        _StringTable.AdGroupCombinedListAssociation: _EntityInfo(lambda: BulkAdGroupCombinedListAssociation()),
        _StringTable.AdGroupCustomerListAssociation: _EntityInfo(lambda: BulkAdGroupCustomerListAssociation()),
        _StringTable.AdGroupNegativeCombinedListAssociation: _EntityInfo(lambda: BulkAdGroupNegativeCombinedListAssociation()),
        _StringTable.AdGroupNegativeCustomerListAssociation: _EntityInfo(lambda: BulkAdGroupNegativeCustomerListAssociation()),
        _StringTable.CampaignProductAudienceAssociation: _EntityInfo(lambda: BulkCampaignProductAudienceAssociation()),
        _StringTable.CampaignNegativeProductAudienceAssociation: _EntityInfo(lambda: BulkCampaignNegativeProductAudienceAssociation()),
        _StringTable.CampaignCombinedListAssociation: _EntityInfo(lambda: BulkCampaignCombinedListAssociation()),
        _StringTable.CampaignNegativeCombinedListAssociation: _EntityInfo(lambda: BulkCampaignNegativeCombinedListAssociation()),
        _StringTable.CampaignCustomerListAssociation: _EntityInfo(lambda: BulkCampaignCustomerListAssociation()),
        _StringTable.CampaignNegativeCustomerListAssociation: _EntityInfo(lambda: BulkCampaignNegativeCustomerListAssociation()),
        _StringTable.ImpressionBasedRemarketingList: _EntityInfo(lambda: BulkImpressionBasedRemarketingList()),
        _StringTable.CampaignImpressionBasedRemarketingListAssociation: _EntityInfo(lambda: BulkCampaignImpressionBasedRemarketingListAssociation()),
        _StringTable.CampaignNegativeImpressionBasedRemarketingListAssociation: _EntityInfo(lambda: BulkCampaignNegativeImpressionBasedRemarketingListAssociation()),
        _StringTable.AdGroupImpressionBasedRemarketingListAssociation: _EntityInfo(lambda: BulkAdGroupImpressionBasedRemarketingListAssociation()),
        _StringTable.AdGroupNegativeImpressionBasedRemarketingListAssociation: _EntityInfo(lambda: BulkAdGroupNegativeImpressionBasedRemarketingListAssociation()),
        _StringTable.AdGroupIndustryCriterion: _EntityInfo(lambda: BulkAdGroupIndustryCriterion()),
        _StringTable.AdGroupCompanyNameCriterion: _EntityInfo(lambda: BulkAdGroupCompanyNameCriterion()),
        _StringTable.AdGroupJobFunctionCriterion: _EntityInfo(lambda: BulkAdGroupJobFunctionCriterion()),
        _StringTable.AdGroupNegativeAgeCriterion: _EntityInfo(lambda: BulkAdGroupNegativeAgeCriterion()),
        _StringTable.AdGroupNegativeCompanyNameCriterion: _EntityInfo(lambda: BulkAdGroupNegativeCompanyNameCriterion()),
        _StringTable.AdGroupNegativeGenderCriterion: _EntityInfo(lambda: BulkAdGroupNegativeGenderCriterion()),
        _StringTable.AdGroupNegativeIndustryCriterion: _EntityInfo(lambda: BulkAdGroupNegativeIndustryCriterion()),
        _StringTable.AdGroupNegativeJobFunctionCriterion: _EntityInfo(lambda: BulkAdGroupNegativeJobFunctionCriterion()),
        _StringTable.AdGroupGenreCriterion: _EntityInfo(lambda: BulkAdGroupGenreCriterion()),
        _StringTable.Label: _EntityInfo(lambda: BulkLabel()),
        _StringTable.CampaignLabel: _EntityInfo(lambda: BulkCampaignLabel()),
        _StringTable.AdGroupLabel: _EntityInfo(lambda: BulkAdGroupLabel()),
        _StringTable.KeywordLabel: _EntityInfo(lambda: BulkKeywordLabel()),
        _StringTable.AppInstallAdLabel: _EntityInfo(lambda: BulkAppInstallAdLabel()),
        _StringTable.DynamicSearchAdLabel: _EntityInfo(lambda: BulkDynamicSearchAdLabel()),
        _StringTable.ExpandedTextAdLabel: _EntityInfo(lambda: BulkExpandedTextAdLabel()),
        _StringTable.ProductAdLabel: _EntityInfo(lambda: BulkProductAdLabel()),
        _StringTable.ResponsiveAdLabel: _EntityInfo(lambda: BulkResponsiveAdLabel()),
        _StringTable.ResponsiveSearchAdLabel: _EntityInfo(lambda: BulkResponsiveSearchAdLabel()),
        _StringTable.OfflineConversion: _EntityInfo(lambda: BulkOfflineConversion()),
        _StringTable.OnlineConversionAdjustment: _EntityInfo(lambda: BulkOnlineConversionAdjustment()),
        _StringTable.SimilarRemarketingList: _EntityInfo(lambda: BulkSimilarRemarketingList()),
        _StringTable.AdGroupSimilarRemarketingListAssociation: _EntityInfo(lambda: BulkAdGroupSimilarRemarketingListAssociation()),
        _StringTable.AdGroupNegativeSimilarRemarketingListAssociation: _EntityInfo(lambda: BulkAdGroupNegativeSimilarRemarketingListAssociation()),
        _StringTable.CampaignSimilarRemarketingListAssociation: _EntityInfo(lambda: BulkCampaignSimilarRemarketingListAssociation()),
        _StringTable.CampaignNegativeSimilarRemarketingListAssociation: _EntityInfo(lambda: BulkCampaignNegativeSimilarRemarketingListAssociation()),
        _StringTable.ActionAdExtension: _EntityInfo(lambda: BulkActionAdExtension()),
        _StringTable.AccountActionAdExtension: _EntityInfo(lambda: BulkAccountActionAdExtension()),
        _StringTable.AdGroupActionAdExtension: _EntityInfo(lambda: BulkAdGroupActionAdExtension()),
        _StringTable.CampaignActionAdExtension: _EntityInfo(lambda: BulkCampaignActionAdExtension()),
        _StringTable.Experiment: _EntityInfo(lambda: BulkExperiment()),
        _StringTable.Feed: _EntityInfo(lambda: BulkFeed()),
        _StringTable.FeedItem: _EntityInfo(lambda: BulkFeedItem()),
        _StringTable.CampaignConversionGoal: _EntityInfo(lambda: BulkCampaignConversionGoal()),
        _StringTable.AdCustomizerAttribute: _EntityInfo(lambda: BulkAdCustomizerAttribute()),
        _StringTable.AdCustomizerCampaign: _EntityInfo(lambda: BulkCampaignAdCustomizerAttribute()),
        _StringTable.AdCustomizerAdGroup: _EntityInfo(lambda: BulkAdGroupAdCustomizerAttribute()),
        _StringTable.AdCustomizerKeyword: _EntityInfo(lambda: BulkKeywordAdCustomizerAttribute()),
        _StringTable.AssetGroup: _EntityInfo(lambda: BulkAssetGroup()),
        _StringTable.AudienceGroup: _EntityInfo(lambda: BulkAudienceGroup()),
        _StringTable.CampaignNegativeWebpage: _EntityInfo(lambda: BulkCampaignNegativeWebpage()),
        _StringTable.AssetGroupListingGroup: _EntityInfo(lambda: BulkAssetGroupListingGroup()),
        _StringTable.AudienceGroupAssetGroupAssociation: _EntityInfo(lambda: BulkAudienceGroupAssetGroupAssociation()),
        _StringTable.SeasonalityAdjustment: _EntityInfo(lambda: BulkSeasonalityAdjustment()),
        _StringTable.DataExclusion: _EntityInfo(lambda: BulkDataExclusion()),
        'Account Negative Keyword List': _EntityInfo(lambda: BulkAccountNegativeKeywordList()),
        'Account Negative Keyword List Association': _EntityInfo(lambda: BulkAccountNegativeKeywordListAssociation()),
        'Account Shared Negative Keyword': _EntityInfo(lambda: BulkAccountSharedNegativeKeyword()),
        _StringTable.EventGoal: _EntityInfo(lambda: BulkEventGoal()),
        _StringTable.AppInstallGoal: _EntityInfo(lambda: BulkAppInstallGoal()),
        _StringTable.DurationGoal: _EntityInfo(lambda: BulkDurationGoal()),
        _StringTable.OfflineConversionGoal: _EntityInfo(lambda: BulkOfflineConversionGoal()),
        _StringTable.UrlGoal: _EntityInfo(lambda: BulkUrlGoal()),
        _StringTable.InStoreTransactionGoal: _EntityInfo(lambda: BulkInStoreTransactionGoal()),
        _StringTable.PagesViewedPerVisitGoal: _EntityInfo(lambda: BulkPagesViewedPerVisitGoal()),
        _StringTable.InStoreVisitGoal: _EntityInfo(lambda: BulkInStoreVisitGoal()),
        _StringTable.ProductGoal: _EntityInfo(lambda: BulkProductGoal()),
        _StringTable.AssetGroupSearchTheme: _EntityInfo(lambda: BulkAssetGroupSearchTheme()),
        _StringTable.BrandList: _EntityInfo(lambda: BulkBrandList()),
        _StringTable.BrandItem: _EntityInfo(lambda: BulkBrandItem()),
        _StringTable.CampaignBrandList: _EntityInfo(lambda: BulkCampaignBrandListAssociation()),
        _StringTable.AssetGroupUrlTarget: _EntityInfo(lambda: BulkAssetGroupUrlTarget()),
        _StringTable.NewCustomerAcquisitionGoal: _EntityInfo(lambda: BulkNewCustomerAcquisitionGoal()),
        _StringTable.AccountPlacementExclusionList: _EntityInfo(lambda: BulkAccountPlacementExclusionList()),
        _StringTable.AccountPlacementExclusionListItem: _EntityInfo(lambda: BulkSharedNegativeSite()),
        _StringTable.CampaignAccountPlacementListAssociation: _EntityInfo(lambda: BulkAccountPlacementExclusionListAssociation()),
        _StringTable.AccountPlacementInclusionList: _EntityInfo(lambda: BulkAccountPlacementInclusionList()),
        _StringTable.AccountPlacementInclusionListItem: _EntityInfo(lambda: BulkSharedSite()),
        _StringTable.CampaignAccountPlacementInclusionListAssociation: _EntityInfo(lambda: BulkAccountPlacementInclusionListAssociation()),
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
