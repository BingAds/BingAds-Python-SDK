def output_adapierror(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adapierror * * *")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Detail: {0}".format(data_object.Detail))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("Message: {0}".format(data_object.Message))
    output_status_message("* * * End output_adapierror * * *")

def output_array_of_adapierror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdApiError']:
        output_adapierror(data_object)

def output_adapifaultdetail(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adapifaultdetail * * *")
    output_status_message("Errors:")
    output_array_of_adapierror(data_object.Errors)
    output_status_message("* * * End output_adapifaultdetail * * *")

def output_array_of_adapifaultdetail(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdApiFaultDetail']:
        output_adapifaultdetail(data_object)

def output_adgroupbidlandscape(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adgroupbidlandscape * * *")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("AdGroupBidLandscapeType: {0}".format(data_object.AdGroupBidLandscapeType))
    output_status_message("StartDate:")
    output_daymonthandyear(data_object.StartDate)
    output_status_message("EndDate:")
    output_daymonthandyear(data_object.EndDate)
    output_status_message("BidLandscapePoints:")
    output_array_of_bidlandscapepoint(data_object.BidLandscapePoints)
    output_status_message("* * * End output_adgroupbidlandscape * * *")

def output_array_of_adgroupbidlandscape(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdGroupBidLandscape']:
        output_adgroupbidlandscape(data_object)

def output_adgroupbidlandscapeinput(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adgroupbidlandscapeinput * * *")
    output_status_message("AdGroupBidLandscapeType: {0}".format(data_object.AdGroupBidLandscapeType))
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("* * * End output_adgroupbidlandscapeinput * * *")

def output_array_of_adgroupbidlandscapeinput(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdGroupBidLandscapeInput']:
        output_adgroupbidlandscapeinput(data_object)

def output_adgroupestimate(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adgroupestimate * * *")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("KeywordEstimates:")
    output_array_of_keywordestimate(data_object.KeywordEstimates)
    output_status_message("* * * End output_adgroupestimate * * *")

def output_array_of_adgroupestimate(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdGroupEstimate']:
        output_adgroupestimate(data_object)

def output_adgroupestimator(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adgroupestimator * * *")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("KeywordEstimators:")
    output_array_of_keywordestimator(data_object.KeywordEstimators)
    output_status_message("MaxCpc: {0}".format(data_object.MaxCpc))
    output_status_message("* * * End output_adgroupestimator * * *")

def output_array_of_adgroupestimator(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdGroupEstimator']:
        output_adgroupestimator(data_object)

def output_apifaultdetail(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_apifaultdetail * * *")
    output_status_message("BatchErrors:")
    output_array_of_batcherror(data_object.BatchErrors)
    output_status_message("OperationErrors:")
    output_array_of_operationerror(data_object.OperationErrors)
    output_status_message("* * * End output_apifaultdetail * * *")

def output_array_of_apifaultdetail(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ApiFaultDetail']:
        output_apifaultdetail(data_object)

def output_applicationfault(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_applicationfault * * *")
    output_status_message("TrackingId: {0}".format(data_object.TrackingId))
    if data_object.Type == 'AdApiFaultDetail':
        output_adapifaultdetail(data_object)
    if data_object.Type == 'ApiFaultDetail':
        output_apifaultdetail(data_object)
    output_status_message("* * * End output_applicationfault * * *")

def output_array_of_applicationfault(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ApplicationFault']:
        output_applicationfault(data_object)

def output_auctioninsightentry(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_auctioninsightentry * * *")
    output_status_message("DisplayDomain: {0}".format(data_object.DisplayDomain))
    output_status_message("AggregatedKpi:")
    output_auctioninsightkpi(data_object.AggregatedKpi)
    output_status_message("SegmentedKpis:")
    output_array_of_auctioninsightkpi(data_object.SegmentedKpis)
    output_status_message("* * * End output_auctioninsightentry * * *")

def output_array_of_auctioninsightentry(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AuctionInsightEntry']:
        output_auctioninsightentry(data_object)

def output_auctioninsightkpi(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_auctioninsightkpi * * *")
    output_status_message("Segments:")
    output_array_of_string(data_object.Segments)
    output_status_message("ImpressionShare: {0}".format(data_object.ImpressionShare))
    output_status_message("OverlapRate: {0}".format(data_object.OverlapRate))
    output_status_message("AveragePosition: {0}".format(data_object.AveragePosition))
    output_status_message("AboveRate: {0}".format(data_object.AboveRate))
    output_status_message("TopOfPageRate: {0}".format(data_object.TopOfPageRate))
    output_status_message("OutrankingShare: {0}".format(data_object.OutrankingShare))
    output_status_message("AbsoluteTopOfPageRate: {0}".format(data_object.AbsoluteTopOfPageRate))
    output_status_message("* * * End output_auctioninsightkpi * * *")

def output_array_of_auctioninsightkpi(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AuctionInsightKpi']:
        output_auctioninsightkpi(data_object)

def output_auctioninsightresult(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_auctioninsightresult * * *")
    output_status_message("Segments:")
    output_array_of_auctionsegment(data_object.Segments)
    output_status_message("Entries:")
    output_array_of_auctioninsightentry(data_object.Entries)
    output_status_message("UsedImpressions: {0}".format(data_object.UsedImpressions))
    output_status_message("UsedKeywords: {0}".format(data_object.UsedKeywords))
    output_status_message("* * * End output_auctioninsightresult * * *")

def output_array_of_auctioninsightresult(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AuctionInsightResult']:
        output_auctioninsightresult(data_object)

def output_auctionsegmentsearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_auctionsegmentsearchparameter * * *")
    output_status_message("Segment: {0}".format(data_object.Segment))
    output_status_message("* * * End output_auctionsegmentsearchparameter * * *")

def output_array_of_auctionsegmentsearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AuctionSegmentSearchParameter']:
        output_auctionsegmentsearchparameter(data_object)

def output_batcherror(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_batcherror * * *")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Message: {0}".format(data_object.Message))
    output_status_message("* * * End output_batcherror * * *")

def output_array_of_batcherror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BatchError']:
        output_batcherror(data_object)

def output_bidlandscapepoint(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_bidlandscapepoint * * *")
    output_status_message("Bid: {0}".format(data_object.Bid))
    output_status_message("Clicks: {0}".format(data_object.Clicks))
    output_status_message("Impressions: {0}".format(data_object.Impressions))
    output_status_message("TopImpressions: {0}".format(data_object.TopImpressions))
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("Cost: {0}".format(data_object.Cost))
    output_status_message("MarginalCPC: {0}".format(data_object.MarginalCPC))
    output_status_message("* * * End output_bidlandscapepoint * * *")

def output_array_of_bidlandscapepoint(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BidLandscapePoint']:
        output_bidlandscapepoint(data_object)

def output_bidopportunity(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_bidopportunity * * *")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("CurrentBid: {0}".format(data_object.CurrentBid))
    output_status_message("EstimatedIncreaseInClicks: {0}".format(data_object.EstimatedIncreaseInClicks))
    output_status_message("EstimatedIncreaseInCost: {0}".format(data_object.EstimatedIncreaseInCost))
    output_status_message("EstimatedIncreaseInImpressions: {0}".format(data_object.EstimatedIncreaseInImpressions))
    output_status_message("KeywordId: {0}".format(data_object.KeywordId))
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("SuggestedBid: {0}".format(data_object.SuggestedBid))
    output_status_message("* * * End output_bidopportunity * * *")

def output_array_of_bidopportunity(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BidOpportunity']:
        output_bidopportunity(data_object)

def output_broadmatchkeywordopportunity(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_broadmatchkeywordopportunity * * *")
    output_status_message("AverageCPC: {0}".format(data_object.AverageCPC))
    output_status_message("AverageCTR: {0}".format(data_object.AverageCTR))
    output_status_message("ClickShare: {0}".format(data_object.ClickShare))
    output_status_message("ImpressionShare: {0}".format(data_object.ImpressionShare))
    output_status_message("ReferenceKeywordBid: {0}".format(data_object.ReferenceKeywordBid))
    output_status_message("ReferenceKeywordId: {0}".format(data_object.ReferenceKeywordId))
    output_status_message("ReferenceKeywordMatchType: {0}".format(data_object.ReferenceKeywordMatchType))
    output_status_message("SearchQueryKPIs:")
    output_array_of_broadmatchsearchquerykpi(data_object.SearchQueryKPIs)
    output_status_message("* * * End output_broadmatchkeywordopportunity * * *")

def output_array_of_broadmatchkeywordopportunity(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BroadMatchKeywordOpportunity']:
        output_broadmatchkeywordopportunity(data_object)

def output_broadmatchsearchquerykpi(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_broadmatchsearchquerykpi * * *")
    output_status_message("AverageCTR: {0}".format(data_object.AverageCTR))
    output_status_message("Clicks: {0}".format(data_object.Clicks))
    output_status_message("Impressions: {0}".format(data_object.Impressions))
    output_status_message("SRPV: {0}".format(data_object.SRPV))
    output_status_message("SearchQuery: {0}".format(data_object.SearchQuery))
    output_status_message("* * * End output_broadmatchsearchquerykpi * * *")

def output_array_of_broadmatchsearchquerykpi(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BroadMatchSearchQueryKPI']:
        output_broadmatchsearchquerykpi(data_object)

def output_budgetopportunity(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_budgetopportunity * * *")
    output_status_message("BudgetPoints:")
    output_array_of_budgetpoint(data_object.BudgetPoints)
    output_status_message("BudgetType: {0}".format(data_object.BudgetType))
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("CurrentBudget: {0}".format(data_object.CurrentBudget))
    output_status_message("IncreaseInClicks: {0}".format(data_object.IncreaseInClicks))
    output_status_message("IncreaseInImpressions: {0}".format(data_object.IncreaseInImpressions))
    output_status_message("PercentageIncreaseInClicks: {0}".format(data_object.PercentageIncreaseInClicks))
    output_status_message("PercentageIncreaseInImpressions: {0}".format(data_object.PercentageIncreaseInImpressions))
    output_status_message("RecommendedBudget: {0}".format(data_object.RecommendedBudget))
    output_status_message("* * * End output_budgetopportunity * * *")

def output_array_of_budgetopportunity(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BudgetOpportunity']:
        output_budgetopportunity(data_object)

def output_budgetpoint(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_budgetpoint * * *")
    output_status_message("BudgetAmount: {0}".format(data_object.BudgetAmount))
    output_status_message("BudgetPointType: {0}".format(data_object.BudgetPointType))
    output_status_message("EstimatedWeeklyClicks: {0}".format(data_object.EstimatedWeeklyClicks))
    output_status_message("EstimatedWeeklyCost: {0}".format(data_object.EstimatedWeeklyCost))
    output_status_message("EstimatedWeeklyImpressions: {0}".format(data_object.EstimatedWeeklyImpressions))
    output_status_message("* * * End output_budgetpoint * * *")

def output_array_of_budgetpoint(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BudgetPoint']:
        output_budgetpoint(data_object)

def output_campaignestimate(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_campaignestimate * * *")
    output_status_message("AdGroupEstimates:")
    output_array_of_adgroupestimate(data_object.AdGroupEstimates)
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("* * * End output_campaignestimate * * *")

def output_array_of_campaignestimate(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CampaignEstimate']:
        output_campaignestimate(data_object)

def output_campaignestimator(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_campaignestimator * * *")
    output_status_message("AdGroupEstimators:")
    output_array_of_adgroupestimator(data_object.AdGroupEstimators)
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("Criteria:")
    output_array_of_criterion(data_object.Criteria)
    output_status_message("DailyBudget: {0}".format(data_object.DailyBudget))
    output_status_message("NegativeKeywords:")
    output_array_of_negativekeyword(data_object.NegativeKeywords)
    output_status_message("* * * End output_campaignestimator * * *")

def output_array_of_campaignestimator(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CampaignEstimator']:
        output_campaignestimator(data_object)

def output_categorysearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_categorysearchparameter * * *")
    output_status_message("CategoryId: {0}".format(data_object.CategoryId))
    output_status_message("* * * End output_categorysearchparameter * * *")

def output_array_of_categorysearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CategorySearchParameter']:
        output_categorysearchparameter(data_object)

def output_competitionsearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_competitionsearchparameter * * *")
    output_status_message("CompetitionLevels:")
    output_array_of_competitionlevel(data_object.CompetitionLevels)
    output_status_message("* * * End output_competitionsearchparameter * * *")

def output_array_of_competitionsearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CompetitionSearchParameter']:
        output_competitionsearchparameter(data_object)

def output_criterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_criterion * * *")
    if data_object.Type == 'DeviceCriterion':
        output_devicecriterion(data_object)
    if data_object.Type == 'LanguageCriterion':
        output_languagecriterion(data_object)
    if data_object.Type == 'LocationCriterion':
        output_locationcriterion(data_object)
    if data_object.Type == 'NetworkCriterion':
        output_networkcriterion(data_object)
    output_status_message("* * * End output_criterion * * *")

def output_array_of_criterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Criterion']:
        output_criterion(data_object)

def output_daterangesearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_daterangesearchparameter * * *")
    output_status_message("EndDate:")
    output_daymonthandyear(data_object.EndDate)
    output_status_message("StartDate:")
    output_daymonthandyear(data_object.StartDate)
    output_status_message("* * * End output_daterangesearchparameter * * *")

def output_array_of_daterangesearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DateRangeSearchParameter']:
        output_daterangesearchparameter(data_object)

def output_daymonthandyear(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_daymonthandyear * * *")
    output_status_message("Day: {0}".format(data_object.Day))
    output_status_message("Month: {0}".format(data_object.Month))
    output_status_message("Year: {0}".format(data_object.Year))
    output_status_message("* * * End output_daymonthandyear * * *")

def output_array_of_daymonthandyear(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DayMonthAndYear']:
        output_daymonthandyear(data_object)

def output_devicecriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_devicecriterion * * *")
    output_status_message("DeviceName: {0}".format(data_object.DeviceName))
    output_status_message("* * * End output_devicecriterion * * *")

def output_array_of_devicecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DeviceCriterion']:
        output_devicecriterion(data_object)

def output_devicesearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_devicesearchparameter * * *")
    output_status_message("Device:")
    output_devicecriterion(data_object.Device)
    output_status_message("* * * End output_devicesearchparameter * * *")

def output_array_of_devicesearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DeviceSearchParameter']:
        output_devicesearchparameter(data_object)

def output_domaincategory(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_domaincategory * * *")
    output_status_message("Bid: {0}".format(data_object.Bid))
    output_status_message("CategoryName: {0}".format(data_object.CategoryName))
    output_status_message("Coverage: {0}".format(data_object.Coverage))
    output_status_message("* * * End output_domaincategory * * *")

def output_array_of_domaincategory(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DomainCategory']:
        output_domaincategory(data_object)

def output_estimatedbidandtraffic(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_estimatedbidandtraffic * * *")
    output_status_message("MinClicksPerWeek: {0}".format(data_object.MinClicksPerWeek))
    output_status_message("MaxClicksPerWeek: {0}".format(data_object.MaxClicksPerWeek))
    output_status_message("AverageCPC: {0}".format(data_object.AverageCPC))
    output_status_message("MinImpressionsPerWeek: {0}".format(data_object.MinImpressionsPerWeek))
    output_status_message("MaxImpressionsPerWeek: {0}".format(data_object.MaxImpressionsPerWeek))
    output_status_message("CTR: {0}".format(data_object.CTR))
    output_status_message("MinTotalCostPerWeek: {0}".format(data_object.MinTotalCostPerWeek))
    output_status_message("MaxTotalCostPerWeek: {0}".format(data_object.MaxTotalCostPerWeek))
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("EstimatedMinBid: {0}".format(data_object.EstimatedMinBid))
    output_status_message("* * * End output_estimatedbidandtraffic * * *")

def output_array_of_estimatedbidandtraffic(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EstimatedBidAndTraffic']:
        output_estimatedbidandtraffic(data_object)

def output_estimatedpositionandtraffic(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_estimatedpositionandtraffic * * *")
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("MinClicksPerWeek: {0}".format(data_object.MinClicksPerWeek))
    output_status_message("MaxClicksPerWeek: {0}".format(data_object.MaxClicksPerWeek))
    output_status_message("AverageCPC: {0}".format(data_object.AverageCPC))
    output_status_message("MinImpressionsPerWeek: {0}".format(data_object.MinImpressionsPerWeek))
    output_status_message("MaxImpressionsPerWeek: {0}".format(data_object.MaxImpressionsPerWeek))
    output_status_message("CTR: {0}".format(data_object.CTR))
    output_status_message("MinTotalCostPerWeek: {0}".format(data_object.MinTotalCostPerWeek))
    output_status_message("MaxTotalCostPerWeek: {0}".format(data_object.MaxTotalCostPerWeek))
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("EstimatedAdPosition: {0}".format(data_object.EstimatedAdPosition))
    output_status_message("* * * End output_estimatedpositionandtraffic * * *")

def output_array_of_estimatedpositionandtraffic(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EstimatedPositionAndTraffic']:
        output_estimatedpositionandtraffic(data_object)

def output_excludeaccountkeywordssearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_excludeaccountkeywordssearchparameter * * *")
    output_status_message("ExcludeAccountKeywords: {0}".format(data_object.ExcludeAccountKeywords))
    output_status_message("* * * End output_excludeaccountkeywordssearchparameter * * *")

def output_array_of_excludeaccountkeywordssearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ExcludeAccountKeywordsSearchParameter']:
        output_excludeaccountkeywordssearchparameter(data_object)

def output_historicalsearchcountperiodic(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_historicalsearchcountperiodic * * *")
    output_status_message("SearchCount: {0}".format(data_object.SearchCount))
    output_status_message("DayMonthAndYear:")
    output_daymonthandyear(data_object.DayMonthAndYear)
    output_status_message("* * * End output_historicalsearchcountperiodic * * *")

def output_array_of_historicalsearchcountperiodic(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['HistoricalSearchCountPeriodic']:
        output_historicalsearchcountperiodic(data_object)

def output_ideatextsearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_ideatextsearchparameter * * *")
    output_status_message("Excluded:")
    output_array_of_keyword(data_object.Excluded)
    output_status_message("Included:")
    output_array_of_keyword(data_object.Included)
    output_status_message("* * * End output_ideatextsearchparameter * * *")

def output_array_of_ideatextsearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['IdeaTextSearchParameter']:
        output_ideatextsearchparameter(data_object)

def output_impressionsharesearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_impressionsharesearchparameter * * *")
    output_status_message("Maximum: {0}".format(data_object.Maximum))
    output_status_message("Minimum: {0}".format(data_object.Minimum))
    output_status_message("* * * End output_impressionsharesearchparameter * * *")

def output_array_of_impressionsharesearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ImpressionShareSearchParameter']:
        output_impressionsharesearchparameter(data_object)

def output_keyword(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keyword * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("* * * End output_keyword * * *")

def output_array_of_keyword(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Keyword']:
        output_keyword(data_object)

def output_keywordandconfidence(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordandconfidence * * *")
    output_status_message("SuggestedKeyword: {0}".format(data_object.SuggestedKeyword))
    output_status_message("ConfidenceScore: {0}".format(data_object.ConfidenceScore))
    output_status_message("* * * End output_keywordandconfidence * * *")

def output_array_of_keywordandconfidence(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordAndConfidence']:
        output_keywordandconfidence(data_object)

def output_keywordandmatchtype(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordandmatchtype * * *")
    output_status_message("KeywordText: {0}".format(data_object.KeywordText))
    output_status_message("MatchTypes:")
    output_array_of_matchtype(data_object.MatchTypes)
    output_status_message("* * * End output_keywordandmatchtype * * *")

def output_array_of_keywordandmatchtype(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordAndMatchType']:
        output_keywordandmatchtype(data_object)

def output_keywordbidlandscape(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordbidlandscape * * *")
    output_status_message("KeywordId: {0}".format(data_object.KeywordId))
    output_status_message("StartDate:")
    output_daymonthandyear(data_object.StartDate)
    output_status_message("EndDate:")
    output_daymonthandyear(data_object.EndDate)
    output_status_message("BidLandscapePoints:")
    output_array_of_bidlandscapepoint(data_object.BidLandscapePoints)
    output_status_message("* * * End output_keywordbidlandscape * * *")

def output_array_of_keywordbidlandscape(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordBidLandscape']:
        output_keywordbidlandscape(data_object)

def output_keywordcategory(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordcategory * * *")
    output_status_message("Category: {0}".format(data_object.Category))
    output_status_message("ConfidenceScore: {0}".format(data_object.ConfidenceScore))
    output_status_message("* * * End output_keywordcategory * * *")

def output_array_of_keywordcategory(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordCategory']:
        output_keywordcategory(data_object)

def output_keywordcategoryresult(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordcategoryresult * * *")
    output_status_message("Keyword: {0}".format(data_object.Keyword))
    output_status_message("KeywordCategories:")
    output_array_of_keywordcategory(data_object.KeywordCategories)
    output_status_message("* * * End output_keywordcategoryresult * * *")

def output_array_of_keywordcategoryresult(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordCategoryResult']:
        output_keywordcategoryresult(data_object)

def output_keyworddemographic(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keyworddemographic * * *")
    output_status_message("Device: {0}".format(data_object.Device))
    output_status_message("EighteenToTwentyFour: {0}".format(data_object.EighteenToTwentyFour))
    output_status_message("TwentyFiveToThirtyFour: {0}".format(data_object.TwentyFiveToThirtyFour))
    output_status_message("ThirtyFiveToFourtyNine: {0}".format(data_object.ThirtyFiveToFourtyNine))
    output_status_message("FiftyToSixtyFour: {0}".format(data_object.FiftyToSixtyFour))
    output_status_message("SixtyFiveAndAbove: {0}".format(data_object.SixtyFiveAndAbove))
    output_status_message("AgeUnknown: {0}".format(data_object.AgeUnknown))
    output_status_message("Female: {0}".format(data_object.Female))
    output_status_message("Male: {0}".format(data_object.Male))
    output_status_message("GenderUnknown: {0}".format(data_object.GenderUnknown))
    output_status_message("* * * End output_keyworddemographic * * *")

def output_array_of_keyworddemographic(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordDemographic']:
        output_keyworddemographic(data_object)

def output_keyworddemographicresult(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keyworddemographicresult * * *")
    output_status_message("Keyword: {0}".format(data_object.Keyword))
    output_status_message("KeywordDemographics:")
    output_array_of_keyworddemographic(data_object.KeywordDemographics)
    output_status_message("* * * End output_keyworddemographicresult * * *")

def output_array_of_keyworddemographicresult(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordDemographicResult']:
        output_keyworddemographicresult(data_object)

def output_keywordestimate(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordestimate * * *")
    output_status_message("Keyword:")
    output_keyword(data_object.Keyword)
    output_status_message("Maximum:")
    output_trafficestimate(data_object.Maximum)
    output_status_message("Minimum:")
    output_trafficestimate(data_object.Minimum)
    output_status_message("* * * End output_keywordestimate * * *")

def output_array_of_keywordestimate(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordEstimate']:
        output_keywordestimate(data_object)

def output_keywordestimatedbid(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordestimatedbid * * *")
    output_status_message("Keyword: {0}".format(data_object.Keyword))
    output_status_message("EstimatedBids:")
    output_array_of_estimatedbidandtraffic(data_object.EstimatedBids)
    output_status_message("* * * End output_keywordestimatedbid * * *")

def output_array_of_keywordestimatedbid(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordEstimatedBid']:
        output_keywordestimatedbid(data_object)

def output_keywordestimatedposition(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordestimatedposition * * *")
    output_status_message("Keyword: {0}".format(data_object.Keyword))
    output_status_message("EstimatedPositions:")
    output_array_of_estimatedpositionandtraffic(data_object.EstimatedPositions)
    output_status_message("* * * End output_keywordestimatedposition * * *")

def output_array_of_keywordestimatedposition(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordEstimatedPosition']:
        output_keywordestimatedposition(data_object)

def output_keywordestimator(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordestimator * * *")
    output_status_message("Keyword:")
    output_keyword(data_object.Keyword)
    output_status_message("MaxCpc: {0}".format(data_object.MaxCpc))
    output_status_message("* * * End output_keywordestimator * * *")

def output_array_of_keywordestimator(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordEstimator']:
        output_keywordestimator(data_object)

def output_keywordhistoricalperformance(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordhistoricalperformance * * *")
    output_status_message("Keyword: {0}".format(data_object.Keyword))
    output_status_message("KeywordKPIs:")
    output_array_of_keywordkpi(data_object.KeywordKPIs)
    output_status_message("* * * End output_keywordhistoricalperformance * * *")

def output_array_of_keywordhistoricalperformance(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordHistoricalPerformance']:
        output_keywordhistoricalperformance(data_object)

def output_keywordidea(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordidea * * *")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("AdGroupName: {0}".format(data_object.AdGroupName))
    output_status_message("AdImpressionShare: {0}".format(data_object.AdImpressionShare))
    output_status_message("Competition: {0}".format(data_object.Competition))
    output_status_message("Keyword: {0}".format(data_object.Keyword))
    output_status_message("MonthlySearchCounts:")
    output_array_of_long(data_object.MonthlySearchCounts)
    output_status_message("Relevance: {0}".format(data_object.Relevance))
    output_status_message("Source: {0}".format(data_object.Source))
    output_status_message("SuggestedBid: {0}".format(data_object.SuggestedBid))
    output_status_message("* * * End output_keywordidea * * *")

def output_array_of_keywordidea(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordIdea']:
        output_keywordidea(data_object)

def output_keywordideacategory(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordideacategory * * *")
    output_status_message("CategoryId: {0}".format(data_object.CategoryId))
    output_status_message("CategoryName: {0}".format(data_object.CategoryName))
    output_status_message("* * * End output_keywordideacategory * * *")

def output_array_of_keywordideacategory(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordIdeaCategory']:
        output_keywordideacategory(data_object)

def output_keywordidestimatedbid(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordidestimatedbid * * *")
    output_status_message("KeywordId: {0}".format(data_object.KeywordId))
    output_status_message("KeywordEstimatedBid:")
    output_keywordestimatedbid(data_object.KeywordEstimatedBid)
    output_status_message("* * * End output_keywordidestimatedbid * * *")

def output_array_of_keywordidestimatedbid(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordIdEstimatedBid']:
        output_keywordidestimatedbid(data_object)

def output_keywordidestimatedposition(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordidestimatedposition * * *")
    output_status_message("KeywordId: {0}".format(data_object.KeywordId))
    output_status_message("KeywordEstimatedPosition:")
    output_keywordestimatedposition(data_object.KeywordEstimatedPosition)
    output_status_message("* * * End output_keywordidestimatedposition * * *")

def output_array_of_keywordidestimatedposition(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordIdEstimatedPosition']:
        output_keywordidestimatedposition(data_object)

def output_keywordkpi(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordkpi * * *")
    output_status_message("Device: {0}".format(data_object.Device))
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("AdPosition: {0}".format(data_object.AdPosition))
    output_status_message("Clicks: {0}".format(data_object.Clicks))
    output_status_message("Impressions: {0}".format(data_object.Impressions))
    output_status_message("AverageCPC: {0}".format(data_object.AverageCPC))
    output_status_message("CTR: {0}".format(data_object.CTR))
    output_status_message("TotalCost: {0}".format(data_object.TotalCost))
    output_status_message("AverageBid: {0}".format(data_object.AverageBid))
    output_status_message("* * * End output_keywordkpi * * *")

def output_array_of_keywordkpi(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordKPI']:
        output_keywordkpi(data_object)

def output_keywordlocation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordlocation * * *")
    output_status_message("Device: {0}".format(data_object.Device))
    output_status_message("Location: {0}".format(data_object.Location))
    output_status_message("Percentage: {0}".format(data_object.Percentage))
    output_status_message("* * * End output_keywordlocation * * *")

def output_array_of_keywordlocation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordLocation']:
        output_keywordlocation(data_object)

def output_keywordlocationresult(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordlocationresult * * *")
    output_status_message("Keyword: {0}".format(data_object.Keyword))
    output_status_message("KeywordLocations:")
    output_array_of_keywordlocation(data_object.KeywordLocations)
    output_status_message("* * * End output_keywordlocationresult * * *")

def output_array_of_keywordlocationresult(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordLocationResult']:
        output_keywordlocationresult(data_object)

def output_keywordopportunity(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordopportunity * * *")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("AdGroupName: {0}".format(data_object.AdGroupName))
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("CampaignName: {0}".format(data_object.CampaignName))
    output_status_message("Competition: {0}".format(data_object.Competition))
    output_status_message("EstimatedIncreaseInClicks: {0}".format(data_object.EstimatedIncreaseInClicks))
    output_status_message("EstimatedIncreaseInCost: {0}".format(data_object.EstimatedIncreaseInCost))
    output_status_message("EstimatedIncreaseInImpressions: {0}".format(data_object.EstimatedIncreaseInImpressions))
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("MonthlySearches: {0}".format(data_object.MonthlySearches))
    output_status_message("SuggestedBid: {0}".format(data_object.SuggestedBid))
    output_status_message("SuggestedKeyword: {0}".format(data_object.SuggestedKeyword))
    if data_object.Type == 'BroadMatchKeywordOpportunity':
        output_broadmatchkeywordopportunity(data_object)
    output_status_message("* * * End output_keywordopportunity * * *")

def output_array_of_keywordopportunity(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordOpportunity']:
        output_keywordopportunity(data_object)

def output_keywordsearchcount(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordsearchcount * * *")
    output_status_message("Keyword: {0}".format(data_object.Keyword))
    output_status_message("SearchCountsByAttributes:")
    output_array_of_searchcountsbyattributes(data_object.SearchCountsByAttributes)
    output_status_message("* * * End output_keywordsearchcount * * *")

def output_array_of_keywordsearchcount(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordSearchCount']:
        output_keywordsearchcount(data_object)

def output_keywordsuggestion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keywordsuggestion * * *")
    output_status_message("Keyword: {0}".format(data_object.Keyword))
    output_status_message("SuggestionsAndConfidence:")
    output_array_of_keywordandconfidence(data_object.SuggestionsAndConfidence)
    output_status_message("* * * End output_keywordsuggestion * * *")

def output_array_of_keywordsuggestion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeywordSuggestion']:
        output_keywordsuggestion(data_object)

def output_languagecriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_languagecriterion * * *")
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("* * * End output_languagecriterion * * *")

def output_array_of_languagecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['LanguageCriterion']:
        output_languagecriterion(data_object)

def output_languagesearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_languagesearchparameter * * *")
    output_status_message("Languages:")
    output_array_of_languagecriterion(data_object.Languages)
    output_status_message("* * * End output_languagesearchparameter * * *")

def output_array_of_languagesearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['LanguageSearchParameter']:
        output_languagesearchparameter(data_object)

def output_locationcriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_locationcriterion * * *")
    output_status_message("LocationId: {0}".format(data_object.LocationId))
    output_status_message("* * * End output_locationcriterion * * *")

def output_array_of_locationcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['LocationCriterion']:
        output_locationcriterion(data_object)

def output_locationsearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_locationsearchparameter * * *")
    output_status_message("Locations:")
    output_array_of_locationcriterion(data_object.Locations)
    output_status_message("* * * End output_locationsearchparameter * * *")

def output_array_of_locationsearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['LocationSearchParameter']:
        output_locationsearchparameter(data_object)

def output_negativekeyword(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_negativekeyword * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("* * * End output_negativekeyword * * *")

def output_array_of_negativekeyword(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['NegativeKeyword']:
        output_negativekeyword(data_object)

def output_networkcriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_networkcriterion * * *")
    output_status_message("Network: {0}".format(data_object.Network))
    output_status_message("* * * End output_networkcriterion * * *")

def output_array_of_networkcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['NetworkCriterion']:
        output_networkcriterion(data_object)

def output_networksearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_networksearchparameter * * *")
    output_status_message("Network:")
    output_networkcriterion(data_object.Network)
    output_status_message("* * * End output_networksearchparameter * * *")

def output_array_of_networksearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['NetworkSearchParameter']:
        output_networksearchparameter(data_object)

def output_operationerror(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_operationerror * * *")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("Message: {0}".format(data_object.Message))
    output_status_message("* * * End output_operationerror * * *")

def output_array_of_operationerror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['OperationError']:
        output_operationerror(data_object)

def output_opportunity(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_opportunity * * *")
    output_status_message("OpportunityKey: {0}".format(data_object.OpportunityKey))
    if data_object.Type == 'BidOpportunity':
        output_bidopportunity(data_object)
    if data_object.Type == 'BudgetOpportunity':
        output_budgetopportunity(data_object)
    if data_object.Type == 'KeywordOpportunity':
        output_keywordopportunity(data_object)
    output_status_message("* * * End output_opportunity * * *")

def output_array_of_opportunity(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Opportunity']:
        output_opportunity(data_object)

def output_querysearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_querysearchparameter * * *")
    output_status_message("Queries:")
    output_array_of_string(data_object.Queries)
    output_status_message("* * * End output_querysearchparameter * * *")

def output_array_of_querysearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['QuerySearchParameter']:
        output_querysearchparameter(data_object)

def output_searchcountsbyattributes(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_searchcountsbyattributes * * *")
    output_status_message("Device: {0}".format(data_object.Device))
    output_status_message("HistoricalSearchCounts:")
    output_array_of_historicalsearchcountperiodic(data_object.HistoricalSearchCounts)
    output_status_message("* * * End output_searchcountsbyattributes * * *")

def output_array_of_searchcountsbyattributes(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SearchCountsByAttributes']:
        output_searchcountsbyattributes(data_object)

def output_searchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_searchparameter * * *")
    if data_object.Type == 'AuctionSegmentSearchParameter':
        output_auctionsegmentsearchparameter(data_object)
    if data_object.Type == 'CategorySearchParameter':
        output_categorysearchparameter(data_object)
    if data_object.Type == 'CompetitionSearchParameter':
        output_competitionsearchparameter(data_object)
    if data_object.Type == 'DateRangeSearchParameter':
        output_daterangesearchparameter(data_object)
    if data_object.Type == 'DeviceSearchParameter':
        output_devicesearchparameter(data_object)
    if data_object.Type == 'ExcludeAccountKeywordsSearchParameter':
        output_excludeaccountkeywordssearchparameter(data_object)
    if data_object.Type == 'IdeaTextSearchParameter':
        output_ideatextsearchparameter(data_object)
    if data_object.Type == 'ImpressionShareSearchParameter':
        output_impressionsharesearchparameter(data_object)
    if data_object.Type == 'LanguageSearchParameter':
        output_languagesearchparameter(data_object)
    if data_object.Type == 'LocationSearchParameter':
        output_locationsearchparameter(data_object)
    if data_object.Type == 'NetworkSearchParameter':
        output_networksearchparameter(data_object)
    if data_object.Type == 'QuerySearchParameter':
        output_querysearchparameter(data_object)
    if data_object.Type == 'SearchVolumeSearchParameter':
        output_searchvolumesearchparameter(data_object)
    if data_object.Type == 'SuggestedBidSearchParameter':
        output_suggestedbidsearchparameter(data_object)
    if data_object.Type == 'UrlSearchParameter':
        output_urlsearchparameter(data_object)
    output_status_message("* * * End output_searchparameter * * *")

def output_array_of_searchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SearchParameter']:
        output_searchparameter(data_object)

def output_searchvolumesearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_searchvolumesearchparameter * * *")
    output_status_message("Maximum: {0}".format(data_object.Maximum))
    output_status_message("Minimum: {0}".format(data_object.Minimum))
    output_status_message("* * * End output_searchvolumesearchparameter * * *")

def output_array_of_searchvolumesearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SearchVolumeSearchParameter']:
        output_searchvolumesearchparameter(data_object)

def output_suggestedbidsearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_suggestedbidsearchparameter * * *")
    output_status_message("Maximum: {0}".format(data_object.Maximum))
    output_status_message("Minimum: {0}".format(data_object.Minimum))
    output_status_message("* * * End output_suggestedbidsearchparameter * * *")

def output_array_of_suggestedbidsearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SuggestedBidSearchParameter']:
        output_suggestedbidsearchparameter(data_object)

def output_trafficestimate(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_trafficestimate * * *")
    output_status_message("AverageCpc: {0}".format(data_object.AverageCpc))
    output_status_message("AveragePosition: {0}".format(data_object.AveragePosition))
    output_status_message("Clicks: {0}".format(data_object.Clicks))
    output_status_message("Ctr: {0}".format(data_object.Ctr))
    output_status_message("Impressions: {0}".format(data_object.Impressions))
    output_status_message("TotalCost: {0}".format(data_object.TotalCost))
    output_status_message("* * * End output_trafficestimate * * *")

def output_array_of_trafficestimate(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['TrafficEstimate']:
        output_trafficestimate(data_object)

def output_urlsearchparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_urlsearchparameter * * *")
    output_status_message("Url: {0}".format(data_object.Url))
    output_status_message("* * * End output_urlsearchparameter * * *")

def output_array_of_urlsearchparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['UrlSearchParameter']:
        output_urlsearchparameter(data_object)

def output_bidopportunitytype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_bidopportunitytype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BidOpportunityType:\n")
    for value_set in value_sets['BidOpportunityType']:
        output_bidopportunitytype(value_set)

def output_budgetpointtype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_budgetpointtype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BudgetPointType:\n")
    for value_set in value_sets['BudgetPointType']:
        output_budgetpointtype(value_set)

def output_budgetlimittype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_budgetlimittype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BudgetLimitType:\n")
    for value_set in value_sets['BudgetLimitType']:
        output_budgetlimittype(value_set)

def output_keywordopportunitytype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_keywordopportunitytype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of KeywordOpportunityType:\n")
    for value_set in value_sets['KeywordOpportunityType']:
        output_keywordopportunitytype(value_set)

def output_targetadposition(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_targetadposition(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of TargetAdPosition:\n")
    for value_set in value_sets['TargetAdPosition']:
        output_targetadposition(value_set)

def output_currencycode(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_currencycode(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CurrencyCode:\n")
    for value_set in value_sets['CurrencyCode']:
        output_currencycode(value_set)

def output_matchtype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_matchtype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of MatchType:\n")
    for value_set in value_sets['MatchType']:
        output_matchtype(value_set)

def output_adgroupbidlandscapetype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adgroupbidlandscapetype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdGroupBidLandscapeType:\n")
    for value_set in value_sets['AdGroupBidLandscapeType']:
        output_adgroupbidlandscapetype(value_set)

def output_timeinterval(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_timeinterval(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of TimeInterval:\n")
    for value_set in value_sets['TimeInterval']:
        output_timeinterval(value_set)

def output_adposition(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adposition(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdPosition:\n")
    for value_set in value_sets['AdPosition']:
        output_adposition(value_set)

def output_entitytype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_entitytype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of EntityType:\n")
    for value_set in value_sets['EntityType']:
        output_entitytype(value_set)

def output_networktype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_networktype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of NetworkType:\n")
    for value_set in value_sets['NetworkType']:
        output_networktype(value_set)

def output_competitionlevel(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_competitionlevel(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CompetitionLevel:\n")
    for value_set in value_sets['CompetitionLevel']:
        output_competitionlevel(value_set)

def output_auctionsegment(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_auctionsegment(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AuctionSegment:\n")
    for value_set in value_sets['AuctionSegment']:
        output_auctionsegment(value_set)

def output_auctioninsightkpiadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_auctioninsightkpiadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AuctionInsightKpiAdditionalField:\n")
    for value_set in value_sets['AuctionInsightKpiAdditionalField']:
        output_auctioninsightkpiadditionalfield(value_set)

def output_keywordideaattribute(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_keywordideaattribute(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of KeywordIdeaAttribute:\n")
    for value_set in value_sets['KeywordIdeaAttribute']:
        output_keywordideaattribute(value_set)

def output_sourcetype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_sourcetype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of SourceType:\n")
    for value_set in value_sets['SourceType']:
        output_sourcetype(value_set)

def output_array_of_long(items):
    if items is None or items['long'] is None:
        return
    output_status_message("Array Of long:")
    for item in items['long']:
        output_status_message("{0}".format(item))
def output_array_of_string(items):
    if items is None or items['string'] is None:
        return
    output_status_message("Array Of string:")
    for item in items['string']:
        output_status_message("{0}".format(item))
def output_status_message(message):
    print(message)
