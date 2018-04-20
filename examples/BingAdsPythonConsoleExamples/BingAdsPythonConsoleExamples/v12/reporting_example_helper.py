def output_accountperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AccountPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("DeviceOS: {0}".format(data_object.DeviceOS))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))

def output_array_of_accountperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AccountPerformanceReportFilter:\n")
    for data_object in data_objects['AccountPerformanceReportFilter']:
        output_accountperformancereportfilter(data_object)
        output_status_message("\n")

def output_accountperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AccountPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_accountperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_accountperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_accountperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AccountPerformanceReportRequest:\n")
    for data_object in data_objects['AccountPerformanceReportRequest']:
        output_accountperformancereportrequest(data_object)
        output_status_message("\n")

def output_accountreportscope(data_object):
    if data_object is None:
        return
    output_status_message("AccountReportScope (Data Object):")
    output_status_message("AccountIds (Element Name):")
    output_array_of_long(data_object.AccountIds)

def output_array_of_accountreportscope(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AccountReportScope:\n")
    for data_object in data_objects['AccountReportScope']:
        output_accountreportscope(data_object)
        output_status_message("\n")

def output_accountthroughadgroupreportscope(data_object):
    if data_object is None:
        return
    output_status_message("AccountThroughAdGroupReportScope (Data Object):")
    output_status_message("AccountIds (Element Name):")
    output_array_of_long(data_object.AccountIds)
    output_status_message("AdGroups (Element Name):")
    output_array_of_adgroupreportscope(data_object.AdGroups)
    output_status_message("Campaigns (Element Name):")
    output_array_of_campaignreportscope(data_object.Campaigns)

def output_array_of_accountthroughadgroupreportscope(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AccountThroughAdGroupReportScope:\n")
    for data_object in data_objects['AccountThroughAdGroupReportScope']:
        output_accountthroughadgroupreportscope(data_object)
        output_status_message("\n")

def output_accountthroughcampaignreportscope(data_object):
    if data_object is None:
        return
    output_status_message("AccountThroughCampaignReportScope (Data Object):")
    output_status_message("AccountIds (Element Name):")
    output_array_of_long(data_object.AccountIds)
    output_status_message("Campaigns (Element Name):")
    output_array_of_campaignreportscope(data_object.Campaigns)

def output_array_of_accountthroughcampaignreportscope(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AccountThroughCampaignReportScope:\n")
    for data_object in data_objects['AccountThroughCampaignReportScope']:
        output_accountthroughcampaignreportscope(data_object)
        output_status_message("\n")

def output_adapierror(data_object):
    if data_object is None:
        return
    output_status_message("AdApiError (Data Object):")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Detail: {0}".format(data_object.Detail))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("Message: {0}".format(data_object.Message))

def output_array_of_adapierror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdApiError:\n")
    for data_object in data_objects['AdApiError']:
        output_adapierror(data_object)
        output_status_message("\n")

def output_adapifaultdetail(data_object):
    if data_object is None:
        return
    output_status_message("AdApiFaultDetail (Data Object):")
    output_status_message("Errors (Element Name):")
    output_array_of_adapierror(data_object.Errors)

def output_array_of_adapifaultdetail(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdApiFaultDetail:\n")
    for data_object in data_objects['AdApiFaultDetail']:
        output_adapifaultdetail(data_object)
        output_status_message("\n")

def output_addynamictextperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AdDynamicTextPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("AdType: {0}".format(data_object.AdType))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("KeywordStatus: {0}".format(data_object.KeywordStatus))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_addynamictextperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdDynamicTextPerformanceReportFilter:\n")
    for data_object in data_objects['AdDynamicTextPerformanceReportFilter']:
        output_addynamictextperformancereportfilter(data_object)
        output_status_message("\n")

def output_addynamictextperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AdDynamicTextPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_addynamictextperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_addynamictextperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_addynamictextperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdDynamicTextPerformanceReportRequest:\n")
    for data_object in data_objects['AdDynamicTextPerformanceReportRequest']:
        output_addynamictextperformancereportrequest(data_object)
        output_status_message("\n")

def output_adextensionbyadreportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionByAdReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceOS: {0}".format(data_object.DeviceOS))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))

def output_array_of_adextensionbyadreportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionByAdReportFilter:\n")
    for data_object in data_objects['AdExtensionByAdReportFilter']:
        output_adextensionbyadreportfilter(data_object)
        output_status_message("\n")

def output_adextensionbyadreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionByAdReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_adextensionbyadreportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_adextensionbyadreportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_adextensionbyadreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionByAdReportRequest:\n")
    for data_object in data_objects['AdExtensionByAdReportRequest']:
        output_adextensionbyadreportrequest(data_object)
        output_status_message("\n")

def output_adextensionbykeywordreportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionByKeywordReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceOS: {0}".format(data_object.DeviceOS))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("KeywordStatus: {0}".format(data_object.KeywordStatus))

def output_array_of_adextensionbykeywordreportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionByKeywordReportFilter:\n")
    for data_object in data_objects['AdExtensionByKeywordReportFilter']:
        output_adextensionbykeywordreportfilter(data_object)
        output_status_message("\n")

def output_adextensionbykeywordreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionByKeywordReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_adextensionbykeywordreportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_adextensionbykeywordreportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_adextensionbykeywordreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionByKeywordReportRequest:\n")
    for data_object in data_objects['AdExtensionByKeywordReportRequest']:
        output_adextensionbykeywordreportrequest(data_object)
        output_status_message("\n")

def output_adextensiondetailreportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionDetailReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceOS: {0}".format(data_object.DeviceOS))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))

def output_array_of_adextensiondetailreportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionDetailReportFilter:\n")
    for data_object in data_objects['AdExtensionDetailReportFilter']:
        output_adextensiondetailreportfilter(data_object)
        output_status_message("\n")

def output_adextensiondetailreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionDetailReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_adextensiondetailreportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_adextensiondetailreportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_adextensiondetailreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionDetailReportRequest:\n")
    for data_object in data_objects['AdExtensionDetailReportRequest']:
        output_adextensiondetailreportrequest(data_object)
        output_status_message("\n")

def output_adgroupperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AdGroupPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceOS: {0}".format(data_object.DeviceOS))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)
    output_status_message("Status: {0}".format(data_object.Status))

def output_array_of_adgroupperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdGroupPerformanceReportFilter:\n")
    for data_object in data_objects['AdGroupPerformanceReportFilter']:
        output_adgroupperformancereportfilter(data_object)
        output_status_message("\n")

def output_adgroupperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AdGroupPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_adgroupperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_adgroupperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_adgroupperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdGroupPerformanceReportRequest:\n")
    for data_object in data_objects['AdGroupPerformanceReportRequest']:
        output_adgroupperformancereportrequest(data_object)
        output_status_message("\n")

def output_adgroupreportscope(data_object):
    if data_object is None:
        return
    output_status_message("AdGroupReportScope (Data Object):")
    output_status_message("AccountId: {0}".format(data_object.AccountId))
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))

def output_array_of_adgroupreportscope(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdGroupReportScope:\n")
    for data_object in data_objects['AdGroupReportScope']:
        output_adgroupreportscope(data_object)
        output_status_message("\n")

def output_adperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AdPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("AdType: {0}".format(data_object.AdType))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_adperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdPerformanceReportFilter:\n")
    for data_object in data_objects['AdPerformanceReportFilter']:
        output_adperformancereportfilter(data_object)
        output_status_message("\n")

def output_adperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AdPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_adperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_adperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_adperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdPerformanceReportRequest:\n")
    for data_object in data_objects['AdPerformanceReportRequest']:
        output_adperformancereportrequest(data_object)
        output_status_message("\n")

def output_agegenderaudiencereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AgeGenderAudienceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_agegenderaudiencereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AgeGenderAudienceReportFilter:\n")
    for data_object in data_objects['AgeGenderAudienceReportFilter']:
        output_agegenderaudiencereportfilter(data_object)
        output_status_message("\n")

def output_agegenderaudiencereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AgeGenderAudienceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_agegenderaudiencereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_agegenderaudiencereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_agegenderaudiencereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AgeGenderAudienceReportRequest:\n")
    for data_object in data_objects['AgeGenderAudienceReportRequest']:
        output_agegenderaudiencereportrequest(data_object)
        output_status_message("\n")

def output_agegenderdemographicreportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AgeGenderDemographicReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_agegenderdemographicreportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AgeGenderDemographicReportFilter:\n")
    for data_object in data_objects['AgeGenderDemographicReportFilter']:
        output_agegenderdemographicreportfilter(data_object)
        output_status_message("\n")

def output_agegenderdemographicreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AgeGenderDemographicReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_agegenderdemographicreportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_agegenderdemographicreportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_agegenderdemographicreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AgeGenderDemographicReportRequest:\n")
    for data_object in data_objects['AgeGenderDemographicReportRequest']:
        output_agegenderdemographicreportrequest(data_object)
        output_status_message("\n")

def output_apifaultdetail(data_object):
    if data_object is None:
        return
    output_status_message("ApiFaultDetail (Data Object):")
    output_status_message("BatchErrors (Element Name):")
    output_array_of_batcherror(data_object.BatchErrors)
    output_status_message("OperationErrors (Element Name):")
    output_array_of_operationerror(data_object.OperationErrors)

def output_array_of_apifaultdetail(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ApiFaultDetail:\n")
    for data_object in data_objects['ApiFaultDetail']:
        output_apifaultdetail(data_object)
        output_status_message("\n")

def output_applicationfault(data_object):
    if data_object is None:
        return
    output_status_message("ApplicationFault (Data Object):")
    output_status_message("TrackingId: {0}".format(data_object.TrackingId))
    if data_object.Type == 'AdApiFaultDetail':
        output_adapifaultdetail(data_object)
    if data_object.Type == 'ApiFaultDetail':
        output_apifaultdetail(data_object)

def output_array_of_applicationfault(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ApplicationFault:\n")
    for data_object in data_objects['ApplicationFault']:
        output_applicationfault(data_object)
        output_status_message("\n")

def output_audienceperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("AudiencePerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))

def output_array_of_audienceperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AudiencePerformanceReportFilter:\n")
    for data_object in data_objects['AudiencePerformanceReportFilter']:
        output_audienceperformancereportfilter(data_object)
        output_status_message("\n")

def output_audienceperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("AudiencePerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_audienceperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_audienceperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_audienceperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AudiencePerformanceReportRequest:\n")
    for data_object in data_objects['AudiencePerformanceReportRequest']:
        output_audienceperformancereportrequest(data_object)
        output_status_message("\n")

def output_batcherror(data_object):
    if data_object is None:
        return
    output_status_message("BatchError (Data Object):")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Message: {0}".format(data_object.Message))

def output_array_of_batcherror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BatchError:\n")
    for data_object in data_objects['BatchError']:
        output_batcherror(data_object)
        output_status_message("\n")

def output_budgetsummaryreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("BudgetSummaryReportRequest (Data Object):")
    output_status_message("Columns (Element Name):")
    output_array_of_budgetsummaryreportcolumn(data_object.Columns)
    output_status_message("Scope (Element Name):")
    output_accountthroughcampaignreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_budgetsummaryreporttime(data_object.Time)

def output_array_of_budgetsummaryreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BudgetSummaryReportRequest:\n")
    for data_object in data_objects['BudgetSummaryReportRequest']:
        output_budgetsummaryreportrequest(data_object)
        output_status_message("\n")

def output_budgetsummaryreporttime(data_object):
    if data_object is None:
        return
    output_status_message("BudgetSummaryReportTime (Data Object):")
    output_status_message("CustomDateRangeEnd (Element Name):")
    output_date(data_object.CustomDateRangeEnd)
    output_status_message("CustomDateRangeStart (Element Name):")
    output_date(data_object.CustomDateRangeStart)
    output_status_message("PredefinedTime: {0}".format(data_object.PredefinedTime))
    output_status_message("ReportTimeZone: {0}".format(data_object.ReportTimeZone))

def output_array_of_budgetsummaryreporttime(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BudgetSummaryReportTime:\n")
    for data_object in data_objects['BudgetSummaryReportTime']:
        output_budgetsummaryreporttime(data_object)
        output_status_message("\n")

def output_calldetailreportfilter(data_object):
    if data_object is None:
        return
    output_status_message("CallDetailReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))

def output_array_of_calldetailreportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CallDetailReportFilter:\n")
    for data_object in data_objects['CallDetailReportFilter']:
        output_calldetailreportfilter(data_object)
        output_status_message("\n")

def output_calldetailreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("CallDetailReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_calldetailreportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_calldetailreportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_calldetailreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CallDetailReportRequest:\n")
    for data_object in data_objects['CallDetailReportRequest']:
        output_calldetailreportrequest(data_object)
        output_status_message("\n")

def output_campaignperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("CampaignPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("DeviceOS: {0}".format(data_object.DeviceOS))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("Status: {0}".format(data_object.Status))

def output_array_of_campaignperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CampaignPerformanceReportFilter:\n")
    for data_object in data_objects['CampaignPerformanceReportFilter']:
        output_campaignperformancereportfilter(data_object)
        output_status_message("\n")

def output_campaignperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("CampaignPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_campaignperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_campaignperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughcampaignreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_campaignperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CampaignPerformanceReportRequest:\n")
    for data_object in data_objects['CampaignPerformanceReportRequest']:
        output_campaignperformancereportrequest(data_object)
        output_status_message("\n")

def output_campaignreportscope(data_object):
    if data_object is None:
        return
    output_status_message("CampaignReportScope (Data Object):")
    output_status_message("AccountId: {0}".format(data_object.AccountId))
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))

def output_array_of_campaignreportscope(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CampaignReportScope:\n")
    for data_object in data_objects['CampaignReportScope']:
        output_campaignreportscope(data_object)
        output_status_message("\n")

def output_conversionperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("ConversionPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("KeywordStatus: {0}".format(data_object.KeywordStatus))
    output_status_message("Keywords (Element Name):")
    output_array_of_string(data_object.Keywords)

def output_array_of_conversionperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ConversionPerformanceReportFilter:\n")
    for data_object in data_objects['ConversionPerformanceReportFilter']:
        output_conversionperformancereportfilter(data_object)
        output_status_message("\n")

def output_conversionperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("ConversionPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_conversionperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_conversionperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_conversionperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ConversionPerformanceReportRequest:\n")
    for data_object in data_objects['ConversionPerformanceReportRequest']:
        output_conversionperformancereportrequest(data_object)
        output_status_message("\n")

def output_date(data_object):
    if data_object is None:
        return
    output_status_message("Date (Data Object):")
    output_status_message("Day: {0}".format(data_object.Day))
    output_status_message("Month: {0}".format(data_object.Month))
    output_status_message("Year: {0}".format(data_object.Year))

def output_array_of_date(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Date:\n")
    for data_object in data_objects['Date']:
        output_date(data_object)
        output_status_message("\n")

def output_destinationurlperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("DestinationUrlPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_destinationurlperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DestinationUrlPerformanceReportFilter:\n")
    for data_object in data_objects['DestinationUrlPerformanceReportFilter']:
        output_destinationurlperformancereportfilter(data_object)
        output_status_message("\n")

def output_destinationurlperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("DestinationUrlPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_destinationurlperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_destinationurlperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_destinationurlperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DestinationUrlPerformanceReportRequest:\n")
    for data_object in data_objects['DestinationUrlPerformanceReportRequest']:
        output_destinationurlperformancereportrequest(data_object)
        output_status_message("\n")

def output_dsaautotargetperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("DSAAutoTargetPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("BidStrategyType: {0}".format(data_object.BidStrategyType))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DynamicAdTargetStatus: {0}".format(data_object.DynamicAdTargetStatus))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_dsaautotargetperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DSAAutoTargetPerformanceReportFilter:\n")
    for data_object in data_objects['DSAAutoTargetPerformanceReportFilter']:
        output_dsaautotargetperformancereportfilter(data_object)
        output_status_message("\n")

def output_dsaautotargetperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("DSAAutoTargetPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_dsaautotargetperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_dsaautotargetperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_dsaautotargetperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DSAAutoTargetPerformanceReportRequest:\n")
    for data_object in data_objects['DSAAutoTargetPerformanceReportRequest']:
        output_dsaautotargetperformancereportrequest(data_object)
        output_status_message("\n")

def output_dsacategoryperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("DSACategoryPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_dsacategoryperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DSACategoryPerformanceReportFilter:\n")
    for data_object in data_objects['DSACategoryPerformanceReportFilter']:
        output_dsacategoryperformancereportfilter(data_object)
        output_status_message("\n")

def output_dsacategoryperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("DSACategoryPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_dsacategoryperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_dsacategoryperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_dsacategoryperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DSACategoryPerformanceReportRequest:\n")
    for data_object in data_objects['DSACategoryPerformanceReportRequest']:
        output_dsacategoryperformancereportrequest(data_object)
        output_status_message("\n")

def output_dsasearchqueryperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("DSASearchQueryPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("ExcludeZeroClicks: {0}".format(data_object.ExcludeZeroClicks))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)
    output_status_message("SearchQueries (Element Name):")
    output_array_of_string(data_object.SearchQueries)

def output_array_of_dsasearchqueryperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DSASearchQueryPerformanceReportFilter:\n")
    for data_object in data_objects['DSASearchQueryPerformanceReportFilter']:
        output_dsasearchqueryperformancereportfilter(data_object)
        output_status_message("\n")

def output_dsasearchqueryperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("DSASearchQueryPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_dsasearchqueryperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_dsasearchqueryperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_dsasearchqueryperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DSASearchQueryPerformanceReportRequest:\n")
    for data_object in data_objects['DSASearchQueryPerformanceReportRequest']:
        output_dsasearchqueryperformancereportrequest(data_object)
        output_status_message("\n")

def output_geographicperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("GeographicPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("CountryCode (Element Name):")
    output_array_of_string(data_object.CountryCode)
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_geographicperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of GeographicPerformanceReportFilter:\n")
    for data_object in data_objects['GeographicPerformanceReportFilter']:
        output_geographicperformancereportfilter(data_object)
        output_status_message("\n")

def output_geographicperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("GeographicPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_geographicperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_geographicperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_geographicperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of GeographicPerformanceReportRequest:\n")
    for data_object in data_objects['GeographicPerformanceReportRequest']:
        output_geographicperformancereportrequest(data_object)
        output_status_message("\n")

def output_goalsandfunnelsreportfilter(data_object):
    if data_object is None:
        return
    output_status_message("GoalsAndFunnelsReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceOS: {0}".format(data_object.DeviceOS))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("GoalIds (Element Name):")
    output_array_of_long(data_object.GoalIds)
    output_status_message("KeywordStatus: {0}".format(data_object.KeywordStatus))

def output_array_of_goalsandfunnelsreportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of GoalsAndFunnelsReportFilter:\n")
    for data_object in data_objects['GoalsAndFunnelsReportFilter']:
        output_goalsandfunnelsreportfilter(data_object)
        output_status_message("\n")

def output_goalsandfunnelsreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("GoalsAndFunnelsReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_goalsandfunnelsreportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_goalsandfunnelsreportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_goalsandfunnelsreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of GoalsAndFunnelsReportRequest:\n")
    for data_object in data_objects['GoalsAndFunnelsReportRequest']:
        output_goalsandfunnelsreportrequest(data_object)
        output_status_message("\n")

def output_keywordperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("KeywordPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdRelevance (Element Name):")
    output_array_of_int(data_object.AdRelevance)
    output_status_message("AdType: {0}".format(data_object.AdType))
    output_status_message("BidMatchType: {0}".format(data_object.BidMatchType))
    output_status_message("BidStrategyType: {0}".format(data_object.BidStrategyType))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeliveredMatchType: {0}".format(data_object.DeliveredMatchType))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("ExpectedCtr (Element Name):")
    output_array_of_int(data_object.ExpectedCtr)
    output_status_message("KeywordStatus: {0}".format(data_object.KeywordStatus))
    output_status_message("Keywords (Element Name):")
    output_array_of_string(data_object.Keywords)
    output_status_message("LandingPageExperience (Element Name):")
    output_array_of_int(data_object.LandingPageExperience)
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)
    output_status_message("QualityScore (Element Name):")
    output_array_of_int(data_object.QualityScore)

def output_array_of_keywordperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of KeywordPerformanceReportFilter:\n")
    for data_object in data_objects['KeywordPerformanceReportFilter']:
        output_keywordperformancereportfilter(data_object)
        output_status_message("\n")

def output_keywordperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("KeywordPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_keywordperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_keywordperformancereportfilter(data_object.Filter)
    output_status_message("MaxRows: {0}".format(data_object.MaxRows))
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Sort (Element Name):")
    output_array_of_keywordperformancereportsort(data_object.Sort)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_keywordperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of KeywordPerformanceReportRequest:\n")
    for data_object in data_objects['KeywordPerformanceReportRequest']:
        output_keywordperformancereportrequest(data_object)
        output_status_message("\n")

def output_keywordperformancereportsort(data_object):
    if data_object is None:
        return
    output_status_message("KeywordPerformanceReportSort (Data Object):")
    output_status_message("SortColumn: {0}".format(data_object.SortColumn))
    output_status_message("SortOrder: {0}".format(data_object.SortOrder))

def output_array_of_keywordperformancereportsort(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of KeywordPerformanceReportSort:\n")
    for data_object in data_objects['KeywordPerformanceReportSort']:
        output_keywordperformancereportsort(data_object)
        output_status_message("\n")

def output_negativekeywordconflictreportfilter(data_object):
    if data_object is None:
        return
    output_status_message("NegativeKeywordConflictReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("KeywordStatus: {0}".format(data_object.KeywordStatus))

def output_array_of_negativekeywordconflictreportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of NegativeKeywordConflictReportFilter:\n")
    for data_object in data_objects['NegativeKeywordConflictReportFilter']:
        output_negativekeywordconflictreportfilter(data_object)
        output_status_message("\n")

def output_negativekeywordconflictreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("NegativeKeywordConflictReportRequest (Data Object):")
    output_status_message("Columns (Element Name):")
    output_array_of_negativekeywordconflictreportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_negativekeywordconflictreportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)

def output_array_of_negativekeywordconflictreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of NegativeKeywordConflictReportRequest:\n")
    for data_object in data_objects['NegativeKeywordConflictReportRequest']:
        output_negativekeywordconflictreportrequest(data_object)
        output_status_message("\n")

def output_operationerror(data_object):
    if data_object is None:
        return
    output_status_message("OperationError (Data Object):")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("Message: {0}".format(data_object.Message))

def output_array_of_operationerror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of OperationError:\n")
    for data_object in data_objects['OperationError']:
        output_operationerror(data_object)
        output_status_message("\n")

def output_productdimensionperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("ProductDimensionPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_productdimensionperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductDimensionPerformanceReportFilter:\n")
    for data_object in data_objects['ProductDimensionPerformanceReportFilter']:
        output_productdimensionperformancereportfilter(data_object)
        output_status_message("\n")

def output_productdimensionperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("ProductDimensionPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_productdimensionperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_productdimensionperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_productdimensionperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductDimensionPerformanceReportRequest:\n")
    for data_object in data_objects['ProductDimensionPerformanceReportRequest']:
        output_productdimensionperformancereportrequest(data_object)
        output_status_message("\n")

def output_productmatchcountreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("ProductMatchCountReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_productmatchcountreportcolumn(data_object.Columns)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_productmatchcountreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductMatchCountReportRequest:\n")
    for data_object in data_objects['ProductMatchCountReportRequest']:
        output_productmatchcountreportrequest(data_object)
        output_status_message("\n")

def output_productpartitionperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("ProductPartitionPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_productpartitionperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductPartitionPerformanceReportFilter:\n")
    for data_object in data_objects['ProductPartitionPerformanceReportFilter']:
        output_productpartitionperformancereportfilter(data_object)
        output_status_message("\n")

def output_productpartitionperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("ProductPartitionPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_productpartitionperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_productpartitionperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_productpartitionperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductPartitionPerformanceReportRequest:\n")
    for data_object in data_objects['ProductPartitionPerformanceReportRequest']:
        output_productpartitionperformancereportrequest(data_object)
        output_status_message("\n")

def output_productpartitionunitperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("ProductPartitionUnitPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_productpartitionunitperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductPartitionUnitPerformanceReportFilter:\n")
    for data_object in data_objects['ProductPartitionUnitPerformanceReportFilter']:
        output_productpartitionunitperformancereportfilter(data_object)
        output_status_message("\n")

def output_productpartitionunitperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("ProductPartitionUnitPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_productpartitionunitperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_productpartitionunitperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_productpartitionunitperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductPartitionUnitPerformanceReportRequest:\n")
    for data_object in data_objects['ProductPartitionUnitPerformanceReportRequest']:
        output_productpartitionunitperformancereportrequest(data_object)
        output_status_message("\n")

def output_productsearchqueryperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("ProductSearchQueryPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("AdType: {0}".format(data_object.AdType))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("ExcludeZeroClicks: {0}".format(data_object.ExcludeZeroClicks))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)
    output_status_message("SearchQueries (Element Name):")
    output_array_of_string(data_object.SearchQueries)

def output_array_of_productsearchqueryperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductSearchQueryPerformanceReportFilter:\n")
    for data_object in data_objects['ProductSearchQueryPerformanceReportFilter']:
        output_productsearchqueryperformancereportfilter(data_object)
        output_status_message("\n")

def output_productsearchqueryperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("ProductSearchQueryPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_productsearchqueryperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_productsearchqueryperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_productsearchqueryperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductSearchQueryPerformanceReportRequest:\n")
    for data_object in data_objects['ProductSearchQueryPerformanceReportRequest']:
        output_productsearchqueryperformancereportrequest(data_object)
        output_status_message("\n")

def output_professionaldemographicsaudiencereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("ProfessionalDemographicsAudienceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_professionaldemographicsaudiencereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProfessionalDemographicsAudienceReportFilter:\n")
    for data_object in data_objects['ProfessionalDemographicsAudienceReportFilter']:
        output_professionaldemographicsaudiencereportfilter(data_object)
        output_status_message("\n")

def output_professionaldemographicsaudiencereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("ProfessionalDemographicsAudienceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_professionaldemographicsaudiencereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_professionaldemographicsaudiencereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_professionaldemographicsaudiencereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProfessionalDemographicsAudienceReportRequest:\n")
    for data_object in data_objects['ProfessionalDemographicsAudienceReportRequest']:
        output_professionaldemographicsaudiencereportrequest(data_object)
        output_status_message("\n")

def output_publisherusageperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("PublisherUsagePerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_publisherusageperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of PublisherUsagePerformanceReportFilter:\n")
    for data_object in data_objects['PublisherUsagePerformanceReportFilter']:
        output_publisherusageperformancereportfilter(data_object)
        output_status_message("\n")

def output_publisherusageperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("PublisherUsagePerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_publisherusageperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_publisherusageperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_publisherusageperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of PublisherUsagePerformanceReportRequest:\n")
    for data_object in data_objects['PublisherUsagePerformanceReportRequest']:
        output_publisherusageperformancereportrequest(data_object)
        output_status_message("\n")

def output_reportrequest(data_object):
    if data_object is None:
        return
    output_status_message("ReportRequest (Data Object):")
    output_status_message("ExcludeColumnHeaders: {0}".format(data_object.ExcludeColumnHeaders))
    output_status_message("ExcludeReportFooter: {0}".format(data_object.ExcludeReportFooter))
    output_status_message("ExcludeReportHeader: {0}".format(data_object.ExcludeReportHeader))
    output_status_message("Format: {0}".format(data_object.Format))
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("ReportName: {0}".format(data_object.ReportName))
    output_status_message("ReturnOnlyCompleteData: {0}".format(data_object.ReturnOnlyCompleteData))
    if data_object.Type == 'AccountPerformanceReportRequest':
        output_accountperformancereportrequest(data_object)
    if data_object.Type == 'AdDynamicTextPerformanceReportRequest':
        output_addynamictextperformancereportrequest(data_object)
    if data_object.Type == 'AdExtensionByAdReportRequest':
        output_adextensionbyadreportrequest(data_object)
    if data_object.Type == 'AdExtensionByKeywordReportRequest':
        output_adextensionbykeywordreportrequest(data_object)
    if data_object.Type == 'AdExtensionDetailReportRequest':
        output_adextensiondetailreportrequest(data_object)
    if data_object.Type == 'AdGroupPerformanceReportRequest':
        output_adgroupperformancereportrequest(data_object)
    if data_object.Type == 'AdPerformanceReportRequest':
        output_adperformancereportrequest(data_object)
    if data_object.Type == 'AgeGenderAudienceReportRequest':
        output_agegenderaudiencereportrequest(data_object)
    if data_object.Type == 'AgeGenderDemographicReportRequest':
        output_agegenderdemographicreportrequest(data_object)
    if data_object.Type == 'AudiencePerformanceReportRequest':
        output_audienceperformancereportrequest(data_object)
    if data_object.Type == 'BudgetSummaryReportRequest':
        output_budgetsummaryreportrequest(data_object)
    if data_object.Type == 'CallDetailReportRequest':
        output_calldetailreportrequest(data_object)
    if data_object.Type == 'CampaignPerformanceReportRequest':
        output_campaignperformancereportrequest(data_object)
    if data_object.Type == 'ConversionPerformanceReportRequest':
        output_conversionperformancereportrequest(data_object)
    if data_object.Type == 'DestinationUrlPerformanceReportRequest':
        output_destinationurlperformancereportrequest(data_object)
    if data_object.Type == 'DSAAutoTargetPerformanceReportRequest':
        output_dsaautotargetperformancereportrequest(data_object)
    if data_object.Type == 'DSACategoryPerformanceReportRequest':
        output_dsacategoryperformancereportrequest(data_object)
    if data_object.Type == 'DSASearchQueryPerformanceReportRequest':
        output_dsasearchqueryperformancereportrequest(data_object)
    if data_object.Type == 'GeographicPerformanceReportRequest':
        output_geographicperformancereportrequest(data_object)
    if data_object.Type == 'GoalsAndFunnelsReportRequest':
        output_goalsandfunnelsreportrequest(data_object)
    if data_object.Type == 'KeywordPerformanceReportRequest':
        output_keywordperformancereportrequest(data_object)
    if data_object.Type == 'NegativeKeywordConflictReportRequest':
        output_negativekeywordconflictreportrequest(data_object)
    if data_object.Type == 'ProductDimensionPerformanceReportRequest':
        output_productdimensionperformancereportrequest(data_object)
    if data_object.Type == 'ProductMatchCountReportRequest':
        output_productmatchcountreportrequest(data_object)
    if data_object.Type == 'ProductPartitionPerformanceReportRequest':
        output_productpartitionperformancereportrequest(data_object)
    if data_object.Type == 'ProductPartitionUnitPerformanceReportRequest':
        output_productpartitionunitperformancereportrequest(data_object)
    if data_object.Type == 'ProductSearchQueryPerformanceReportRequest':
        output_productsearchqueryperformancereportrequest(data_object)
    if data_object.Type == 'ProfessionalDemographicsAudienceReportRequest':
        output_professionaldemographicsaudiencereportrequest(data_object)
    if data_object.Type == 'PublisherUsagePerformanceReportRequest':
        output_publisherusageperformancereportrequest(data_object)
    if data_object.Type == 'SearchCampaignChangeHistoryReportRequest':
        output_searchcampaignchangehistoryreportrequest(data_object)
    if data_object.Type == 'SearchQueryPerformanceReportRequest':
        output_searchqueryperformancereportrequest(data_object)
    if data_object.Type == 'ShareOfVoiceReportRequest':
        output_shareofvoicereportrequest(data_object)
    if data_object.Type == 'UserLocationPerformanceReportRequest':
        output_userlocationperformancereportrequest(data_object)

def output_array_of_reportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ReportRequest:\n")
    for data_object in data_objects['ReportRequest']:
        output_reportrequest(data_object)
        output_status_message("\n")

def output_reportrequeststatus(data_object):
    if data_object is None:
        return
    output_status_message("ReportRequestStatus (Data Object):")
    output_status_message("ReportDownloadUrl: {0}".format(data_object.ReportDownloadUrl))
    output_status_message("Status: {0}".format(data_object.Status))

def output_array_of_reportrequeststatus(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ReportRequestStatus:\n")
    for data_object in data_objects['ReportRequestStatus']:
        output_reportrequeststatus(data_object)
        output_status_message("\n")

def output_reporttime(data_object):
    if data_object is None:
        return
    output_status_message("ReportTime (Data Object):")
    output_status_message("CustomDateRangeEnd (Element Name):")
    output_date(data_object.CustomDateRangeEnd)
    output_status_message("CustomDateRangeStart (Element Name):")
    output_date(data_object.CustomDateRangeStart)
    output_status_message("PredefinedTime: {0}".format(data_object.PredefinedTime))
    output_status_message("ReportTimeZone: {0}".format(data_object.ReportTimeZone))

def output_array_of_reporttime(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ReportTime:\n")
    for data_object in data_objects['ReportTime']:
        output_reporttime(data_object)
        output_status_message("\n")

def output_searchcampaignchangehistoryreportfilter(data_object):
    if data_object is None:
        return
    output_status_message("SearchCampaignChangeHistoryReportFilter (Data Object):")
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("HowChanged: {0}".format(data_object.HowChanged))
    output_status_message("ItemChanged: {0}".format(data_object.ItemChanged))

def output_array_of_searchcampaignchangehistoryreportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SearchCampaignChangeHistoryReportFilter:\n")
    for data_object in data_objects['SearchCampaignChangeHistoryReportFilter']:
        output_searchcampaignchangehistoryreportfilter(data_object)
        output_status_message("\n")

def output_searchcampaignchangehistoryreportrequest(data_object):
    if data_object is None:
        return
    output_status_message("SearchCampaignChangeHistoryReportRequest (Data Object):")
    output_status_message("Columns (Element Name):")
    output_array_of_searchcampaignchangehistoryreportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_searchcampaignchangehistoryreportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_searchcampaignchangehistoryreportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SearchCampaignChangeHistoryReportRequest:\n")
    for data_object in data_objects['SearchCampaignChangeHistoryReportRequest']:
        output_searchcampaignchangehistoryreportrequest(data_object)
        output_status_message("\n")

def output_searchqueryperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("SearchQueryPerformanceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("AdStatus: {0}".format(data_object.AdStatus))
    output_status_message("AdType: {0}".format(data_object.AdType))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeliveredMatchType: {0}".format(data_object.DeliveredMatchType))
    output_status_message("ExcludeZeroClicks: {0}".format(data_object.ExcludeZeroClicks))
    output_status_message("KeywordStatus: {0}".format(data_object.KeywordStatus))
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)
    output_status_message("SearchQueries (Element Name):")
    output_array_of_string(data_object.SearchQueries)

def output_array_of_searchqueryperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SearchQueryPerformanceReportFilter:\n")
    for data_object in data_objects['SearchQueryPerformanceReportFilter']:
        output_searchqueryperformancereportfilter(data_object)
        output_status_message("\n")

def output_searchqueryperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("SearchQueryPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_searchqueryperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_searchqueryperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_searchqueryperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SearchQueryPerformanceReportRequest:\n")
    for data_object in data_objects['SearchQueryPerformanceReportRequest']:
        output_searchqueryperformancereportrequest(data_object)
        output_status_message("\n")

def output_shareofvoicereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("ShareOfVoiceReportFilter (Data Object):")
    output_status_message("AccountStatus: {0}".format(data_object.AccountStatus))
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdGroupStatus: {0}".format(data_object.AdGroupStatus))
    output_status_message("BidMatchType: {0}".format(data_object.BidMatchType))
    output_status_message("BidStrategyType: {0}".format(data_object.BidStrategyType))
    output_status_message("CampaignStatus: {0}".format(data_object.CampaignStatus))
    output_status_message("DeliveredMatchType: {0}".format(data_object.DeliveredMatchType))
    output_status_message("DeviceType: {0}".format(data_object.DeviceType))
    output_status_message("KeywordStatus: {0}".format(data_object.KeywordStatus))
    output_status_message("Keywords (Element Name):")
    output_array_of_string(data_object.Keywords)
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_shareofvoicereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ShareOfVoiceReportFilter:\n")
    for data_object in data_objects['ShareOfVoiceReportFilter']:
        output_shareofvoicereportfilter(data_object)
        output_status_message("\n")

def output_shareofvoicereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("ShareOfVoiceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_shareofvoicereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_shareofvoicereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_shareofvoicereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ShareOfVoiceReportRequest:\n")
    for data_object in data_objects['ShareOfVoiceReportRequest']:
        output_shareofvoicereportrequest(data_object)
        output_status_message("\n")

def output_userlocationperformancereportfilter(data_object):
    if data_object is None:
        return
    output_status_message("UserLocationPerformanceReportFilter (Data Object):")
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("CountryCode (Element Name):")
    output_array_of_string(data_object.CountryCode)
    output_status_message("LanguageCode (Element Name):")
    output_array_of_string(data_object.LanguageCode)

def output_array_of_userlocationperformancereportfilter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of UserLocationPerformanceReportFilter:\n")
    for data_object in data_objects['UserLocationPerformanceReportFilter']:
        output_userlocationperformancereportfilter(data_object)
        output_status_message("\n")

def output_userlocationperformancereportrequest(data_object):
    if data_object is None:
        return
    output_status_message("UserLocationPerformanceReportRequest (Data Object):")
    output_status_message("Aggregation: {0}".format(data_object.Aggregation))
    output_status_message("Columns (Element Name):")
    output_array_of_userlocationperformancereportcolumn(data_object.Columns)
    output_status_message("Filter (Element Name):")
    output_userlocationperformancereportfilter(data_object.Filter)
    output_status_message("Scope (Element Name):")
    output_accountthroughadgroupreportscope(data_object.Scope)
    output_status_message("Time (Element Name):")
    output_reporttime(data_object.Time)

def output_array_of_userlocationperformancereportrequest(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of UserLocationPerformanceReportRequest:\n")
    for data_object in data_objects['UserLocationPerformanceReportRequest']:
        output_userlocationperformancereportrequest(data_object)
        output_status_message("\n")

def output_reportformat(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_reportformat(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ReportFormat:\n")
    for value_set in value_sets['ReportFormat']:
        output_reportformat(value_set)

def output_reportlanguage(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_reportlanguage(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ReportLanguage:\n")
    for value_set in value_sets['ReportLanguage']:
        output_reportlanguage(value_set)

def output_reportaggregation(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_reportaggregation(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ReportAggregation:\n")
    for value_set in value_sets['ReportAggregation']:
        output_reportaggregation(value_set)

def output_accountperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_accountperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AccountPerformanceReportColumn:\n")
    for value_set in value_sets['AccountPerformanceReportColumn']:
        output_accountperformancereportcolumn(value_set)

def output_accountstatusreportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_accountstatusreportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AccountStatusReportFilter:\n")
    for value_set in value_sets['AccountStatusReportFilter']:
        output_accountstatusreportfilter(value_set)

def output_addistributionreportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_addistributionreportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdDistributionReportFilter:\n")
    for value_set in value_sets['AdDistributionReportFilter']:
        output_addistributionreportfilter(value_set)

def output_deviceosreportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_deviceosreportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DeviceOSReportFilter:\n")
    for value_set in value_sets['DeviceOSReportFilter']:
        output_deviceosreportfilter(value_set)

def output_devicetypereportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_devicetypereportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DeviceTypeReportFilter:\n")
    for value_set in value_sets['DeviceTypeReportFilter']:
        output_devicetypereportfilter(value_set)

def output_reporttimeperiod(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_reporttimeperiod(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ReportTimePeriod:\n")
    for value_set in value_sets['ReportTimePeriod']:
        output_reporttimeperiod(value_set)

def output_reporttimezone(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_reporttimezone(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ReportTimeZone:\n")
    for value_set in value_sets['ReportTimeZone']:
        output_reporttimezone(value_set)

def output_campaignperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_campaignperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CampaignPerformanceReportColumn:\n")
    for value_set in value_sets['CampaignPerformanceReportColumn']:
        output_campaignperformancereportcolumn(value_set)

def output_campaignstatusreportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_campaignstatusreportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CampaignStatusReportFilter:\n")
    for value_set in value_sets['CampaignStatusReportFilter']:
        output_campaignstatusreportfilter(value_set)

def output_addynamictextperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_addynamictextperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdDynamicTextPerformanceReportColumn:\n")
    for value_set in value_sets['AdDynamicTextPerformanceReportColumn']:
        output_addynamictextperformancereportcolumn(value_set)

def output_adgroupstatusreportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adgroupstatusreportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdGroupStatusReportFilter:\n")
    for value_set in value_sets['AdGroupStatusReportFilter']:
        output_adgroupstatusreportfilter(value_set)

def output_adstatusreportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adstatusreportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdStatusReportFilter:\n")
    for value_set in value_sets['AdStatusReportFilter']:
        output_adstatusreportfilter(value_set)

def output_adtypereportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adtypereportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdTypeReportFilter:\n")
    for value_set in value_sets['AdTypeReportFilter']:
        output_adtypereportfilter(value_set)

def output_keywordstatusreportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_keywordstatusreportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of KeywordStatusReportFilter:\n")
    for value_set in value_sets['KeywordStatusReportFilter']:
        output_keywordstatusreportfilter(value_set)

def output_adgroupperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adgroupperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdGroupPerformanceReportColumn:\n")
    for value_set in value_sets['AdGroupPerformanceReportColumn']:
        output_adgroupperformancereportcolumn(value_set)

def output_adperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdPerformanceReportColumn:\n")
    for value_set in value_sets['AdPerformanceReportColumn']:
        output_adperformancereportcolumn(value_set)

def output_keywordperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_keywordperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of KeywordPerformanceReportColumn:\n")
    for value_set in value_sets['KeywordPerformanceReportColumn']:
        output_keywordperformancereportcolumn(value_set)

def output_bidmatchtypereportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_bidmatchtypereportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BidMatchTypeReportFilter:\n")
    for value_set in value_sets['BidMatchTypeReportFilter']:
        output_bidmatchtypereportfilter(value_set)

def output_bidstrategytypereportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_bidstrategytypereportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BidStrategyTypeReportFilter:\n")
    for value_set in value_sets['BidStrategyTypeReportFilter']:
        output_bidstrategytypereportfilter(value_set)

def output_deliveredmatchtypereportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_deliveredmatchtypereportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DeliveredMatchTypeReportFilter:\n")
    for value_set in value_sets['DeliveredMatchTypeReportFilter']:
        output_deliveredmatchtypereportfilter(value_set)

def output_sortorder(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_sortorder(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of SortOrder:\n")
    for value_set in value_sets['SortOrder']:
        output_sortorder(value_set)

def output_destinationurlperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_destinationurlperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DestinationUrlPerformanceReportColumn:\n")
    for value_set in value_sets['DestinationUrlPerformanceReportColumn']:
        output_destinationurlperformancereportcolumn(value_set)

def output_budgetsummaryreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_budgetsummaryreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BudgetSummaryReportColumn:\n")
    for value_set in value_sets['BudgetSummaryReportColumn']:
        output_budgetsummaryreportcolumn(value_set)

def output_agegenderdemographicreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_agegenderdemographicreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AgeGenderDemographicReportColumn:\n")
    for value_set in value_sets['AgeGenderDemographicReportColumn']:
        output_agegenderdemographicreportcolumn(value_set)

def output_agegenderaudiencereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_agegenderaudiencereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AgeGenderAudienceReportColumn:\n")
    for value_set in value_sets['AgeGenderAudienceReportColumn']:
        output_agegenderaudiencereportcolumn(value_set)

def output_professionaldemographicsaudiencereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_professionaldemographicsaudiencereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ProfessionalDemographicsAudienceReportColumn:\n")
    for value_set in value_sets['ProfessionalDemographicsAudienceReportColumn']:
        output_professionaldemographicsaudiencereportcolumn(value_set)

def output_userlocationperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_userlocationperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of UserLocationPerformanceReportColumn:\n")
    for value_set in value_sets['UserLocationPerformanceReportColumn']:
        output_userlocationperformancereportcolumn(value_set)

def output_publisherusageperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_publisherusageperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of PublisherUsagePerformanceReportColumn:\n")
    for value_set in value_sets['PublisherUsagePerformanceReportColumn']:
        output_publisherusageperformancereportcolumn(value_set)

def output_searchqueryperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_searchqueryperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of SearchQueryPerformanceReportColumn:\n")
    for value_set in value_sets['SearchQueryPerformanceReportColumn']:
        output_searchqueryperformancereportcolumn(value_set)

def output_conversionperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_conversionperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ConversionPerformanceReportColumn:\n")
    for value_set in value_sets['ConversionPerformanceReportColumn']:
        output_conversionperformancereportcolumn(value_set)

def output_goalsandfunnelsreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_goalsandfunnelsreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of GoalsAndFunnelsReportColumn:\n")
    for value_set in value_sets['GoalsAndFunnelsReportColumn']:
        output_goalsandfunnelsreportcolumn(value_set)

def output_negativekeywordconflictreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_negativekeywordconflictreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of NegativeKeywordConflictReportColumn:\n")
    for value_set in value_sets['NegativeKeywordConflictReportColumn']:
        output_negativekeywordconflictreportcolumn(value_set)

def output_searchcampaignchangehistoryreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_searchcampaignchangehistoryreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of SearchCampaignChangeHistoryReportColumn:\n")
    for value_set in value_sets['SearchCampaignChangeHistoryReportColumn']:
        output_searchcampaignchangehistoryreportcolumn(value_set)

def output_changetypereportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_changetypereportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ChangeTypeReportFilter:\n")
    for value_set in value_sets['ChangeTypeReportFilter']:
        output_changetypereportfilter(value_set)

def output_changeentityreportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_changeentityreportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ChangeEntityReportFilter:\n")
    for value_set in value_sets['ChangeEntityReportFilter']:
        output_changeentityreportfilter(value_set)

def output_adextensionbyadreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adextensionbyadreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdExtensionByAdReportColumn:\n")
    for value_set in value_sets['AdExtensionByAdReportColumn']:
        output_adextensionbyadreportcolumn(value_set)

def output_adextensionbykeywordreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adextensionbykeywordreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdExtensionByKeywordReportColumn:\n")
    for value_set in value_sets['AdExtensionByKeywordReportColumn']:
        output_adextensionbykeywordreportcolumn(value_set)

def output_audienceperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_audienceperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AudiencePerformanceReportColumn:\n")
    for value_set in value_sets['AudiencePerformanceReportColumn']:
        output_audienceperformancereportcolumn(value_set)

def output_adextensiondetailreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adextensiondetailreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdExtensionDetailReportColumn:\n")
    for value_set in value_sets['AdExtensionDetailReportColumn']:
        output_adextensiondetailreportcolumn(value_set)

def output_shareofvoicereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_shareofvoicereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ShareOfVoiceReportColumn:\n")
    for value_set in value_sets['ShareOfVoiceReportColumn']:
        output_shareofvoicereportcolumn(value_set)

def output_productdimensionperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_productdimensionperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ProductDimensionPerformanceReportColumn:\n")
    for value_set in value_sets['ProductDimensionPerformanceReportColumn']:
        output_productdimensionperformancereportcolumn(value_set)

def output_productpartitionperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_productpartitionperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ProductPartitionPerformanceReportColumn:\n")
    for value_set in value_sets['ProductPartitionPerformanceReportColumn']:
        output_productpartitionperformancereportcolumn(value_set)

def output_productpartitionunitperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_productpartitionunitperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ProductPartitionUnitPerformanceReportColumn:\n")
    for value_set in value_sets['ProductPartitionUnitPerformanceReportColumn']:
        output_productpartitionunitperformancereportcolumn(value_set)

def output_productsearchqueryperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_productsearchqueryperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ProductSearchQueryPerformanceReportColumn:\n")
    for value_set in value_sets['ProductSearchQueryPerformanceReportColumn']:
        output_productsearchqueryperformancereportcolumn(value_set)

def output_productmatchcountreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_productmatchcountreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ProductMatchCountReportColumn:\n")
    for value_set in value_sets['ProductMatchCountReportColumn']:
        output_productmatchcountreportcolumn(value_set)

def output_calldetailreportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_calldetailreportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CallDetailReportColumn:\n")
    for value_set in value_sets['CallDetailReportColumn']:
        output_calldetailreportcolumn(value_set)

def output_geographicperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_geographicperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of GeographicPerformanceReportColumn:\n")
    for value_set in value_sets['GeographicPerformanceReportColumn']:
        output_geographicperformancereportcolumn(value_set)

def output_dsasearchqueryperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_dsasearchqueryperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DSASearchQueryPerformanceReportColumn:\n")
    for value_set in value_sets['DSASearchQueryPerformanceReportColumn']:
        output_dsasearchqueryperformancereportcolumn(value_set)

def output_dsaautotargetperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_dsaautotargetperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DSAAutoTargetPerformanceReportColumn:\n")
    for value_set in value_sets['DSAAutoTargetPerformanceReportColumn']:
        output_dsaautotargetperformancereportcolumn(value_set)

def output_dynamicadtargetstatusreportfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_dynamicadtargetstatusreportfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DynamicAdTargetStatusReportFilter:\n")
    for value_set in value_sets['DynamicAdTargetStatusReportFilter']:
        output_dynamicadtargetstatusreportfilter(value_set)

def output_dsacategoryperformancereportcolumn(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_dsacategoryperformancereportcolumn(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DSACategoryPerformanceReportColumn:\n")
    for value_set in value_sets['DSACategoryPerformanceReportColumn']:
        output_dsacategoryperformancereportcolumn(value_set)

def output_reportrequeststatustype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_reportrequeststatustype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ReportRequestStatusType:\n")
    for value_set in value_sets['ReportRequestStatusType']:
        output_reportrequeststatustype(value_set)

def output_array_of_long(items):
    if items is None or items['long'] is None:
        return
    output_status_message("Array Of long:")
    for item in items['long']:
        output_status_message("Value of the long: {0}".format(item))
def output_array_of_string(items):
    if items is None or items['string'] is None:
        return
    output_status_message("Array Of string:")
    for item in items['string']:
        output_status_message("Value of the string: {0}".format(item))
def output_status_message(message):
    print(message)
