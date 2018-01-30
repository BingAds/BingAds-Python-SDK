def output_accountmigrationstatusesinfo(data_object):
    if data_object is None:
        return
    output_status_message("AccountMigrationStatusesInfo (Data Object):")
    output_status_message("AccountId: {0}".format(data_object.AccountId))
    output_status_message("MigrationStatusInfo (Element Name):")
    output_array_of_migrationstatusinfo(data_object.MigrationStatusInfo)

def output_array_of_accountmigrationstatusesinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AccountMigrationStatusesInfo:\n")
    for data_object in data_objects['AccountMigrationStatusesInfo']:
        output_accountmigrationstatusesinfo(data_object)
        output_status_message("\n")

def output_accountproperty(data_object):
    if data_object is None:
        return
    output_status_message("AccountProperty (Data Object):")
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Value: {0}".format(data_object.Value))

def output_array_of_accountproperty(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AccountProperty:\n")
    for data_object in data_objects['AccountProperty']:
        output_accountproperty(data_object)
        output_status_message("\n")

def output_ad(data_object):
    if data_object is None:
        return
    output_status_message("Ad (Data Object):")
    output_status_message("AdFormatPreference: {0}".format(data_object.AdFormatPreference))
    output_status_message("DevicePreference: {0}".format(data_object.DevicePreference))
    output_status_message("EditorialStatus: {0}".format(data_object.EditorialStatus))
    output_status_message("FinalAppUrls (Element Name):")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls (Element Name):")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrls (Element Name):")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)
    if data_object.Type == 'AppInstallAd':
        output_appinstallad(data_object)
    if data_object.Type == 'DynamicSearchAd':
        output_dynamicsearchad(data_object)
    if data_object.Type == 'ExpandedTextAd':
        output_expandedtextad(data_object)
    if data_object.Type == 'ProductAd':
        output_productad(data_object)
    if data_object.Type == 'TextAd':
        output_textad(data_object)

def output_array_of_ad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Ad:\n")
    for data_object in data_objects['Ad']:
        output_ad(data_object)
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

def output_address(data_object):
    if data_object is None:
        return
    output_status_message("Address (Data Object):")
    output_status_message("CityName: {0}".format(data_object.CityName))
    output_status_message("CountryCode: {0}".format(data_object.CountryCode))
    output_status_message("PostalCode: {0}".format(data_object.PostalCode))
    output_status_message("ProvinceCode: {0}".format(data_object.ProvinceCode))
    output_status_message("ProvinceName: {0}".format(data_object.ProvinceName))
    output_status_message("StreetAddress: {0}".format(data_object.StreetAddress))
    output_status_message("StreetAddress2: {0}".format(data_object.StreetAddress2))

def output_array_of_address(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Address:\n")
    for data_object in data_objects['Address']:
        output_address(data_object)
        output_status_message("\n")

def output_adextension(data_object):
    if data_object is None:
        return
    output_status_message("AdExtension (Data Object):")
    output_status_message("DevicePreference: {0}".format(data_object.DevicePreference))
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Scheduling (Element Name):")
    output_schedule(data_object.Scheduling)
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("Version: {0}".format(data_object.Version))
    if data_object.Type == 'AppAdExtension':
        output_appadextension(data_object)
    if data_object.Type == 'CallAdExtension':
        output_calladextension(data_object)
    if data_object.Type == 'CalloutAdExtension':
        output_calloutadextension(data_object)
    if data_object.Type == 'ImageAdExtension':
        output_imageadextension(data_object)
    if data_object.Type == 'LocationAdExtension':
        output_locationadextension(data_object)
    if data_object.Type == 'PriceAdExtension':
        output_priceadextension(data_object)
    if data_object.Type == 'ReviewAdExtension':
        output_reviewadextension(data_object)
    if data_object.Type == 'Sitelink2AdExtension':
        output_sitelink2adextension(data_object)
    if data_object.Type == 'SiteLinksAdExtension':
        output_sitelinksadextension(data_object)
    if data_object.Type == 'StructuredSnippetAdExtension':
        output_structuredsnippetadextension(data_object)

def output_array_of_adextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtension:\n")
    for data_object in data_objects['AdExtension']:
        output_adextension(data_object)
        output_status_message("\n")

def output_adextensionassociation(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionAssociation (Data Object):")
    output_status_message("AdExtension (Element Name):")
    output_adextension(data_object.AdExtension)
    output_status_message("AssociationType: {0}".format(data_object.AssociationType))
    output_status_message("EditorialStatus: {0}".format(data_object.EditorialStatus))
    output_status_message("EntityId: {0}".format(data_object.EntityId))

def output_array_of_adextensionassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionAssociation:\n")
    for data_object in data_objects['AdExtensionAssociation']:
        output_adextensionassociation(data_object)
        output_status_message("\n")

def output_adextensionassociationcollection(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionAssociationCollection (Data Object):")
    output_status_message("AdExtensionAssociations (Element Name):")
    output_array_of_adextensionassociation(data_object.AdExtensionAssociations)

def output_array_of_adextensionassociationcollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionAssociationCollection:\n")
    for data_object in data_objects['AdExtensionAssociationCollection']:
        output_adextensionassociationcollection(data_object)
        output_status_message("\n")

def output_adextensioneditorialreason(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionEditorialReason (Data Object):")
    output_status_message("Location: {0}".format(data_object.Location))
    output_status_message("PublisherCountries (Element Name):")
    output_array_of_string(data_object.PublisherCountries)
    output_status_message("ReasonCode: {0}".format(data_object.ReasonCode))
    output_status_message("Term: {0}".format(data_object.Term))

def output_array_of_adextensioneditorialreason(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionEditorialReason:\n")
    for data_object in data_objects['AdExtensionEditorialReason']:
        output_adextensioneditorialreason(data_object)
        output_status_message("\n")

def output_adextensioneditorialreasoncollection(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionEditorialReasonCollection (Data Object):")
    output_status_message("AdExtensionId: {0}".format(data_object.AdExtensionId))
    output_status_message("Reasons (Element Name):")
    output_array_of_adextensioneditorialreason(data_object.Reasons)

def output_array_of_adextensioneditorialreasoncollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionEditorialReasonCollection:\n")
    for data_object in data_objects['AdExtensionEditorialReasonCollection']:
        output_adextensioneditorialreasoncollection(data_object)
        output_status_message("\n")

def output_adextensionidentity(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionIdentity (Data Object):")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Version: {0}".format(data_object.Version))

def output_array_of_adextensionidentity(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionIdentity:\n")
    for data_object in data_objects['AdExtensionIdentity']:
        output_adextensionidentity(data_object)
        output_status_message("\n")

def output_adextensionidtoentityidassociation(data_object):
    if data_object is None:
        return
    output_status_message("AdExtensionIdToEntityIdAssociation (Data Object):")
    output_status_message("AdExtensionId: {0}".format(data_object.AdExtensionId))
    output_status_message("EntityId: {0}".format(data_object.EntityId))

def output_array_of_adextensionidtoentityidassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdExtensionIdToEntityIdAssociation:\n")
    for data_object in data_objects['AdExtensionIdToEntityIdAssociation']:
        output_adextensionidtoentityidassociation(data_object)
        output_status_message("\n")

def output_adgroup(data_object):
    if data_object is None:
        return
    output_status_message("AdGroup (Data Object):")
    output_status_message("AdDistribution: {0}".format(data_object.AdDistribution))
    output_status_message("AdRotation (Element Name):")
    output_adrotation(data_object.AdRotation)
    output_status_message("BiddingScheme (Element Name):")
    output_biddingscheme(data_object.BiddingScheme)
    output_status_message("ContentMatchBid (Element Name):")
    output_bid(data_object.ContentMatchBid)
    output_status_message("EndDate (Element Name):")
    output_date(data_object.EndDate)
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("NativeBidAdjustment: {0}".format(data_object.NativeBidAdjustment))
    output_status_message("Network: {0}".format(data_object.Network))
    output_status_message("PricingModel: {0}".format(data_object.PricingModel))
    output_status_message("RemarketingTargetingSetting: {0}".format(data_object.RemarketingTargetingSetting))
    output_status_message("SearchBid (Element Name):")
    output_bid(data_object.SearchBid)
    output_status_message("Settings (Element Name):")
    output_array_of_setting(data_object.Settings)
    output_status_message("StartDate (Element Name):")
    output_date(data_object.StartDate)
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)

def output_array_of_adgroup(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdGroup:\n")
    for data_object in data_objects['AdGroup']:
        output_adgroup(data_object)
        output_status_message("\n")

def output_adgroupcriterion(data_object):
    if data_object is None:
        return
    output_status_message("AdGroupCriterion (Data Object):")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("Criterion (Element Name):")
    output_criterion(data_object.Criterion)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'BiddableAdGroupCriterion':
        output_biddableadgroupcriterion(data_object)
    if data_object.Type == 'NegativeAdGroupCriterion':
        output_negativeadgroupcriterion(data_object)

def output_array_of_adgroupcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdGroupCriterion:\n")
    for data_object in data_objects['AdGroupCriterion']:
        output_adgroupcriterion(data_object)
        output_status_message("\n")

def output_adgroupcriterionaction(data_object):
    if data_object is None:
        return
    output_status_message("AdGroupCriterionAction (Data Object):")
    output_status_message("Action: {0}".format(data_object.Action))
    output_status_message("AdGroupCriterion (Element Name):")
    output_adgroupcriterion(data_object.AdGroupCriterion)

def output_array_of_adgroupcriterionaction(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdGroupCriterionAction:\n")
    for data_object in data_objects['AdGroupCriterionAction']:
        output_adgroupcriterionaction(data_object)
        output_status_message("\n")

def output_adgroupnegativesites(data_object):
    if data_object is None:
        return
    output_status_message("AdGroupNegativeSites (Data Object):")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("NegativeSites (Element Name):")
    output_array_of_string(data_object.NegativeSites)

def output_array_of_adgroupnegativesites(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdGroupNegativeSites:\n")
    for data_object in data_objects['AdGroupNegativeSites']:
        output_adgroupnegativesites(data_object)
        output_status_message("\n")

def output_adrotation(data_object):
    if data_object is None:
        return
    output_status_message("AdRotation (Data Object):")
    output_status_message("EndDate: {0}".format(data_object.EndDate))
    output_status_message("StartDate: {0}".format(data_object.StartDate))
    output_status_message("Type: {0}".format(data_object.Type))

def output_array_of_adrotation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AdRotation:\n")
    for data_object in data_objects['AdRotation']:
        output_adrotation(data_object)
        output_status_message("\n")

def output_agecriterion(data_object):
    if data_object is None:
        return
    output_status_message("AgeCriterion (Data Object):")
    output_status_message("AgeRange: {0}".format(data_object.AgeRange))

def output_array_of_agecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AgeCriterion:\n")
    for data_object in data_objects['AgeCriterion']:
        output_agecriterion(data_object)
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

def output_appadextension(data_object):
    if data_object is None:
        return
    output_status_message("AppAdExtension (Data Object):")
    output_status_message("AppPlatform: {0}".format(data_object.AppPlatform))
    output_status_message("AppStoreId: {0}".format(data_object.AppStoreId))
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("DisplayText: {0}".format(data_object.DisplayText))
    output_status_message("FinalAppUrls (Element Name):")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls (Element Name):")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrls (Element Name):")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)

def output_array_of_appadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AppAdExtension:\n")
    for data_object in data_objects['AppAdExtension']:
        output_appadextension(data_object)
        output_status_message("\n")

def output_appinstallad(data_object):
    if data_object is None:
        return
    output_status_message("AppInstallAd (Data Object):")
    output_status_message("AppPlatform: {0}".format(data_object.AppPlatform))
    output_status_message("AppStoreId: {0}".format(data_object.AppStoreId))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("Title: {0}".format(data_object.Title))

def output_array_of_appinstallad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AppInstallAd:\n")
    for data_object in data_objects['AppInstallAd']:
        output_appinstallad(data_object)
        output_status_message("\n")

def output_appinstallgoal(data_object):
    if data_object is None:
        return
    output_status_message("AppInstallGoal (Data Object):")
    output_status_message("AppPlatform: {0}".format(data_object.AppPlatform))
    output_status_message("AppStoreId: {0}".format(data_object.AppStoreId))

def output_array_of_appinstallgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AppInstallGoal:\n")
    for data_object in data_objects['AppInstallGoal']:
        output_appinstallgoal(data_object)
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
    if data_object.Type == 'EditorialApiFaultDetail':
        output_editorialapifaultdetail(data_object)

def output_array_of_applicationfault(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ApplicationFault:\n")
    for data_object in data_objects['ApplicationFault']:
        output_applicationfault(data_object)
        output_status_message("\n")

def output_appurl(data_object):
    if data_object is None:
        return
    output_status_message("AppUrl (Data Object):")
    output_status_message("OsType: {0}".format(data_object.OsType))
    output_status_message("Url: {0}".format(data_object.Url))

def output_array_of_appurl(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AppUrl:\n")
    for data_object in data_objects['AppUrl']:
        output_appurl(data_object)
        output_status_message("\n")

def output_audience(data_object):
    if data_object is None:
        return
    output_status_message("Audience (Data Object):")
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MembershipDuration: {0}".format(data_object.MembershipDuration))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("ParentId: {0}".format(data_object.ParentId))
    output_status_message("Scope: {0}".format(data_object.Scope))
    output_status_message("SearchSize: {0}".format(data_object.SearchSize))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'CustomAudience':
        output_customaudience(data_object)
    if data_object.Type == 'InMarketAudience':
        output_inmarketaudience(data_object)
    if data_object.Type == 'RemarketingList':
        output_remarketinglist(data_object)

def output_array_of_audience(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Audience:\n")
    for data_object in data_objects['Audience']:
        output_audience(data_object)
        output_status_message("\n")

def output_audiencecriterion(data_object):
    if data_object is None:
        return
    output_status_message("AudienceCriterion (Data Object):")
    output_status_message("AudienceId: {0}".format(data_object.AudienceId))
    output_status_message("AudienceType: {0}".format(data_object.AudienceType))

def output_array_of_audiencecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of AudienceCriterion:\n")
    for data_object in data_objects['AudienceCriterion']:
        output_audiencecriterion(data_object)
        output_status_message("\n")

def output_batcherror(data_object):
    if data_object is None:
        return
    output_status_message("BatchError (Data Object):")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("FieldPath: {0}".format(data_object.FieldPath))
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Message: {0}".format(data_object.Message))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'EditorialError':
        output_editorialerror(data_object)

def output_array_of_batcherror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BatchError:\n")
    for data_object in data_objects['BatchError']:
        output_batcherror(data_object)
        output_status_message("\n")

def output_batcherrorcollection(data_object):
    if data_object is None:
        return
    output_status_message("BatchErrorCollection (Data Object):")
    output_status_message("BatchErrors (Element Name):")
    output_array_of_batcherror(data_object.BatchErrors)
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("FieldPath: {0}".format(data_object.FieldPath))
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Message: {0}".format(data_object.Message))
    output_status_message("Type: {0}".format(data_object.Type))

def output_array_of_batcherrorcollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BatchErrorCollection:\n")
    for data_object in data_objects['BatchErrorCollection']:
        output_batcherrorcollection(data_object)
        output_status_message("\n")

def output_bid(data_object):
    if data_object is None:
        return
    output_status_message("Bid (Data Object):")
    output_status_message("Amount: {0}".format(data_object.Amount))

def output_array_of_bid(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Bid:\n")
    for data_object in data_objects['Bid']:
        output_bid(data_object)
        output_status_message("\n")

def output_biddableadgroupcriterion(data_object):
    if data_object is None:
        return
    output_status_message("BiddableAdGroupCriterion (Data Object):")
    output_status_message("CriterionBid (Element Name):")
    output_criterionbid(data_object.CriterionBid)
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("EditorialStatus: {0}".format(data_object.EditorialStatus))
    output_status_message("FinalAppUrls (Element Name):")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls (Element Name):")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrls (Element Name):")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)

def output_array_of_biddableadgroupcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BiddableAdGroupCriterion:\n")
    for data_object in data_objects['BiddableAdGroupCriterion']:
        output_biddableadgroupcriterion(data_object)
        output_status_message("\n")

def output_biddablecampaigncriterion(data_object):
    if data_object is None:
        return
    output_status_message("BiddableCampaignCriterion (Data Object):")
    output_status_message("CriterionBid (Element Name):")
    output_criterionbid(data_object.CriterionBid)

def output_array_of_biddablecampaigncriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BiddableCampaignCriterion:\n")
    for data_object in data_objects['BiddableCampaignCriterion']:
        output_biddablecampaigncriterion(data_object)
        output_status_message("\n")

def output_biddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("BiddingScheme (Data Object):")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'EnhancedCpcBiddingScheme':
        output_enhancedcpcbiddingscheme(data_object)
    if data_object.Type == 'InheritFromParentBiddingScheme':
        output_inheritfromparentbiddingscheme(data_object)
    if data_object.Type == 'ManualCpcBiddingScheme':
        output_manualcpcbiddingscheme(data_object)
    if data_object.Type == 'MaxClicksBiddingScheme':
        output_maxclicksbiddingscheme(data_object)
    if data_object.Type == 'MaxConversionsBiddingScheme':
        output_maxconversionsbiddingscheme(data_object)
    if data_object.Type == 'TargetCpaBiddingScheme':
        output_targetcpabiddingscheme(data_object)

def output_array_of_biddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BiddingScheme:\n")
    for data_object in data_objects['BiddingScheme']:
        output_biddingscheme(data_object)
        output_status_message("\n")

def output_bidmultiplier(data_object):
    if data_object is None:
        return
    output_status_message("BidMultiplier (Data Object):")
    output_status_message("Multiplier: {0}".format(data_object.Multiplier))

def output_array_of_bidmultiplier(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BidMultiplier:\n")
    for data_object in data_objects['BidMultiplier']:
        output_bidmultiplier(data_object)
        output_status_message("\n")

def output_bmcstore(data_object):
    if data_object is None:
        return
    output_status_message("BMCStore (Data Object):")
    output_status_message("HasCatalog: {0}".format(data_object.HasCatalog))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("IsActive: {0}".format(data_object.IsActive))
    output_status_message("IsProductAdsEnabled: {0}".format(data_object.IsProductAdsEnabled))
    output_status_message("Name: {0}".format(data_object.Name))

def output_array_of_bmcstore(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BMCStore:\n")
    for data_object in data_objects['BMCStore']:
        output_bmcstore(data_object)
        output_status_message("\n")

def output_budget(data_object):
    if data_object is None:
        return
    output_status_message("Budget (Data Object):")
    output_status_message("Amount: {0}".format(data_object.Amount))
    output_status_message("AssociationCount: {0}".format(data_object.AssociationCount))
    output_status_message("BudgetType: {0}".format(data_object.BudgetType))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))

def output_array_of_budget(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Budget:\n")
    for data_object in data_objects['Budget']:
        output_budget(data_object)
        output_status_message("\n")

def output_calladextension(data_object):
    if data_object is None:
        return
    output_status_message("CallAdExtension (Data Object):")
    output_status_message("CountryCode: {0}".format(data_object.CountryCode))
    output_status_message("IsCallOnly: {0}".format(data_object.IsCallOnly))
    output_status_message("IsCallTrackingEnabled: {0}".format(data_object.IsCallTrackingEnabled))
    output_status_message("PhoneNumber: {0}".format(data_object.PhoneNumber))
    output_status_message("RequireTollFreeTrackingNumber: {0}".format(data_object.RequireTollFreeTrackingNumber))

def output_array_of_calladextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CallAdExtension:\n")
    for data_object in data_objects['CallAdExtension']:
        output_calladextension(data_object)
        output_status_message("\n")

def output_calloutadextension(data_object):
    if data_object is None:
        return
    output_status_message("CalloutAdExtension (Data Object):")
    output_status_message("Text: {0}".format(data_object.Text))

def output_array_of_calloutadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CalloutAdExtension:\n")
    for data_object in data_objects['CalloutAdExtension']:
        output_calloutadextension(data_object)
        output_status_message("\n")

def output_campaign(data_object):
    if data_object is None:
        return
    output_status_message("Campaign (Data Object):")
    output_status_message("BiddingScheme (Element Name):")
    output_biddingscheme(data_object.BiddingScheme)
    output_status_message("BudgetType: {0}".format(data_object.BudgetType))
    output_status_message("DailyBudget: {0}".format(data_object.DailyBudget))
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("NativeBidAdjustment: {0}".format(data_object.NativeBidAdjustment))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("TimeZone: {0}".format(data_object.TimeZone))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("CampaignType: {0}".format(data_object.CampaignType))
    output_status_message("Settings (Element Name):")
    output_array_of_setting(data_object.Settings)
    output_status_message("BudgetId: {0}".format(data_object.BudgetId))
    output_status_message("Languages (Element Name):")
    output_array_of_string(data_object.Languages)

def output_array_of_campaign(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Campaign:\n")
    for data_object in data_objects['Campaign']:
        output_campaign(data_object)
        output_status_message("\n")

def output_campaigncriterion(data_object):
    if data_object is None:
        return
    output_status_message("CampaignCriterion (Data Object):")
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("Criterion (Element Name):")
    output_criterion(data_object.Criterion)
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'BiddableCampaignCriterion':
        output_biddablecampaigncriterion(data_object)
    if data_object.Type == 'NegativeCampaignCriterion':
        output_negativecampaigncriterion(data_object)

def output_array_of_campaigncriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CampaignCriterion:\n")
    for data_object in data_objects['CampaignCriterion']:
        output_campaigncriterion(data_object)
        output_status_message("\n")

def output_campaignnegativesites(data_object):
    if data_object is None:
        return
    output_status_message("CampaignNegativeSites (Data Object):")
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("NegativeSites (Element Name):")
    output_array_of_string(data_object.NegativeSites)

def output_array_of_campaignnegativesites(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CampaignNegativeSites:\n")
    for data_object in data_objects['CampaignNegativeSites']:
        output_campaignnegativesites(data_object)
        output_status_message("\n")

def output_conversiongoal(data_object):
    if data_object is None:
        return
    output_status_message("ConversionGoal (Data Object):")
    output_status_message("ConversionWindowInMinutes: {0}".format(data_object.ConversionWindowInMinutes))
    output_status_message("CountType: {0}".format(data_object.CountType))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Revenue (Element Name):")
    output_conversiongoalrevenue(data_object.Revenue)
    output_status_message("Scope: {0}".format(data_object.Scope))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("TagId: {0}".format(data_object.TagId))
    output_status_message("TrackingStatus: {0}".format(data_object.TrackingStatus))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'AppInstallGoal':
        output_appinstallgoal(data_object)
    if data_object.Type == 'DurationGoal':
        output_durationgoal(data_object)
    if data_object.Type == 'EventGoal':
        output_eventgoal(data_object)
    if data_object.Type == 'InStoreTransactionGoal':
        output_instoretransactiongoal(data_object)
    if data_object.Type == 'OfflineConversionGoal':
        output_offlineconversiongoal(data_object)
    if data_object.Type == 'PagesViewedPerVisitGoal':
        output_pagesviewedpervisitgoal(data_object)
    if data_object.Type == 'UrlGoal':
        output_urlgoal(data_object)

def output_array_of_conversiongoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ConversionGoal:\n")
    for data_object in data_objects['ConversionGoal']:
        output_conversiongoal(data_object)
        output_status_message("\n")

def output_conversiongoalrevenue(data_object):
    if data_object is None:
        return
    output_status_message("ConversionGoalRevenue (Data Object):")
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("Value: {0}".format(data_object.Value))

def output_array_of_conversiongoalrevenue(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ConversionGoalRevenue:\n")
    for data_object in data_objects['ConversionGoalRevenue']:
        output_conversiongoalrevenue(data_object)
        output_status_message("\n")

def output_criterion(data_object):
    if data_object is None:
        return
    output_status_message("Criterion (Data Object):")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'AgeCriterion':
        output_agecriterion(data_object)
    if data_object.Type == 'AudienceCriterion':
        output_audiencecriterion(data_object)
    if data_object.Type == 'DayTimeCriterion':
        output_daytimecriterion(data_object)
    if data_object.Type == 'DeviceCriterion':
        output_devicecriterion(data_object)
    if data_object.Type == 'GenderCriterion':
        output_gendercriterion(data_object)
    if data_object.Type == 'LocationCriterion':
        output_locationcriterion(data_object)
    if data_object.Type == 'LocationIntentCriterion':
        output_locationintentcriterion(data_object)
    if data_object.Type == 'ProductPartition':
        output_productpartition(data_object)
    if data_object.Type == 'ProductScope':
        output_productscope(data_object)
    if data_object.Type == 'RadiusCriterion':
        output_radiuscriterion(data_object)
    if data_object.Type == 'Webpage':
        output_webpage(data_object)

def output_array_of_criterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Criterion:\n")
    for data_object in data_objects['Criterion']:
        output_criterion(data_object)
        output_status_message("\n")

def output_criterionbid(data_object):
    if data_object is None:
        return
    output_status_message("CriterionBid (Data Object):")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'BidMultiplier':
        output_bidmultiplier(data_object)
    if data_object.Type == 'FixedBid':
        output_fixedbid(data_object)

def output_array_of_criterionbid(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CriterionBid:\n")
    for data_object in data_objects['CriterionBid']:
        output_criterionbid(data_object)
        output_status_message("\n")

def output_customaudience(data_object):
    if data_object is None:
        return
    output_status_message("CustomAudience (Data Object):")

def output_array_of_customaudience(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CustomAudience:\n")
    for data_object in data_objects['CustomAudience']:
        output_customaudience(data_object)
        output_status_message("\n")

def output_customeventsrule(data_object):
    if data_object is None:
        return
    output_status_message("CustomEventsRule (Data Object):")
    output_status_message("Action: {0}".format(data_object.Action))
    output_status_message("ActionOperator: {0}".format(data_object.ActionOperator))
    output_status_message("Category: {0}".format(data_object.Category))
    output_status_message("CategoryOperator: {0}".format(data_object.CategoryOperator))
    output_status_message("Label: {0}".format(data_object.Label))
    output_status_message("LabelOperator: {0}".format(data_object.LabelOperator))
    output_status_message("Value: {0}".format(data_object.Value))
    output_status_message("ValueOperator: {0}".format(data_object.ValueOperator))

def output_array_of_customeventsrule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CustomEventsRule:\n")
    for data_object in data_objects['CustomEventsRule']:
        output_customeventsrule(data_object)
        output_status_message("\n")

def output_customparameter(data_object):
    if data_object is None:
        return
    output_status_message("CustomParameter (Data Object):")
    output_status_message("Key: {0}".format(data_object.Key))
    output_status_message("Value: {0}".format(data_object.Value))

def output_array_of_customparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CustomParameter:\n")
    for data_object in data_objects['CustomParameter']:
        output_customparameter(data_object)
        output_status_message("\n")

def output_customparameters(data_object):
    if data_object is None:
        return
    output_status_message("CustomParameters (Data Object):")
    output_status_message("Parameters (Element Name):")
    output_array_of_customparameter(data_object.Parameters)

def output_array_of_customparameters(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CustomParameters:\n")
    for data_object in data_objects['CustomParameters']:
        output_customparameters(data_object)
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

def output_daytime(data_object):
    if data_object is None:
        return
    output_status_message("DayTime (Data Object):")
    output_status_message("Day: {0}".format(data_object.Day))
    output_status_message("EndHour: {0}".format(data_object.EndHour))
    output_status_message("EndMinute: {0}".format(data_object.EndMinute))
    output_status_message("StartHour: {0}".format(data_object.StartHour))
    output_status_message("StartMinute: {0}".format(data_object.StartMinute))

def output_array_of_daytime(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DayTime:\n")
    for data_object in data_objects['DayTime']:
        output_daytime(data_object)
        output_status_message("\n")

def output_daytimecriterion(data_object):
    if data_object is None:
        return
    output_status_message("DayTimeCriterion (Data Object):")
    output_status_message("Day: {0}".format(data_object.Day))
    output_status_message("FromHour: {0}".format(data_object.FromHour))
    output_status_message("FromMinute: {0}".format(data_object.FromMinute))
    output_status_message("ToHour: {0}".format(data_object.ToHour))
    output_status_message("ToMinute: {0}".format(data_object.ToMinute))

def output_array_of_daytimecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DayTimeCriterion:\n")
    for data_object in data_objects['DayTimeCriterion']:
        output_daytimecriterion(data_object)
        output_status_message("\n")

def output_devicecriterion(data_object):
    if data_object is None:
        return
    output_status_message("DeviceCriterion (Data Object):")
    output_status_message("DeviceName: {0}".format(data_object.DeviceName))
    output_status_message("OSName: {0}".format(data_object.OSName))

def output_array_of_devicecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DeviceCriterion:\n")
    for data_object in data_objects['DeviceCriterion']:
        output_devicecriterion(data_object)
        output_status_message("\n")

def output_durationgoal(data_object):
    if data_object is None:
        return
    output_status_message("DurationGoal (Data Object):")
    output_status_message("MinimumDurationInSeconds: {0}".format(data_object.MinimumDurationInSeconds))

def output_array_of_durationgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DurationGoal:\n")
    for data_object in data_objects['DurationGoal']:
        output_durationgoal(data_object)
        output_status_message("\n")

def output_dynamicsearchad(data_object):
    if data_object is None:
        return
    output_status_message("DynamicSearchAd (Data Object):")
    output_status_message("Path1: {0}".format(data_object.Path1))
    output_status_message("Path2: {0}".format(data_object.Path2))
    output_status_message("Text: {0}".format(data_object.Text))

def output_array_of_dynamicsearchad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DynamicSearchAd:\n")
    for data_object in data_objects['DynamicSearchAd']:
        output_dynamicsearchad(data_object)
        output_status_message("\n")

def output_dynamicsearchadssetting(data_object):
    if data_object is None:
        return
    output_status_message("DynamicSearchAdsSetting (Data Object):")
    output_status_message("DomainName: {0}".format(data_object.DomainName))
    output_status_message("Language: {0}".format(data_object.Language))

def output_array_of_dynamicsearchadssetting(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of DynamicSearchAdsSetting:\n")
    for data_object in data_objects['DynamicSearchAdsSetting']:
        output_dynamicsearchadssetting(data_object)
        output_status_message("\n")

def output_editorialapifaultdetail(data_object):
    if data_object is None:
        return
    output_status_message("EditorialApiFaultDetail (Data Object):")
    output_status_message("BatchErrors (Element Name):")
    output_array_of_batcherror(data_object.BatchErrors)
    output_status_message("EditorialErrors (Element Name):")
    output_array_of_editorialerror(data_object.EditorialErrors)
    output_status_message("OperationErrors (Element Name):")
    output_array_of_operationerror(data_object.OperationErrors)

def output_array_of_editorialapifaultdetail(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of EditorialApiFaultDetail:\n")
    for data_object in data_objects['EditorialApiFaultDetail']:
        output_editorialapifaultdetail(data_object)
        output_status_message("\n")

def output_editorialerror(data_object):
    if data_object is None:
        return
    output_status_message("EditorialError (Data Object):")
    output_status_message("Appealable: {0}".format(data_object.Appealable))
    output_status_message("DisapprovedText: {0}".format(data_object.DisapprovedText))
    output_status_message("Location: {0}".format(data_object.Location))
    output_status_message("PublisherCountry: {0}".format(data_object.PublisherCountry))
    output_status_message("ReasonCode: {0}".format(data_object.ReasonCode))

def output_array_of_editorialerror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of EditorialError:\n")
    for data_object in data_objects['EditorialError']:
        output_editorialerror(data_object)
        output_status_message("\n")

def output_editorialreason(data_object):
    if data_object is None:
        return
    output_status_message("EditorialReason (Data Object):")
    output_status_message("Location: {0}".format(data_object.Location))
    output_status_message("PublisherCountries (Element Name):")
    output_array_of_string(data_object.PublisherCountries)
    output_status_message("ReasonCode: {0}".format(data_object.ReasonCode))
    output_status_message("Term: {0}".format(data_object.Term))

def output_array_of_editorialreason(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of EditorialReason:\n")
    for data_object in data_objects['EditorialReason']:
        output_editorialreason(data_object)
        output_status_message("\n")

def output_editorialreasoncollection(data_object):
    if data_object is None:
        return
    output_status_message("EditorialReasonCollection (Data Object):")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("AdOrKeywordId: {0}".format(data_object.AdOrKeywordId))
    output_status_message("AppealStatus: {0}".format(data_object.AppealStatus))
    output_status_message("Reasons (Element Name):")
    output_array_of_editorialreason(data_object.Reasons)

def output_array_of_editorialreasoncollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of EditorialReasonCollection:\n")
    for data_object in data_objects['EditorialReasonCollection']:
        output_editorialreasoncollection(data_object)
        output_status_message("\n")

def output_enhancedcpcbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("EnhancedCpcBiddingScheme (Data Object):")

def output_array_of_enhancedcpcbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of EnhancedCpcBiddingScheme:\n")
    for data_object in data_objects['EnhancedCpcBiddingScheme']:
        output_enhancedcpcbiddingscheme(data_object)
        output_status_message("\n")

def output_entityidtoparentidassociation(data_object):
    if data_object is None:
        return
    output_status_message("EntityIdToParentIdAssociation (Data Object):")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("ParentId: {0}".format(data_object.ParentId))

def output_array_of_entityidtoparentidassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of EntityIdToParentIdAssociation:\n")
    for data_object in data_objects['EntityIdToParentIdAssociation']:
        output_entityidtoparentidassociation(data_object)
        output_status_message("\n")

def output_entitynegativekeyword(data_object):
    if data_object is None:
        return
    output_status_message("EntityNegativeKeyword (Data Object):")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("EntityType: {0}".format(data_object.EntityType))
    output_status_message("NegativeKeywords (Element Name):")
    output_array_of_negativekeyword(data_object.NegativeKeywords)

def output_array_of_entitynegativekeyword(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of EntityNegativeKeyword:\n")
    for data_object in data_objects['EntityNegativeKeyword']:
        output_entitynegativekeyword(data_object)
        output_status_message("\n")

def output_eventgoal(data_object):
    if data_object is None:
        return
    output_status_message("EventGoal (Data Object):")
    output_status_message("ActionExpression: {0}".format(data_object.ActionExpression))
    output_status_message("ActionOperator: {0}".format(data_object.ActionOperator))
    output_status_message("CategoryExpression: {0}".format(data_object.CategoryExpression))
    output_status_message("CategoryOperator: {0}".format(data_object.CategoryOperator))
    output_status_message("LabelExpression: {0}".format(data_object.LabelExpression))
    output_status_message("LabelOperator: {0}".format(data_object.LabelOperator))
    output_status_message("Value: {0}".format(data_object.Value))
    output_status_message("ValueOperator: {0}".format(data_object.ValueOperator))

def output_array_of_eventgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of EventGoal:\n")
    for data_object in data_objects['EventGoal']:
        output_eventgoal(data_object)
        output_status_message("\n")

def output_expandedtextad(data_object):
    if data_object is None:
        return
    output_status_message("ExpandedTextAd (Data Object):")
    output_status_message("DisplayUrl: {0}".format(data_object.DisplayUrl))
    output_status_message("Path1: {0}".format(data_object.Path1))
    output_status_message("Path2: {0}".format(data_object.Path2))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("TitlePart1: {0}".format(data_object.TitlePart1))
    output_status_message("TitlePart2: {0}".format(data_object.TitlePart2))

def output_array_of_expandedtextad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ExpandedTextAd:\n")
    for data_object in data_objects['ExpandedTextAd']:
        output_expandedtextad(data_object)
        output_status_message("\n")

def output_fixedbid(data_object):
    if data_object is None:
        return
    output_status_message("FixedBid (Data Object):")
    output_status_message("Amount: {0}".format(data_object.Amount))

def output_array_of_fixedbid(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of FixedBid:\n")
    for data_object in data_objects['FixedBid']:
        output_fixedbid(data_object)
        output_status_message("\n")

def output_gendercriterion(data_object):
    if data_object is None:
        return
    output_status_message("GenderCriterion (Data Object):")
    output_status_message("GenderType: {0}".format(data_object.GenderType))

def output_array_of_gendercriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of GenderCriterion:\n")
    for data_object in data_objects['GenderCriterion']:
        output_gendercriterion(data_object)
        output_status_message("\n")

def output_geopoint(data_object):
    if data_object is None:
        return
    output_status_message("GeoPoint (Data Object):")
    output_status_message("LatitudeInMicroDegrees: {0}".format(data_object.LatitudeInMicroDegrees))
    output_status_message("LongitudeInMicroDegrees: {0}".format(data_object.LongitudeInMicroDegrees))

def output_array_of_geopoint(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of GeoPoint:\n")
    for data_object in data_objects['GeoPoint']:
        output_geopoint(data_object)
        output_status_message("\n")

def output_idcollection(data_object):
    if data_object is None:
        return
    output_status_message("IdCollection (Data Object):")
    output_status_message("Ids (Element Name):")
    output_array_of_long(data_object.Ids)

def output_array_of_idcollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of IdCollection:\n")
    for data_object in data_objects['IdCollection']:
        output_idcollection(data_object)
        output_status_message("\n")

def output_image(data_object):
    if data_object is None:
        return
    output_status_message("Image (Data Object):")
    output_status_message("Data: {0}".format(data_object.Data))

def output_array_of_image(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Image:\n")
    for data_object in data_objects['Image']:
        output_image(data_object)
        output_status_message("\n")

def output_imageadextension(data_object):
    if data_object is None:
        return
    output_status_message("ImageAdExtension (Data Object):")
    output_status_message("AlternativeText: {0}".format(data_object.AlternativeText))
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("FinalAppUrls (Element Name):")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls (Element Name):")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrls (Element Name):")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("ImageMediaIds (Element Name):")
    output_array_of_long(data_object.ImageMediaIds)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)

def output_array_of_imageadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ImageAdExtension:\n")
    for data_object in data_objects['ImageAdExtension']:
        output_imageadextension(data_object)
        output_status_message("\n")

def output_imagemediarepresentation(data_object):
    if data_object is None:
        return
    output_status_message("ImageMediaRepresentation (Data Object):")
    output_status_message("Height: {0}".format(data_object.Height))
    output_status_message("Width: {0}".format(data_object.Width))

def output_array_of_imagemediarepresentation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ImageMediaRepresentation:\n")
    for data_object in data_objects['ImageMediaRepresentation']:
        output_imagemediarepresentation(data_object)
        output_status_message("\n")

def output_inheritfromparentbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("InheritFromParentBiddingScheme (Data Object):")
    output_status_message("InheritedBidStrategyType: {0}".format(data_object.InheritedBidStrategyType))

def output_array_of_inheritfromparentbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of InheritFromParentBiddingScheme:\n")
    for data_object in data_objects['InheritFromParentBiddingScheme']:
        output_inheritfromparentbiddingscheme(data_object)
        output_status_message("\n")

def output_inmarketaudience(data_object):
    if data_object is None:
        return
    output_status_message("InMarketAudience (Data Object):")

def output_array_of_inmarketaudience(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of InMarketAudience:\n")
    for data_object in data_objects['InMarketAudience']:
        output_inmarketaudience(data_object)
        output_status_message("\n")

def output_instoretransactiongoal(data_object):
    if data_object is None:
        return
    output_status_message("InStoreTransactionGoal (Data Object):")

def output_array_of_instoretransactiongoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of InStoreTransactionGoal:\n")
    for data_object in data_objects['InStoreTransactionGoal']:
        output_instoretransactiongoal(data_object)
        output_status_message("\n")

def output_keyvaluepairofstringstring(data_object):
    if data_object is None:
        return
    output_status_message("KeyValuePairOfstringstring (Data Object):")
    output_status_message("key: {0}".format(data_object.key))
    output_status_message("value: {0}".format(data_object.value))

def output_array_of_keyvaluepairofstringstring(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of KeyValuePairOfstringstring:\n")
    for data_object in data_objects['KeyValuePairOfstringstring']:
        output_keyvaluepairofstringstring(data_object)
        output_status_message("\n")

def output_keyword(data_object):
    if data_object is None:
        return
    output_status_message("Keyword (Data Object):")
    output_status_message("Bid (Element Name):")
    output_bid(data_object.Bid)
    output_status_message("BiddingScheme (Element Name):")
    output_biddingscheme(data_object.BiddingScheme)
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("EditorialStatus: {0}".format(data_object.EditorialStatus))
    output_status_message("FinalAppUrls (Element Name):")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls (Element Name):")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrls (Element Name):")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("Param1: {0}".format(data_object.Param1))
    output_status_message("Param2: {0}".format(data_object.Param2))
    output_status_message("Param3: {0}".format(data_object.Param3))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)

def output_array_of_keyword(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Keyword:\n")
    for data_object in data_objects['Keyword']:
        output_keyword(data_object)
        output_status_message("\n")

def output_label(data_object):
    if data_object is None:
        return
    output_status_message("Label (Data Object):")
    output_status_message("ColorCode: {0}".format(data_object.ColorCode))
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))

def output_array_of_label(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Label:\n")
    for data_object in data_objects['Label']:
        output_label(data_object)
        output_status_message("\n")

def output_labelassociation(data_object):
    if data_object is None:
        return
    output_status_message("LabelAssociation (Data Object):")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("LabelId: {0}".format(data_object.LabelId))

def output_array_of_labelassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of LabelAssociation:\n")
    for data_object in data_objects['LabelAssociation']:
        output_labelassociation(data_object)
        output_status_message("\n")

def output_locationadextension(data_object):
    if data_object is None:
        return
    output_status_message("LocationAdExtension (Data Object):")
    output_status_message("Address (Element Name):")
    output_address(data_object.Address)
    output_status_message("CompanyName: {0}".format(data_object.CompanyName))
    output_status_message("GeoCodeStatus: {0}".format(data_object.GeoCodeStatus))
    output_status_message("GeoPoint (Element Name):")
    output_geopoint(data_object.GeoPoint)
    output_status_message("IconMediaId: {0}".format(data_object.IconMediaId))
    output_status_message("ImageMediaId: {0}".format(data_object.ImageMediaId))
    output_status_message("PhoneNumber: {0}".format(data_object.PhoneNumber))

def output_array_of_locationadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of LocationAdExtension:\n")
    for data_object in data_objects['LocationAdExtension']:
        output_locationadextension(data_object)
        output_status_message("\n")

def output_locationcriterion(data_object):
    if data_object is None:
        return
    output_status_message("LocationCriterion (Data Object):")
    output_status_message("DisplayName: {0}".format(data_object.DisplayName))
    output_status_message("EnclosedLocationIds (Element Name):")
    output_array_of_long(data_object.EnclosedLocationIds)
    output_status_message("LocationId: {0}".format(data_object.LocationId))
    output_status_message("LocationType: {0}".format(data_object.LocationType))

def output_array_of_locationcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of LocationCriterion:\n")
    for data_object in data_objects['LocationCriterion']:
        output_locationcriterion(data_object)
        output_status_message("\n")

def output_locationintentcriterion(data_object):
    if data_object is None:
        return
    output_status_message("LocationIntentCriterion (Data Object):")
    output_status_message("IntentOption: {0}".format(data_object.IntentOption))

def output_array_of_locationintentcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of LocationIntentCriterion:\n")
    for data_object in data_objects['LocationIntentCriterion']:
        output_locationintentcriterion(data_object)
        output_status_message("\n")

def output_manualcpcbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("ManualCpcBiddingScheme (Data Object):")

def output_array_of_manualcpcbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ManualCpcBiddingScheme:\n")
    for data_object in data_objects['ManualCpcBiddingScheme']:
        output_manualcpcbiddingscheme(data_object)
        output_status_message("\n")

def output_maxclicksbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("MaxClicksBiddingScheme (Data Object):")
    output_status_message("MaxCpc (Element Name):")
    output_bid(data_object.MaxCpc)

def output_array_of_maxclicksbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of MaxClicksBiddingScheme:\n")
    for data_object in data_objects['MaxClicksBiddingScheme']:
        output_maxclicksbiddingscheme(data_object)
        output_status_message("\n")

def output_maxconversionsbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("MaxConversionsBiddingScheme (Data Object):")
    output_status_message("MaxCpc (Element Name):")
    output_bid(data_object.MaxCpc)

def output_array_of_maxconversionsbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of MaxConversionsBiddingScheme:\n")
    for data_object in data_objects['MaxConversionsBiddingScheme']:
        output_maxconversionsbiddingscheme(data_object)
        output_status_message("\n")

def output_media(data_object):
    if data_object is None:
        return
    output_status_message("Media (Data Object):")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MediaType: {0}".format(data_object.MediaType))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.MediaType == 'Image':
        output_image(data_object)

def output_array_of_media(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Media:\n")
    for data_object in data_objects['Media']:
        output_media(data_object)
        output_status_message("\n")

def output_mediaassociation(data_object):
    if data_object is None:
        return
    output_status_message("MediaAssociation (Data Object):")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("MediaEnabledEntity: {0}".format(data_object.MediaEnabledEntity))
    output_status_message("MediaId: {0}".format(data_object.MediaId))

def output_array_of_mediaassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of MediaAssociation:\n")
    for data_object in data_objects['MediaAssociation']:
        output_mediaassociation(data_object)
        output_status_message("\n")

def output_mediametadata(data_object):
    if data_object is None:
        return
    output_status_message("MediaMetaData (Data Object):")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MediaType: {0}".format(data_object.MediaType))
    output_status_message("Representations (Element Name):")
    output_array_of_mediarepresentation(data_object.Representations)
    output_status_message("Type: {0}".format(data_object.Type))

def output_array_of_mediametadata(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of MediaMetaData:\n")
    for data_object in data_objects['MediaMetaData']:
        output_mediametadata(data_object)
        output_status_message("\n")

def output_mediarepresentation(data_object):
    if data_object is None:
        return
    output_status_message("MediaRepresentation (Data Object):")
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("Url: {0}".format(data_object.Url))
    if data_object.Type == 'ImageMediaRepresentation':
        output_imagemediarepresentation(data_object)

def output_array_of_mediarepresentation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of MediaRepresentation:\n")
    for data_object in data_objects['MediaRepresentation']:
        output_mediarepresentation(data_object)
        output_status_message("\n")

def output_migrationstatusinfo(data_object):
    if data_object is None:
        return
    output_status_message("MigrationStatusInfo (Data Object):")
    output_status_message("MigrationType: {0}".format(data_object.MigrationType))
    output_status_message("StartTimeInUtc: {0}".format(data_object.StartTimeInUtc))
    output_status_message("Status: {0}".format(data_object.Status))

def output_array_of_migrationstatusinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of MigrationStatusInfo:\n")
    for data_object in data_objects['MigrationStatusInfo']:
        output_migrationstatusinfo(data_object)
        output_status_message("\n")

def output_negativeadgroupcriterion(data_object):
    if data_object is None:
        return
    output_status_message("NegativeAdGroupCriterion (Data Object):")

def output_array_of_negativeadgroupcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of NegativeAdGroupCriterion:\n")
    for data_object in data_objects['NegativeAdGroupCriterion']:
        output_negativeadgroupcriterion(data_object)
        output_status_message("\n")

def output_negativecampaigncriterion(data_object):
    if data_object is None:
        return
    output_status_message("NegativeCampaignCriterion (Data Object):")

def output_array_of_negativecampaigncriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of NegativeCampaignCriterion:\n")
    for data_object in data_objects['NegativeCampaignCriterion']:
        output_negativecampaigncriterion(data_object)
        output_status_message("\n")

def output_negativekeyword(data_object):
    if data_object is None:
        return
    output_status_message("NegativeKeyword (Data Object):")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("Text: {0}".format(data_object.Text))

def output_array_of_negativekeyword(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of NegativeKeyword:\n")
    for data_object in data_objects['NegativeKeyword']:
        output_negativekeyword(data_object)
        output_status_message("\n")

def output_negativekeywordlist(data_object):
    if data_object is None:
        return
    output_status_message("NegativeKeywordList (Data Object):")

def output_array_of_negativekeywordlist(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of NegativeKeywordList:\n")
    for data_object in data_objects['NegativeKeywordList']:
        output_negativekeywordlist(data_object)
        output_status_message("\n")

def output_offlineconversion(data_object):
    if data_object is None:
        return
    output_status_message("OfflineConversion (Data Object):")
    output_status_message("ConversionCurrencyCode: {0}".format(data_object.ConversionCurrencyCode))
    output_status_message("ConversionName: {0}".format(data_object.ConversionName))
    output_status_message("ConversionTime: {0}".format(data_object.ConversionTime))
    output_status_message("ConversionValue: {0}".format(data_object.ConversionValue))
    output_status_message("MicrosoftClickId: {0}".format(data_object.MicrosoftClickId))

def output_array_of_offlineconversion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of OfflineConversion:\n")
    for data_object in data_objects['OfflineConversion']:
        output_offlineconversion(data_object)
        output_status_message("\n")

def output_offlineconversiongoal(data_object):
    if data_object is None:
        return
    output_status_message("OfflineConversionGoal (Data Object):")

def output_array_of_offlineconversiongoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of OfflineConversionGoal:\n")
    for data_object in data_objects['OfflineConversionGoal']:
        output_offlineconversiongoal(data_object)
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

def output_pagesviewedpervisitgoal(data_object):
    if data_object is None:
        return
    output_status_message("PagesViewedPerVisitGoal (Data Object):")
    output_status_message("MinimumPagesViewed: {0}".format(data_object.MinimumPagesViewed))

def output_array_of_pagesviewedpervisitgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of PagesViewedPerVisitGoal:\n")
    for data_object in data_objects['PagesViewedPerVisitGoal']:
        output_pagesviewedpervisitgoal(data_object)
        output_status_message("\n")

def output_pagevisitorsrule(data_object):
    if data_object is None:
        return
    output_status_message("PageVisitorsRule (Data Object):")
    output_status_message("RuleItemGroups (Element Name):")
    output_array_of_ruleitemgroup(data_object.RuleItemGroups)

def output_array_of_pagevisitorsrule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of PageVisitorsRule:\n")
    for data_object in data_objects['PageVisitorsRule']:
        output_pagevisitorsrule(data_object)
        output_status_message("\n")

def output_pagevisitorswhodidnotvisitanotherpagerule(data_object):
    if data_object is None:
        return
    output_status_message("PageVisitorsWhoDidNotVisitAnotherPageRule (Data Object):")
    output_status_message("ExcludeRuleItemGroups (Element Name):")
    output_array_of_ruleitemgroup(data_object.ExcludeRuleItemGroups)
    output_status_message("IncludeRuleItemGroups (Element Name):")
    output_array_of_ruleitemgroup(data_object.IncludeRuleItemGroups)

def output_array_of_pagevisitorswhodidnotvisitanotherpagerule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of PageVisitorsWhoDidNotVisitAnotherPageRule:\n")
    for data_object in data_objects['PageVisitorsWhoDidNotVisitAnotherPageRule']:
        output_pagevisitorswhodidnotvisitanotherpagerule(data_object)
        output_status_message("\n")

def output_pagevisitorswhovisitedanotherpagerule(data_object):
    if data_object is None:
        return
    output_status_message("PageVisitorsWhoVisitedAnotherPageRule (Data Object):")
    output_status_message("AnotherRuleItemGroups (Element Name):")
    output_array_of_ruleitemgroup(data_object.AnotherRuleItemGroups)
    output_status_message("RuleItemGroups (Element Name):")
    output_array_of_ruleitemgroup(data_object.RuleItemGroups)

def output_array_of_pagevisitorswhovisitedanotherpagerule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of PageVisitorsWhoVisitedAnotherPageRule:\n")
    for data_object in data_objects['PageVisitorsWhoVisitedAnotherPageRule']:
        output_pagevisitorswhovisitedanotherpagerule(data_object)
        output_status_message("\n")

def output_paging(data_object):
    if data_object is None:
        return
    output_status_message("Paging (Data Object):")
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Size: {0}".format(data_object.Size))

def output_array_of_paging(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Paging:\n")
    for data_object in data_objects['Paging']:
        output_paging(data_object)
        output_status_message("\n")

def output_priceadextension(data_object):
    if data_object is None:
        return
    output_status_message("PriceAdExtension (Data Object):")
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("PriceExtensionType: {0}".format(data_object.PriceExtensionType))
    output_status_message("TableRows (Element Name):")
    output_array_of_pricetablerow(data_object.TableRows)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)

def output_array_of_priceadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of PriceAdExtension:\n")
    for data_object in data_objects['PriceAdExtension']:
        output_priceadextension(data_object)
        output_status_message("\n")

def output_pricetablerow(data_object):
    if data_object is None:
        return
    output_status_message("PriceTableRow (Data Object):")
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("FinalMobileUrls (Element Name):")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrls (Element Name):")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("Header: {0}".format(data_object.Header))
    output_status_message("Price: {0}".format(data_object.Price))
    output_status_message("PriceQualifier: {0}".format(data_object.PriceQualifier))
    output_status_message("PriceUnit: {0}".format(data_object.PriceUnit))
    output_status_message("TermsAndConditions: {0}".format(data_object.TermsAndConditions))
    output_status_message("TermsAndConditionsUrl: {0}".format(data_object.TermsAndConditionsUrl))

def output_array_of_pricetablerow(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of PriceTableRow:\n")
    for data_object in data_objects['PriceTableRow']:
        output_pricetablerow(data_object)
        output_status_message("\n")

def output_productad(data_object):
    if data_object is None:
        return
    output_status_message("ProductAd (Data Object):")
    output_status_message("PromotionalText: {0}".format(data_object.PromotionalText))

def output_array_of_productad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductAd:\n")
    for data_object in data_objects['ProductAd']:
        output_productad(data_object)
        output_status_message("\n")

def output_productcondition(data_object):
    if data_object is None:
        return
    output_status_message("ProductCondition (Data Object):")
    output_status_message("Attribute: {0}".format(data_object.Attribute))
    output_status_message("Operand: {0}".format(data_object.Operand))

def output_array_of_productcondition(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductCondition:\n")
    for data_object in data_objects['ProductCondition']:
        output_productcondition(data_object)
        output_status_message("\n")

def output_productpartition(data_object):
    if data_object is None:
        return
    output_status_message("ProductPartition (Data Object):")
    output_status_message("Condition (Element Name):")
    output_productcondition(data_object.Condition)
    output_status_message("ParentCriterionId: {0}".format(data_object.ParentCriterionId))
    output_status_message("PartitionType: {0}".format(data_object.PartitionType))

def output_array_of_productpartition(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductPartition:\n")
    for data_object in data_objects['ProductPartition']:
        output_productpartition(data_object)
        output_status_message("\n")

def output_productscope(data_object):
    if data_object is None:
        return
    output_status_message("ProductScope (Data Object):")
    output_status_message("Conditions (Element Name):")
    output_array_of_productcondition(data_object.Conditions)

def output_array_of_productscope(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ProductScope:\n")
    for data_object in data_objects['ProductScope']:
        output_productscope(data_object)
        output_status_message("\n")

def output_radiuscriterion(data_object):
    if data_object is None:
        return
    output_status_message("RadiusCriterion (Data Object):")
    output_status_message("LatitudeDegrees: {0}".format(data_object.LatitudeDegrees))
    output_status_message("LongitudeDegrees: {0}".format(data_object.LongitudeDegrees))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Radius: {0}".format(data_object.Radius))
    output_status_message("RadiusUnit: {0}".format(data_object.RadiusUnit))

def output_array_of_radiuscriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of RadiusCriterion:\n")
    for data_object in data_objects['RadiusCriterion']:
        output_radiuscriterion(data_object)
        output_status_message("\n")

def output_remarketinglist(data_object):
    if data_object is None:
        return
    output_status_message("RemarketingList (Data Object):")
    output_status_message("Rule (Element Name):")
    output_remarketingrule(data_object.Rule)
    output_status_message("TagId: {0}".format(data_object.TagId))

def output_array_of_remarketinglist(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of RemarketingList:\n")
    for data_object in data_objects['RemarketingList']:
        output_remarketinglist(data_object)
        output_status_message("\n")

def output_remarketingrule(data_object):
    if data_object is None:
        return
    output_status_message("RemarketingRule (Data Object):")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'CustomEventsRule':
        output_customeventsrule(data_object)
    if data_object.Type == 'PageVisitorsRule':
        output_pagevisitorsrule(data_object)
    if data_object.Type == 'PageVisitorsWhoDidNotVisitAnotherPageRule':
        output_pagevisitorswhodidnotvisitanotherpagerule(data_object)
    if data_object.Type == 'PageVisitorsWhoVisitedAnotherPageRule':
        output_pagevisitorswhovisitedanotherpagerule(data_object)

def output_array_of_remarketingrule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of RemarketingRule:\n")
    for data_object in data_objects['RemarketingRule']:
        output_remarketingrule(data_object)
        output_status_message("\n")

def output_reviewadextension(data_object):
    if data_object is None:
        return
    output_status_message("ReviewAdExtension (Data Object):")
    output_status_message("IsExact: {0}".format(data_object.IsExact))
    output_status_message("Source: {0}".format(data_object.Source))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("Url: {0}".format(data_object.Url))

def output_array_of_reviewadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ReviewAdExtension:\n")
    for data_object in data_objects['ReviewAdExtension']:
        output_reviewadextension(data_object)
        output_status_message("\n")

def output_ruleitem(data_object):
    if data_object is None:
        return
    output_status_message("RuleItem (Data Object):")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'StringRuleItem':
        output_stringruleitem(data_object)

def output_array_of_ruleitem(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of RuleItem:\n")
    for data_object in data_objects['RuleItem']:
        output_ruleitem(data_object)
        output_status_message("\n")

def output_ruleitemgroup(data_object):
    if data_object is None:
        return
    output_status_message("RuleItemGroup (Data Object):")
    output_status_message("Items (Element Name):")
    output_array_of_ruleitem(data_object.Items)

def output_array_of_ruleitemgroup(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of RuleItemGroup:\n")
    for data_object in data_objects['RuleItemGroup']:
        output_ruleitemgroup(data_object)
        output_status_message("\n")

def output_schedule(data_object):
    if data_object is None:
        return
    output_status_message("Schedule (Data Object):")
    output_status_message("DayTimeRanges (Element Name):")
    output_array_of_daytime(data_object.DayTimeRanges)
    output_status_message("EndDate (Element Name):")
    output_date(data_object.EndDate)
    output_status_message("StartDate (Element Name):")
    output_date(data_object.StartDate)
    output_status_message("UseSearcherTimeZone: {0}".format(data_object.UseSearcherTimeZone))

def output_array_of_schedule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Schedule:\n")
    for data_object in data_objects['Schedule']:
        output_schedule(data_object)
        output_status_message("\n")

def output_setting(data_object):
    if data_object is None:
        return
    output_status_message("Setting (Data Object):")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'DynamicSearchAdsSetting':
        output_dynamicsearchadssetting(data_object)
    if data_object.Type == 'ShoppingSetting':
        output_shoppingsetting(data_object)

def output_array_of_setting(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Setting:\n")
    for data_object in data_objects['Setting']:
        output_setting(data_object)
        output_status_message("\n")

def output_sharedentity(data_object):
    if data_object is None:
        return
    output_status_message("SharedEntity (Data Object):")
    output_status_message("AssociationCount: {0}".format(data_object.AssociationCount))
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'SharedList':
        output_sharedlist(data_object)

def output_array_of_sharedentity(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SharedEntity:\n")
    for data_object in data_objects['SharedEntity']:
        output_sharedentity(data_object)
        output_status_message("\n")

def output_sharedentityassociation(data_object):
    if data_object is None:
        return
    output_status_message("SharedEntityAssociation (Data Object):")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("EntityType: {0}".format(data_object.EntityType))
    output_status_message("SharedEntityId: {0}".format(data_object.SharedEntityId))
    output_status_message("SharedEntityType: {0}".format(data_object.SharedEntityType))

def output_array_of_sharedentityassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SharedEntityAssociation:\n")
    for data_object in data_objects['SharedEntityAssociation']:
        output_sharedentityassociation(data_object)
        output_status_message("\n")

def output_sharedlist(data_object):
    if data_object is None:
        return
    output_status_message("SharedList (Data Object):")
    output_status_message("ItemCount: {0}".format(data_object.ItemCount))
    if data_object.Type == 'NegativeKeywordList':
        output_negativekeywordlist(data_object)

def output_array_of_sharedlist(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SharedList:\n")
    for data_object in data_objects['SharedList']:
        output_sharedlist(data_object)
        output_status_message("\n")

def output_sharedlistitem(data_object):
    if data_object is None:
        return
    output_status_message("SharedListItem (Data Object):")
    output_status_message("ForwardCompatibilityMap (Element Name):")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'NegativeKeyword':
        output_negativekeyword(data_object)

def output_array_of_sharedlistitem(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SharedListItem:\n")
    for data_object in data_objects['SharedListItem']:
        output_sharedlistitem(data_object)
        output_status_message("\n")

def output_shoppingsetting(data_object):
    if data_object is None:
        return
    output_status_message("ShoppingSetting (Data Object):")
    output_status_message("LocalInventoryAdsEnabled: {0}".format(data_object.LocalInventoryAdsEnabled))
    output_status_message("Priority: {0}".format(data_object.Priority))
    output_status_message("SalesCountryCode: {0}".format(data_object.SalesCountryCode))
    output_status_message("StoreId: {0}".format(data_object.StoreId))

def output_array_of_shoppingsetting(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ShoppingSetting:\n")
    for data_object in data_objects['ShoppingSetting']:
        output_shoppingsetting(data_object)
        output_status_message("\n")

def output_sitelink(data_object):
    if data_object is None:
        return
    output_status_message("SiteLink (Data Object):")
    output_status_message("Description1: {0}".format(data_object.Description1))
    output_status_message("Description2: {0}".format(data_object.Description2))
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("DevicePreference: {0}".format(data_object.DevicePreference))
    output_status_message("DisplayText: {0}".format(data_object.DisplayText))
    output_status_message("FinalAppUrls (Element Name):")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls (Element Name):")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrls (Element Name):")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("Scheduling (Element Name):")
    output_schedule(data_object.Scheduling)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)

def output_array_of_sitelink(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SiteLink:\n")
    for data_object in data_objects['SiteLink']:
        output_sitelink(data_object)
        output_status_message("\n")

def output_sitelink2adextension(data_object):
    if data_object is None:
        return
    output_status_message("Sitelink2AdExtension (Data Object):")
    output_status_message("Description1: {0}".format(data_object.Description1))
    output_status_message("Description2: {0}".format(data_object.Description2))
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("DisplayText: {0}".format(data_object.DisplayText))
    output_status_message("FinalAppUrls (Element Name):")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls (Element Name):")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrls (Element Name):")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters (Element Name):")
    output_customparameters(data_object.UrlCustomParameters)

def output_array_of_sitelink2adextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Sitelink2AdExtension:\n")
    for data_object in data_objects['Sitelink2AdExtension']:
        output_sitelink2adextension(data_object)
        output_status_message("\n")

def output_sitelinksadextension(data_object):
    if data_object is None:
        return
    output_status_message("SiteLinksAdExtension (Data Object):")
    output_status_message("SiteLinks (Element Name):")
    output_array_of_sitelink(data_object.SiteLinks)

def output_array_of_sitelinksadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of SiteLinksAdExtension:\n")
    for data_object in data_objects['SiteLinksAdExtension']:
        output_sitelinksadextension(data_object)
        output_status_message("\n")

def output_stringruleitem(data_object):
    if data_object is None:
        return
    output_status_message("StringRuleItem (Data Object):")
    output_status_message("Operand: {0}".format(data_object.Operand))
    output_status_message("Operator: {0}".format(data_object.Operator))
    output_status_message("Value: {0}".format(data_object.Value))

def output_array_of_stringruleitem(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of StringRuleItem:\n")
    for data_object in data_objects['StringRuleItem']:
        output_stringruleitem(data_object)
        output_status_message("\n")

def output_structuredsnippetadextension(data_object):
    if data_object is None:
        return
    output_status_message("StructuredSnippetAdExtension (Data Object):")
    output_status_message("Header: {0}".format(data_object.Header))
    output_status_message("Values (Element Name):")
    output_array_of_string(data_object.Values)

def output_array_of_structuredsnippetadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of StructuredSnippetAdExtension:\n")
    for data_object in data_objects['StructuredSnippetAdExtension']:
        output_structuredsnippetadextension(data_object)
        output_status_message("\n")

def output_targetcpabiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("TargetCpaBiddingScheme (Data Object):")
    output_status_message("MaxCpc (Element Name):")
    output_bid(data_object.MaxCpc)
    output_status_message("TargetCpa: {0}".format(data_object.TargetCpa))

def output_array_of_targetcpabiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of TargetCpaBiddingScheme:\n")
    for data_object in data_objects['TargetCpaBiddingScheme']:
        output_targetcpabiddingscheme(data_object)
        output_status_message("\n")

def output_textad(data_object):
    if data_object is None:
        return
    output_status_message("TextAd (Data Object):")
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("DisplayUrl: {0}".format(data_object.DisplayUrl))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("Title: {0}".format(data_object.Title))

def output_array_of_textad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of TextAd:\n")
    for data_object in data_objects['TextAd']:
        output_textad(data_object)
        output_status_message("\n")

def output_uettag(data_object):
    if data_object is None:
        return
    output_status_message("UetTag (Data Object):")
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("TrackingNoScript: {0}".format(data_object.TrackingNoScript))
    output_status_message("TrackingScript: {0}".format(data_object.TrackingScript))
    output_status_message("TrackingStatus: {0}".format(data_object.TrackingStatus))

def output_array_of_uettag(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of UetTag:\n")
    for data_object in data_objects['UetTag']:
        output_uettag(data_object)
        output_status_message("\n")

def output_urlgoal(data_object):
    if data_object is None:
        return
    output_status_message("UrlGoal (Data Object):")
    output_status_message("UrlExpression: {0}".format(data_object.UrlExpression))
    output_status_message("UrlOperator: {0}".format(data_object.UrlOperator))

def output_array_of_urlgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of UrlGoal:\n")
    for data_object in data_objects['UrlGoal']:
        output_urlgoal(data_object)
        output_status_message("\n")

def output_webpage(data_object):
    if data_object is None:
        return
    output_status_message("Webpage (Data Object):")
    output_status_message("Parameter (Element Name):")
    output_webpageparameter(data_object.Parameter)

def output_array_of_webpage(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Webpage:\n")
    for data_object in data_objects['Webpage']:
        output_webpage(data_object)
        output_status_message("\n")

def output_webpagecondition(data_object):
    if data_object is None:
        return
    output_status_message("WebpageCondition (Data Object):")
    output_status_message("Argument: {0}".format(data_object.Argument))
    output_status_message("Operand: {0}".format(data_object.Operand))

def output_array_of_webpagecondition(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of WebpageCondition:\n")
    for data_object in data_objects['WebpageCondition']:
        output_webpagecondition(data_object)
        output_status_message("\n")

def output_webpageparameter(data_object):
    if data_object is None:
        return
    output_status_message("WebpageParameter (Data Object):")
    output_status_message("Conditions (Element Name):")
    output_array_of_webpagecondition(data_object.Conditions)
    output_status_message("CriterionName: {0}".format(data_object.CriterionName))

def output_array_of_webpageparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of WebpageParameter:\n")
    for data_object in data_objects['WebpageParameter']:
        output_webpageparameter(data_object)
        output_status_message("\n")

def output_adeditorialstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adeditorialstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdEditorialStatus:\n")
    for value_set in value_sets['AdEditorialStatus']:
        output_adeditorialstatus(value_set)

def output_adstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdStatus:\n")
    for value_set in value_sets['AdStatus']:
        output_adstatus(value_set)

def output_adtype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adtype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdType:\n")
    for value_set in value_sets['AdType']:
        output_adtype(value_set)

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

def output_campaignstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_campaignstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CampaignStatus:\n")
    for value_set in value_sets['CampaignStatus']:
        output_campaignstatus(value_set)

def output_campaigntype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_campaigntype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CampaignType:\n")
    for value_set in value_sets['CampaignType']:
        output_campaigntype(value_set)

def output_addistribution(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_addistribution(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdDistribution:\n")
    for value_set in value_sets['AdDistribution']:
        output_addistribution(value_set)

def output_adrotationtype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adrotationtype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdRotationType:\n")
    for value_set in value_sets['AdRotationType']:
        output_adrotationtype(value_set)

def output_network(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_network(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of Network:\n")
    for value_set in value_sets['Network']:
        output_network(value_set)

def output_pricingmodel(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_pricingmodel(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of PricingModel:\n")
    for value_set in value_sets['PricingModel']:
        output_pricingmodel(value_set)

def output_remarketingtargetingsetting(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_remarketingtargetingsetting(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of RemarketingTargetingSetting:\n")
    for value_set in value_sets['RemarketingTargetingSetting']:
        output_remarketingtargetingsetting(value_set)

def output_adgroupstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adgroupstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdGroupStatus:\n")
    for value_set in value_sets['AdGroupStatus']:
        output_adgroupstatus(value_set)

def output_adgroupadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adgroupadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdGroupAdditionalField:\n")
    for value_set in value_sets['AdGroupAdditionalField']:
        output_adgroupadditionalfield(value_set)

def output_keywordeditorialstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_keywordeditorialstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of KeywordEditorialStatus:\n")
    for value_set in value_sets['KeywordEditorialStatus']:
        output_keywordeditorialstatus(value_set)

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

def output_keywordstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_keywordstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of KeywordStatus:\n")
    for value_set in value_sets['KeywordStatus']:
        output_keywordstatus(value_set)

def output_keywordadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_keywordadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of KeywordAdditionalField:\n")
    for value_set in value_sets['KeywordAdditionalField']:
        output_keywordadditionalfield(value_set)

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

def output_appealstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_appealstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AppealStatus:\n")
    for value_set in value_sets['AppealStatus']:
        output_appealstatus(value_set)

def output_migrationstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_migrationstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of MigrationStatus:\n")
    for value_set in value_sets['MigrationStatus']:
        output_migrationstatus(value_set)

def output_accountpropertyname(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_accountpropertyname(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AccountPropertyName:\n")
    for value_set in value_sets['AccountPropertyName']:
        output_accountpropertyname(value_set)

def output_day(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_day(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of Day:\n")
    for value_set in value_sets['Day']:
        output_day(value_set)

def output_minute(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_minute(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of Minute:\n")
    for value_set in value_sets['Minute']:
        output_minute(value_set)

def output_adextensionstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adextensionstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdExtensionStatus:\n")
    for value_set in value_sets['AdExtensionStatus']:
        output_adextensionstatus(value_set)

def output_businessgeocodestatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_businessgeocodestatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BusinessGeoCodeStatus:\n")
    for value_set in value_sets['BusinessGeoCodeStatus']:
        output_businessgeocodestatus(value_set)

def output_priceextensiontype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_priceextensiontype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of PriceExtensionType:\n")
    for value_set in value_sets['PriceExtensionType']:
        output_priceextensiontype(value_set)

def output_pricequalifier(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_pricequalifier(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of PriceQualifier:\n")
    for value_set in value_sets['PriceQualifier']:
        output_pricequalifier(value_set)

def output_priceunit(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_priceunit(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of PriceUnit:\n")
    for value_set in value_sets['PriceUnit']:
        output_priceunit(value_set)

def output_adextensionstypefilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adextensionstypefilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdExtensionsTypeFilter:\n")
    for value_set in value_sets['AdExtensionsTypeFilter']:
        output_adextensionstypefilter(value_set)

def output_associationtype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_associationtype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AssociationType:\n")
    for value_set in value_sets['AssociationType']:
        output_associationtype(value_set)

def output_adextensioneditorialstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adextensioneditorialstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdExtensionEditorialStatus:\n")
    for value_set in value_sets['AdExtensionEditorialStatus']:
        output_adextensioneditorialstatus(value_set)

def output_mediaenabledentityfilter(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_mediaenabledentityfilter(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of MediaEnabledEntityFilter:\n")
    for value_set in value_sets['MediaEnabledEntityFilter']:
        output_mediaenabledentityfilter(value_set)

def output_adgroupcriteriontype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adgroupcriteriontype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdGroupCriterionType:\n")
    for value_set in value_sets['AdGroupCriterionType']:
        output_adgroupcriteriontype(value_set)

def output_productpartitiontype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_productpartitiontype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ProductPartitionType:\n")
    for value_set in value_sets['ProductPartitionType']:
        output_productpartitiontype(value_set)

def output_webpageconditionoperand(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_webpageconditionoperand(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of WebpageConditionOperand:\n")
    for value_set in value_sets['WebpageConditionOperand']:
        output_webpageconditionoperand(value_set)

def output_agerange(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_agerange(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AgeRange:\n")
    for value_set in value_sets['AgeRange']:
        output_agerange(value_set)

def output_gendertype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_gendertype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of GenderType:\n")
    for value_set in value_sets['GenderType']:
        output_gendertype(value_set)

def output_distanceunit(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_distanceunit(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DistanceUnit:\n")
    for value_set in value_sets['DistanceUnit']:
        output_distanceunit(value_set)

def output_intentoption(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_intentoption(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of IntentOption:\n")
    for value_set in value_sets['IntentOption']:
        output_intentoption(value_set)

def output_audiencetype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_audiencetype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AudienceType:\n")
    for value_set in value_sets['AudienceType']:
        output_audiencetype(value_set)

def output_adgroupcriterionstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adgroupcriterionstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdGroupCriterionStatus:\n")
    for value_set in value_sets['AdGroupCriterionStatus']:
        output_adgroupcriterionstatus(value_set)

def output_adgroupcriterioneditorialstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adgroupcriterioneditorialstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdGroupCriterionEditorialStatus:\n")
    for value_set in value_sets['AdGroupCriterionEditorialStatus']:
        output_adgroupcriterioneditorialstatus(value_set)

def output_itemaction(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_itemaction(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ItemAction:\n")
    for value_set in value_sets['ItemAction']:
        output_itemaction(value_set)

def output_campaigncriterionstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_campaigncriterionstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CampaignCriterionStatus:\n")
    for value_set in value_sets['CampaignCriterionStatus']:
        output_campaigncriterionstatus(value_set)

def output_campaigncriteriontype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_campaigncriteriontype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CampaignCriterionType:\n")
    for value_set in value_sets['CampaignCriterionType']:
        output_campaigncriteriontype(value_set)

def output_entityscope(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_entityscope(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of EntityScope:\n")
    for value_set in value_sets['EntityScope']:
        output_entityscope(value_set)

def output_stringoperator(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_stringoperator(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of StringOperator:\n")
    for value_set in value_sets['StringOperator']:
        output_stringoperator(value_set)

def output_numberoperator(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_numberoperator(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of NumberOperator:\n")
    for value_set in value_sets['NumberOperator']:
        output_numberoperator(value_set)

def output_audienceadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_audienceadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AudienceAdditionalField:\n")
    for value_set in value_sets['AudienceAdditionalField']:
        output_audienceadditionalfield(value_set)

def output_uettagtrackingstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_uettagtrackingstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of UetTagTrackingStatus:\n")
    for value_set in value_sets['UetTagTrackingStatus']:
        output_uettagtrackingstatus(value_set)

def output_conversiongoaltype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_conversiongoaltype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ConversionGoalType:\n")
    for value_set in value_sets['ConversionGoalType']:
        output_conversiongoaltype(value_set)

def output_conversiongoalcounttype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_conversiongoalcounttype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ConversionGoalCountType:\n")
    for value_set in value_sets['ConversionGoalCountType']:
        output_conversiongoalcounttype(value_set)

def output_conversiongoalrevenuetype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_conversiongoalrevenuetype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ConversionGoalRevenueType:\n")
    for value_set in value_sets['ConversionGoalRevenueType']:
        output_conversiongoalrevenuetype(value_set)

def output_conversiongoalstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_conversiongoalstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ConversionGoalStatus:\n")
    for value_set in value_sets['ConversionGoalStatus']:
        output_conversiongoalstatus(value_set)

def output_conversiongoaltrackingstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_conversiongoaltrackingstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ConversionGoalTrackingStatus:\n")
    for value_set in value_sets['ConversionGoalTrackingStatus']:
        output_conversiongoaltrackingstatus(value_set)

def output_expressionoperator(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_expressionoperator(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ExpressionOperator:\n")
    for value_set in value_sets['ExpressionOperator']:
        output_expressionoperator(value_set)

def output_valueoperator(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_valueoperator(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ValueOperator:\n")
    for value_set in value_sets['ValueOperator']:
        output_valueoperator(value_set)

def output_array_of_long(items):
    if items is None or len(items) == 0:
        return
    output_status_message("Array Of long:")
    for item in items['long']:
        output_status_message("Value of the long: {0}".format(item))
def output_array_of_string(items):
    if items is None or len(items) == 0:
        return
    output_status_message("Array Of string:")
    for item in items['string']:
        output_status_message("Value of the string: {0}".format(item))
def output_status_message(message):
    print(message)
