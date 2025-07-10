from .string_table import _StringTable


class _CsvHeaders:
    HEADERS = [
        # Common
        _StringTable.Type,
        _StringTable.Status,
        _StringTable.Id,
        _StringTable.ParentId,
        _StringTable.CampaignId,
        _StringTable.SubType,
        _StringTable.Campaign,
        _StringTable.AdGroup,
        _StringTable.Website,
        _StringTable.SyncTime,
        _StringTable.ClientId,
        _StringTable.LastModifiedTime,
        _StringTable.MultiMediaAdBidAdjustment,
        _StringTable.UseOptimizedTargeting,
        _StringTable.DynamicDescriptionEnabled,
        _StringTable.Details,


        # Campaign
        _StringTable.TimeZone,
        _StringTable.Budget,
        _StringTable.BudgetType,
        _StringTable.BudgetName,
        _StringTable.BudgetId,
        _StringTable.DestinationChannel,
        _StringTable.IsMultiChannelCampaign,

        # AdGroup
        _StringTable.StartDate,
        _StringTable.EndDate,
        _StringTable.NetworkDistribution,
        _StringTable.AdRotation,
        _StringTable.CpcBid,
        _StringTable.CpvBid,
        _StringTable.CpmBid,
        _StringTable.Language,
        _StringTable.PrivacyStatus,
        _StringTable.AdGroupType,
        _StringTable.HotelAdGroupType,
        _StringTable.CommissionRate,
        _StringTable.PercentCpcBid,
        _StringTable.FinalUrlExpansionOptOut,
        _StringTable.HotelListingGroupType,
        _StringTable.HotelAttribute,
        _StringTable.HotelAttributeValue,

        # OnlineConversionAdjustment
        _StringTable.TransactionId,
        # Ads
        _StringTable.Title,
        _StringTable.Text,
        _StringTable.TextPart2,
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
        _StringTable.TargetAll,
        _StringTable.BidAdjustment,
        _StringTable.CashbackAdjustment,
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

        # Profile Criterion
        _StringTable.Profile,
        _StringTable.ProfileId,

        # AdExtensions common
        _StringTable.Version,

        #Disclaimer Ad Extension
        _StringTable.DisclaimerAdsEnabled,
        _StringTable.DisclaimerName,
        _StringTable.DisclaimerTitle,
        _StringTable.DisclaimerLayout,
        _StringTable.DisclaimerPopupText,
        _StringTable.DisclaimerLineText,

        # SiteLink Ad Extensions
        _StringTable.SiteLinkExtensionOrder,
        _StringTable.SiteLinkDisplayText,
        _StringTable.SiteLinkDestinationUrl,
        _StringTable.SiteLinkDescription1,
        _StringTable.SiteLinkDescription2,

        # Location Ad Extensions
        _StringTable.GeoCodeStatus,
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
        _StringTable.Layouts,
        _StringTable.DisplayText,

        # Filter link ad extension
        _StringTable.AdExtensionHeaderType,
        _StringTable.Texts,

        # Image
        _StringTable.Height,
        _StringTable.Width,

        # Video
        _StringTable.SourceUrl,
        _StringTable.AspectRatio,
        _StringTable.DurationInMillionSeconds,

        # Callout Ad Extension
        _StringTable.CalloutText,

        #Flyer Ad Extension
        _StringTable.FlyerAdExtension,
        _StringTable.AccountFlyerAdExtension,
        _StringTable.CampaignFlyerAdExtension,
        _StringTable.AdGroupFlyerAdExtension,
        _StringTable.FlyerName,
        _StringTable.MediaUrls,

        #Video Ad Extension
        _StringTable.ThumbnailUrl,
        _StringTable.ThumbnailId,
        _StringTable.VideoId,

        # Product Target
        _StringTable.MerchantCenterId,
        _StringTable.MerchantCenterName,
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
        _StringTable.LocalInventoryAdsEnabled,

        # experiment
        _StringTable.TrafficSplitPercent,
        _StringTable.BaseCampaignId,
        _StringTable.ExperimentCampaignId,
        _StringTable.ExperimentId,
        _StringTable.ExperimentType,

        #CoOp
        _StringTable.BidOption,
        _StringTable.BidBoostValue,
        _StringTable.MaximumBid,

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

        # Price Ad Extension
        _StringTable.PriceExtensionType,
        _StringTable.Header1,
        _StringTable.Header2,
        _StringTable.Header3,
        _StringTable.Header4,
        _StringTable.Header5,
        _StringTable.Header6,
        _StringTable.Header7,
        _StringTable.Header8,
        _StringTable.PriceDescription1,
        _StringTable.PriceDescription2,
        _StringTable.PriceDescription3,
        _StringTable.PriceDescription4,
        _StringTable.PriceDescription5,
        _StringTable.PriceDescription6,
        _StringTable.PriceDescription7,
        _StringTable.PriceDescription8,
        _StringTable.FinalUrl1,
        _StringTable.FinalUrl2,
        _StringTable.FinalUrl3,
        _StringTable.FinalUrl4,
        _StringTable.FinalUrl5,
        _StringTable.FinalUrl6,
        _StringTable.FinalUrl7,
        _StringTable.FinalUrl8,
        _StringTable.FinalMobileUrl1,
        _StringTable.FinalMobileUrl2,
        _StringTable.FinalMobileUrl3,
        _StringTable.FinalMobileUrl4,
        _StringTable.FinalMobileUrl5,
        _StringTable.FinalMobileUrl6,
        _StringTable.FinalMobileUrl7,
        _StringTable.FinalMobileUrl8,
        _StringTable.Price1,
        _StringTable.Price2,
        _StringTable.Price3,
        _StringTable.Price4,
        _StringTable.Price5,
        _StringTable.Price6,
        _StringTable.Price7,
        _StringTable.Price8,
        _StringTable.CurrencyCode1,
        _StringTable.CurrencyCode2,
        _StringTable.CurrencyCode3,
        _StringTable.CurrencyCode4,
        _StringTable.CurrencyCode5,
        _StringTable.CurrencyCode6,
        _StringTable.CurrencyCode7,
        _StringTable.CurrencyCode8,
        _StringTable.PriceUnit1,
        _StringTable.PriceUnit2,
        _StringTable.PriceUnit3,
        _StringTable.PriceUnit4,
        _StringTable.PriceUnit5,
        _StringTable.PriceUnit6,
        _StringTable.PriceUnit7,
        _StringTable.PriceUnit8,
        _StringTable.PriceQualifier1,
        _StringTable.PriceQualifier2,
        _StringTable.PriceQualifier3,
        _StringTable.PriceQualifier4,
        _StringTable.PriceQualifier5,
        _StringTable.PriceQualifier6,
        _StringTable.PriceQualifier7,
        _StringTable.PriceQualifier8,

        # Bid Strategy
        _StringTable.BidStrategyId,
        _StringTable.BidStrategyName,
        _StringTable.BidStrategyType,
        _StringTable.BidStrategyMaxCpc,
        _StringTable.BidStrategyTargetCpa,
        _StringTable.BidStrategyTargetRoas,
        _StringTable.InheritedBidStrategyType,
        _StringTable.BidStrategyTargetAdPosition,
        _StringTable.BidStrategyTargetImpressionShare,
        _StringTable.BidStrategyCommissionRate,
        _StringTable.BidStrategyPercentMaxCpc,
        _StringTable.BidStrategyTargetCostPerSale,

        # Ad Format Preference
        _StringTable.AdFormatPreference,

        # Remarketing
        _StringTable.Audience,
        _StringTable.Description,
        _StringTable.MembershipDuration,
        _StringTable.Scope,
        _StringTable.TagId,
        _StringTable.AudienceId,
        _StringTable.TargetSetting,
        _StringTable.RemarketingRule,
        _StringTable.AudienceSearchSize,
        _StringTable.AudienceNetworkSize,
        _StringTable.SupportedCampaignTypes,
        _StringTable.ProductAudienceType,
        _StringTable.SourceId,
        _StringTable.CombinationRule,
        _StringTable.EntityType,
        _StringTable.ImpressionCampaignId,
        _StringTable.ImpressionAdGroupId,


        # Expanded Text Ad
        _StringTable.TitlePart1,
        _StringTable.TitlePart2,
        _StringTable.TitlePart3,
        _StringTable.Path1,
        _StringTable.Path2,
        _StringTable.Domain,

        # Responsive Ad
        _StringTable.CallToAction,
        _StringTable.Headline,
        _StringTable.Images,
        _StringTable.LandscapeImageMediaId,
        _StringTable.LandscapeLogoMediaId,
        _StringTable.LongHeadline,
        _StringTable.LongHeadlines,
        _StringTable.SquareImageMediaId,
        _StringTable.SquareLogoMediaId,
        _StringTable.ImpressionTrackingUrls,
        _StringTable.Headlines,
        _StringTable.Descriptions,
        _StringTable.CallToActionLanguage,
        _StringTable.Videos,

        # Ad Scheduling
        _StringTable.AdSchedule,

        #UseSearcherTimeZone
        _StringTable.UseSearcherTimeZone,
        _StringTable.AdScheduleUseSearcherTimeZone,

        # Action ad extension
        _StringTable.ActionType,
        _StringTable.ActionText,

        # Promotion Ad Extension
        _StringTable.PromotionTarget,
        _StringTable.DiscountModifier,
        _StringTable.PercentOff,
        _StringTable.MoneyAmountOff,
        _StringTable.PromotionCode,
        _StringTable.OrdersOverAmount,
        _StringTable.Occasion,
        _StringTable.PromotionStart,
        _StringTable.PromotionEnd,
        _StringTable.CurrencyCode,

        # Dynamic Search Ads
        _StringTable.DomainLanguage,
        _StringTable.DynamicAdTargetCondition1,
        _StringTable.DynamicAdTargetValue1,
        _StringTable.DynamicAdTargetCondition2,
        _StringTable.DynamicAdTargetValue2,
        _StringTable.DynamicAdTargetCondition3,
        _StringTable.DynamicAdTargetValue3,
        _StringTable.DynamicAdTargetConditionOperator1,
        _StringTable.DynamicAdTargetConditionOperator2,
        _StringTable.DynamicAdTargetConditionOperator3,
        _StringTable.PageFeedIds,
        _StringTable.FeedId,

        # Labels
        _StringTable.ColorCode,
        _StringTable.Label,

        # Offline Conversions
        _StringTable.ConversionCurrencyCode,
        _StringTable.ConversionName,
        _StringTable.ConversionTime,
        _StringTable.ConversionValue,
        _StringTable.MicrosoftClickId,
        _StringTable.AdjustmentValue,
        _StringTable.AdjustmentTime,
        _StringTable.AdjustmentCurrencyCode,
        _StringTable.AdjustmentType,
        _StringTable.ExternalAttributionCredit,
        _StringTable.ExternalAttributionModel,
        _StringTable.HashedEmailAddress,
        _StringTable.HashedPhoneNumber,

        # Account
        _StringTable.MSCLKIDAutoTaggingEnabled,
        _StringTable.IncludeViewThroughConversions,
        _StringTable.ProfileExpansionEnabled,
        _StringTable.AdClickParallelTracking,
        _StringTable.AutoApplyRecommendations,
        _StringTable.AllowImageAutoRetrieve,
        _StringTable.BusinessAttributes,
        _StringTable.FinalUrlSuffix,

        # Feeds
        _StringTable.CustomAttributes,
        _StringTable.FeedName,
        _StringTable.PhysicalIntent,
        _StringTable.TargetAdGroupId,
        _StringTable.TargetCampaignId,
        _StringTable.Schedule,

        # Campaign Conversion Goal
        _StringTable.GoalId,

        # RSA AdCustomizer
        _StringTable.AdCustomizerDataType,
        _StringTable.AdCustomizerAttributeValue,

        # Hotel Ad
        _StringTable.MinTargetValue,
        _StringTable.MaxTargetValue,

        # PMax
        _StringTable.Audiences,
        _StringTable.AssetGroup,
        _StringTable.AudienceGroup,
        _StringTable.AgeRanges,
        _StringTable.GenderTypes,
        _StringTable.ParentListingGroupId,
        _StringTable.AudienceGroupName,
        _StringTable.CampaignNegativeWebpage,
        _StringTable.AssetGroupListingGroup,
        _StringTable.AudienceGroupAssetGroupAssociation,
        _StringTable.AutoGeneratedTextOptOut,
        _StringTable.AutoGeneratedImageOptOut,
        _StringTable.CostPerSaleOptOut,
        _StringTable.SearchTheme,

        # Seasonality Adjustment
        _StringTable.SeasonalityAdjustment,
        _StringTable.DataExclusion,
        _StringTable.DeviceType,
        _StringTable.CampaignAssociations,

        # DNV Serving on MSAN
        _StringTable.ShouldServeOnMSAN,

        # Goal
        _StringTable.AttributionModelType,
        _StringTable.ConversionWindowInMinutes,
        _StringTable.CountType,
        _StringTable.ExcludeFromBidding,
        _StringTable.GoalCategory,
        _StringTable.IsEnhancedConversionsEnabled,
        _StringTable.RevenueType,
        _StringTable.RevenueValue,
        _StringTable.TrackingStatus,
        _StringTable.ViewThroughConversionWindowInMinutes,
        _StringTable.MinimumDurationInSecond,
        _StringTable.ActionExpression,
        _StringTable.ActionOperator,
        _StringTable.CategoryExpression,
        _StringTable.CategoryOperator,
        _StringTable.LabelExpression,
        _StringTable.LabelOperator,
        _StringTable.EventValue,
        _StringTable.EventValueOperator,
        _StringTable.IsExternallyAttributed,
        _StringTable.MinimumPagesViewed,
        _StringTable.UrlExpression,
        _StringTable.UrlOperator,

        # Brand List
        _StringTable.BrandId,
        _StringTable.BrandUrl,
        _StringTable.BrandName,
        _StringTable.StatusDateTime,

        # Asset Group Url Target
        _StringTable.AssetGroupTargetCondition1,
        _StringTable.AssetGroupTargetCondition2,
        _StringTable.AssetGroupTargetCondition3,
        _StringTable.AssetGroupTargetConditionOperator1,
        _StringTable.AssetGroupTargetConditionOperator2,
        _StringTable.AssetGroupTargetConditionOperator3,
        _StringTable.AssetGroupTargetValue1,
        _StringTable.AssetGroupTargetValue2,
        _StringTable.AssetGroupTargetValue3,

        # New Customer Acquisition Goal
        _StringTable.AdditionalConversionValue,
        _StringTable.NewCustomerAcquisitionGoalId,
        _StringTable.NewCustomerAcquisitionBidOnlyMode,

        _StringTable.AccountPlacementListItemUrl,

    ]

    @staticmethod
    def get_mappings():
        return _CsvHeaders.COLUMN_INDEX_MAP

    @staticmethod
    def initialize_map():
        return dict(zip(_CsvHeaders.HEADERS, range(len(_CsvHeaders.HEADERS))))


_CsvHeaders.COLUMN_INDEX_MAP = _CsvHeaders.initialize_map()
