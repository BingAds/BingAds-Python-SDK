from .string_table import _StringTable


class _CsvHeaders:
    HEADERS = [
        # Common
        _StringTable.Type,
        _StringTable.Status,
        _StringTable.Id,
        _StringTable.ParentId,
        _StringTable.SubType,
        _StringTable.Campaign,
        _StringTable.AdGroup,
        _StringTable.Website,
        _StringTable.SyncTime,
        _StringTable.ClientId,
        _StringTable.LastModifiedTime,

        # Campaign
        _StringTable.TimeZone,
        _StringTable.Budget,
        _StringTable.BudgetType,
        _StringTable.BudgetName,
        _StringTable.BudgetId,
        _StringTable.KeywordVariantMatchEnabled,

        # AdGroup
        _StringTable.StartDate,
        _StringTable.EndDate,
        _StringTable.NetworkDistribution,
        _StringTable.PricingModel,
        _StringTable.AdRotation,
        _StringTable.SearchNetwork,
        _StringTable.SearchBid,
        _StringTable.ContentNetwork,
        _StringTable.ContentBid,
        _StringTable.Language,

        # Ads
        _StringTable.Title,
        _StringTable.Text,
        _StringTable.DisplayUrl,
        _StringTable.DestinationUrl,
        _StringTable.BusinessName,
        _StringTable.PhoneNumber,
        _StringTable.PromotionalText,
        _StringTable.EditorialStatus,
        _StringTable.EditorialLocation,
        _StringTable.EditorialTerm,
        _StringTable.EditorialReasonCode,
        _StringTable.EditorialAppealStatus,
        _StringTable.DevicePreference,

        # Keywords
        _StringTable.Keyword,
        _StringTable.MatchType,
        _StringTable.Bid,
        _StringTable.Param1,
        _StringTable.Param2,
        _StringTable.Param3,

        # Location Target
        _StringTable.Target,
        _StringTable.PhysicalIntent,
        _StringTable.TargetAll,
        _StringTable.BidAdjustment,
        _StringTable.RadiusTargetId,
        _StringTable.Name,
        _StringTable.OsNames,
        _StringTable.Radius,
        _StringTable.Unit,
        _StringTable.BusinessId,

        # DayTime Target
        _StringTable.FromHour,
        _StringTable.FromMinute,
        _StringTable.ToHour,
        _StringTable.ToMinute,

        # AdExtensions common
        _StringTable.Version,

        # SiteLink Ad Extensions
        _StringTable.SiteLinkExtensionOrder,
        _StringTable.SiteLinkDisplayText,
        _StringTable.SiteLinkDestinationUrl,
        _StringTable.SiteLinkDescription1,
        _StringTable.SiteLinkDescription2,

        # Location Ad Extensions
        _StringTable.GeoCodeStatus,
        _StringTable.IconMediaId,
        _StringTable.ImageMediaId,
        _StringTable.AddressLine1,
        _StringTable.AddressLine2,
        _StringTable.PostalCode,
        _StringTable.City,
        _StringTable.StateOrProvince,
        _StringTable.ProvinceName,
        _StringTable.Latitude,
        _StringTable.Longitude,

        # Call Ad Extensions
        _StringTable.CountryCode,
        _StringTable.IsCallOnly,
        _StringTable.IsCallTrackingEnabled,
        _StringTable.RequireTollFreeTrackingNumber,

        # Structured Snippet Ad Extensions
        _StringTable.StructuredSnippetHeader,
        _StringTable.StructuredSnippetValues,

        # Image Ad Extensions
        _StringTable.AltText,
        _StringTable.MediaIds,
        _StringTable.PublisherCountries,

        # Callout Ad Extension
        _StringTable.CalloutText,

        # Product Target
        _StringTable.BingMerchantCenterId,
        _StringTable.BingMerchantCenterName,
        _StringTable.ProductCondition1,
        _StringTable.ProductValue1,
        _StringTable.ProductCondition2,
        _StringTable.ProductValue2,
        _StringTable.ProductCondition3,
        _StringTable.ProductValue3,
        _StringTable.ProductCondition4,
        _StringTable.ProductValue4,
        _StringTable.ProductCondition5,
        _StringTable.ProductValue5,
        _StringTable.ProductCondition6,
        _StringTable.ProductValue6,
        _StringTable.ProductCondition7,
        _StringTable.ProductValue7,
        _StringTable.ProductCondition8,
        _StringTable.ProductValue8,

        # BI
        _StringTable.Spend,
        _StringTable.Impressions,
        _StringTable.Clicks,
        _StringTable.CTR,
        _StringTable.AvgCPC,
        _StringTable.AvgCPM,
        _StringTable.AvgPosition,
        _StringTable.Conversions,
        _StringTable.CPA,

        _StringTable.QualityScore,
        _StringTable.KeywordRelevance,
        _StringTable.LandingPageRelevance,
        _StringTable.LandingPageUserExperience,

        _StringTable.AppPlatform,
        _StringTable.AppStoreId,
        _StringTable.IsTrackingEnabled,

        _StringTable.Error,
        _StringTable.ErrorNumber,

        # Bing Shopping Campaigns
        _StringTable.IsExcluded,
        _StringTable.ParentAdGroupCriterionId,
        _StringTable.CampaignType,
        _StringTable.CampaignPriority,

        # V10 added
        _StringTable.FieldPath,

        # Upgrade Url
        _StringTable.FinalUrl,
        _StringTable.FinalMobileUrl,
        _StringTable.TrackingTemplate,
        _StringTable.CustomParameter,

        # Review Ad Extension
        _StringTable.IsExact,
        _StringTable.Source,
        _StringTable.Url,

        # Bid Strategy
        _StringTable.BidStrategyType,

        # Ad Format Preference
        _StringTable.AdFormatPreference,

        # Remarketing
        _StringTable.RemarketingList,
        _StringTable.Description,
        _StringTable.MembershipDuration,
        _StringTable.Scope,
        _StringTable.TagId,
        _StringTable.RemarketingListId,
        _StringTable.RemarketingTargetingSetting,
        _StringTable.RemarketingRule,

        # Expanded Text Ad
        _StringTable.TitlePart1,
        _StringTable.TitlePart2,
        _StringTable.Path1,
        _StringTable.Path2,

        # Ad Scheduling
        _StringTable.AdSchedule,
        _StringTable.UseSearcherTimeZone,

        # Dynamic Search Ads
        _StringTable.DomainLanguage,
        _StringTable.DynamicAdTargetCondition1,
        _StringTable.DynamicAdTargetValue1,
        _StringTable.DynamicAdTargetCondition2,
        _StringTable.DynamicAdTargetValue2,
        _StringTable.DynamicAdTargetCondition3,
        _StringTable.DynamicAdTargetValue3,
    ]

    @staticmethod
    def get_mappings():
        return _CsvHeaders.COLUMN_INDEX_MAP

    @staticmethod
    def initialize_map():
        return dict(zip(_CsvHeaders.HEADERS, range(len(_CsvHeaders.HEADERS))))


_CsvHeaders.COLUMN_INDEX_MAP = _CsvHeaders.initialize_map()
