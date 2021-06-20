def output_accountmigrationstatusesinfo(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_accountmigrationstatusesinfo * * *")
    output_status_message("AccountId: {0}".format(data_object.AccountId))
    output_status_message("MigrationStatusInfos:")
    output_array_of_migrationstatusinfo(data_object.MigrationStatusInfos)
    output_status_message("* * * End output_accountmigrationstatusesinfo * * *")

def output_array_of_accountmigrationstatusesinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AccountMigrationStatusesInfo']:
        output_accountmigrationstatusesinfo(data_object)

def output_accountproperty(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_accountproperty * * *")
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Value: {0}".format(data_object.Value))
    output_status_message("* * * End output_accountproperty * * *")

def output_array_of_accountproperty(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AccountProperty']:
        output_accountproperty(data_object)

def output_actionadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_actionadextension * * *")
    output_status_message("ActionType: {0}".format(data_object.ActionType))
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("* * * End output_actionadextension * * *")

def output_array_of_actionadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ActionAdExtension']:
        output_actionadextension(data_object)

def output_ad(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_ad * * *")
    output_status_message("AdFormatPreference: {0}".format(data_object.AdFormatPreference))
    output_status_message("DevicePreference: {0}".format(data_object.DevicePreference))
    output_status_message("EditorialStatus: {0}".format(data_object.EditorialStatus))
    output_status_message("FinalAppUrls:")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    if data_object.Type == 'AppInstall':
        output_appinstallad(data_object)
    if data_object.Type == 'DynamicSearch':
        output_dynamicsearchad(data_object)
    if data_object.Type == 'ExpandedText':
        output_expandedtextad(data_object)
    if data_object.Type == 'Product':
        output_productad(data_object)
    if data_object.Type == 'ResponsiveAd':
        output_responsivead(data_object)
    if data_object.Type == 'ResponsiveSearch':
        output_responsivesearchad(data_object)
    if data_object.Type == 'Text':
        output_textad(data_object)
    output_status_message("* * * End output_ad * * *")

def output_array_of_ad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Ad']:
        output_ad(data_object)

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

def output_address(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_address * * *")
    output_status_message("CityName: {0}".format(data_object.CityName))
    output_status_message("CountryCode: {0}".format(data_object.CountryCode))
    output_status_message("PostalCode: {0}".format(data_object.PostalCode))
    output_status_message("ProvinceCode: {0}".format(data_object.ProvinceCode))
    output_status_message("ProvinceName: {0}".format(data_object.ProvinceName))
    output_status_message("StreetAddress: {0}".format(data_object.StreetAddress))
    output_status_message("StreetAddress2: {0}".format(data_object.StreetAddress2))
    output_status_message("* * * End output_address * * *")

def output_array_of_address(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Address']:
        output_address(data_object)

def output_adextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adextension * * *")
    output_status_message("DevicePreference: {0}".format(data_object.DevicePreference))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Scheduling:")
    output_schedule(data_object.Scheduling)
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("Version: {0}".format(data_object.Version))
    if data_object.Type == 'ActionAdExtension':
        output_actionadextension(data_object)
    if data_object.Type == 'AppAdExtension':
        output_appadextension(data_object)
    if data_object.Type == 'CallAdExtension':
        output_calladextension(data_object)
    if data_object.Type == 'CalloutAdExtension':
        output_calloutadextension(data_object)
    if data_object.Type == 'FilterLinkAdExtension':
        output_filterlinkadextension(data_object)
    if data_object.Type == 'FlyerAdExtension':
        output_flyeradextension(data_object)
    if data_object.Type == 'ImageAdExtension':
        output_imageadextension(data_object)
    if data_object.Type == 'LocationAdExtension':
        output_locationadextension(data_object)
    if data_object.Type == 'PriceAdExtension':
        output_priceadextension(data_object)
    if data_object.Type == 'PromotionAdExtension':
        output_promotionadextension(data_object)
    if data_object.Type == 'ReviewAdExtension':
        output_reviewadextension(data_object)
    if data_object.Type == 'SitelinkAdExtension':
        output_sitelinkadextension(data_object)
    if data_object.Type == 'StructuredSnippetAdExtension':
        output_structuredsnippetadextension(data_object)
    if data_object.Type == 'VideoAdExtension':
        output_videoadextension(data_object)
    output_status_message("* * * End output_adextension * * *")

def output_array_of_adextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdExtension']:
        output_adextension(data_object)

def output_adextensionassociation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adextensionassociation * * *")
    output_status_message("AdExtension:")
    output_adextension(data_object.AdExtension)
    output_status_message("AssociationType: {0}".format(data_object.AssociationType))
    output_status_message("EditorialStatus: {0}".format(data_object.EditorialStatus))
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("* * * End output_adextensionassociation * * *")

def output_array_of_adextensionassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdExtensionAssociation']:
        output_adextensionassociation(data_object)

def output_adextensionassociationcollection(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adextensionassociationcollection * * *")
    output_status_message("AdExtensionAssociations:")
    output_array_of_adextensionassociation(data_object.AdExtensionAssociations)
    output_status_message("* * * End output_adextensionassociationcollection * * *")

def output_array_of_adextensionassociationcollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdExtensionAssociationCollection']:
        output_adextensionassociationcollection(data_object)

def output_adextensioneditorialreason(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adextensioneditorialreason * * *")
    output_status_message("Location: {0}".format(data_object.Location))
    output_status_message("PublisherCountries:")
    output_array_of_string(data_object.PublisherCountries)
    output_status_message("ReasonCode: {0}".format(data_object.ReasonCode))
    output_status_message("Term: {0}".format(data_object.Term))
    output_status_message("* * * End output_adextensioneditorialreason * * *")

def output_array_of_adextensioneditorialreason(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdExtensionEditorialReason']:
        output_adextensioneditorialreason(data_object)

def output_adextensioneditorialreasoncollection(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adextensioneditorialreasoncollection * * *")
    output_status_message("AdExtensionId: {0}".format(data_object.AdExtensionId))
    output_status_message("Reasons:")
    output_array_of_adextensioneditorialreason(data_object.Reasons)
    output_status_message("* * * End output_adextensioneditorialreasoncollection * * *")

def output_array_of_adextensioneditorialreasoncollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdExtensionEditorialReasonCollection']:
        output_adextensioneditorialreasoncollection(data_object)

def output_adextensionidentity(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adextensionidentity * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Version: {0}".format(data_object.Version))
    output_status_message("* * * End output_adextensionidentity * * *")

def output_array_of_adextensionidentity(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdExtensionIdentity']:
        output_adextensionidentity(data_object)

def output_adextensionidtoentityidassociation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adextensionidtoentityidassociation * * *")
    output_status_message("AdExtensionId: {0}".format(data_object.AdExtensionId))
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("* * * End output_adextensionidtoentityidassociation * * *")

def output_array_of_adextensionidtoentityidassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdExtensionIdToEntityIdAssociation']:
        output_adextensionidtoentityidassociation(data_object)

def output_adgroup(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adgroup * * *")
    output_status_message("AdRotation:")
    output_adrotation(data_object.AdRotation)
    output_status_message("AudienceAdsBidAdjustment: {0}".format(data_object.AudienceAdsBidAdjustment))
    output_status_message("BiddingScheme:")
    output_biddingscheme(data_object.BiddingScheme)
    output_status_message("CpcBid:")
    output_bid(data_object.CpcBid)
    output_status_message("EndDate:")
    output_date(data_object.EndDate)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("MultimediaAdsBidAdjustment: {0}".format(data_object.MultimediaAdsBidAdjustment))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Network: {0}".format(data_object.Network))
    output_status_message("PrivacyStatus: {0}".format(data_object.PrivacyStatus))
    output_status_message("Settings:")
    output_array_of_setting(data_object.Settings)
    output_status_message("StartDate:")
    output_date(data_object.StartDate)
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("AdScheduleUseSearcherTimeZone: {0}".format(data_object.AdScheduleUseSearcherTimeZone))
    output_status_message("AdGroupType: {0}".format(data_object.AdGroupType))
    output_status_message("CpvBid:")
    output_bid(data_object.CpvBid)
    output_status_message("CpmBid:")
    output_bid(data_object.CpmBid)
    output_status_message("* * * End output_adgroup * * *")

def output_array_of_adgroup(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdGroup']:
        output_adgroup(data_object)

def output_adgroupcriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adgroupcriterion * * *")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("Criterion:")
    output_criterion(data_object.Criterion)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'BiddableAdGroupCriterion':
        output_biddableadgroupcriterion(data_object)
    if data_object.Type == 'NegativeAdGroupCriterion':
        output_negativeadgroupcriterion(data_object)
    output_status_message("* * * End output_adgroupcriterion * * *")

def output_array_of_adgroupcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdGroupCriterion']:
        output_adgroupcriterion(data_object)

def output_adgroupcriterionaction(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adgroupcriterionaction * * *")
    output_status_message("Action: {0}".format(data_object.Action))
    output_status_message("AdGroupCriterion:")
    output_adgroupcriterion(data_object.AdGroupCriterion)
    output_status_message("* * * End output_adgroupcriterionaction * * *")

def output_array_of_adgroupcriterionaction(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdGroupCriterionAction']:
        output_adgroupcriterionaction(data_object)

def output_adgroupnegativesites(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adgroupnegativesites * * *")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("NegativeSites:")
    output_array_of_string(data_object.NegativeSites)
    output_status_message("* * * End output_adgroupnegativesites * * *")

def output_array_of_adgroupnegativesites(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdGroupNegativeSites']:
        output_adgroupnegativesites(data_object)

def output_adrotation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_adrotation * * *")
    output_status_message("EndDate: {0}".format(data_object.EndDate))
    output_status_message("StartDate: {0}".format(data_object.StartDate))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("* * * End output_adrotation * * *")

def output_array_of_adrotation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdRotation']:
        output_adrotation(data_object)

def output_agecriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_agecriterion * * *")
    output_status_message("AgeRange: {0}".format(data_object.AgeRange))
    output_status_message("* * * End output_agecriterion * * *")

def output_array_of_agecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AgeCriterion']:
        output_agecriterion(data_object)

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

def output_appadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_appadextension * * *")
    output_status_message("AppPlatform: {0}".format(data_object.AppPlatform))
    output_status_message("AppStoreId: {0}".format(data_object.AppStoreId))
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("DisplayText: {0}".format(data_object.DisplayText))
    output_status_message("FinalAppUrls:")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("* * * End output_appadextension * * *")

def output_array_of_appadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AppAdExtension']:
        output_appadextension(data_object)

def output_appinstallad(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_appinstallad * * *")
    output_status_message("AppPlatform: {0}".format(data_object.AppPlatform))
    output_status_message("AppStoreId: {0}".format(data_object.AppStoreId))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("Title: {0}".format(data_object.Title))
    output_status_message("* * * End output_appinstallad * * *")

def output_array_of_appinstallad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AppInstallAd']:
        output_appinstallad(data_object)

def output_appinstallgoal(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_appinstallgoal * * *")
    output_status_message("AppPlatform: {0}".format(data_object.AppPlatform))
    output_status_message("AppStoreId: {0}".format(data_object.AppStoreId))
    output_status_message("* * * End output_appinstallgoal * * *")

def output_array_of_appinstallgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AppInstallGoal']:
        output_appinstallgoal(data_object)

def output_applicationfault(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_applicationfault * * *")
    output_status_message("TrackingId: {0}".format(data_object.TrackingId))
    if data_object.Type == 'AdApiFaultDetail':
        output_adapifaultdetail(data_object)
    if data_object.Type == 'ApiFaultDetail':
        output_apifaultdetail(data_object)
    if data_object.Type == 'EditorialApiFaultDetail':
        output_editorialapifaultdetail(data_object)
    output_status_message("* * * End output_applicationfault * * *")

def output_array_of_applicationfault(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ApplicationFault']:
        output_applicationfault(data_object)

def output_appurl(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_appurl * * *")
    output_status_message("OsType: {0}".format(data_object.OsType))
    output_status_message("Url: {0}".format(data_object.Url))
    output_status_message("* * * End output_appurl * * *")

def output_array_of_appurl(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AppUrl']:
        output_appurl(data_object)

def output_asset(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_asset * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'ImageAsset':
        output_imageasset(data_object)
    if data_object.Type == 'TextAsset':
        output_textasset(data_object)
    if data_object.Type == 'VideoAsset':
        output_videoasset(data_object)
    output_status_message("* * * End output_asset * * *")

def output_array_of_asset(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Asset']:
        output_asset(data_object)

def output_assetlink(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_assetlink * * *")
    output_status_message("Asset:")
    output_asset(data_object.Asset)
    output_status_message("AssetPerformanceLabel: {0}".format(data_object.AssetPerformanceLabel))
    output_status_message("EditorialStatus: {0}".format(data_object.EditorialStatus))
    output_status_message("PinnedField: {0}".format(data_object.PinnedField))
    output_status_message("* * * End output_assetlink * * *")

def output_array_of_assetlink(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AssetLink']:
        output_assetlink(data_object)

def output_audience(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_audience * * *")
    output_status_message("AudienceNetworkSize: {0}".format(data_object.AudienceNetworkSize))
    output_status_message("CustomerShare:")
    output_customershare(data_object.CustomerShare)
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MembershipDuration: {0}".format(data_object.MembershipDuration))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("ParentId: {0}".format(data_object.ParentId))
    output_status_message("Scope: {0}".format(data_object.Scope))
    output_status_message("SearchSize: {0}".format(data_object.SearchSize))
    output_status_message("SupportedCampaignTypes:")
    output_array_of_string(data_object.SupportedCampaignTypes)
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'CombinedList':
        output_combinedlist(data_object)
    if data_object.Type == 'Custom':
        output_customaudience(data_object)
    if data_object.Type == 'InMarket':
        output_inmarketaudience(data_object)
    if data_object.Type == 'Product':
        output_productaudience(data_object)
    if data_object.Type == 'RemarketingList':
        output_remarketinglist(data_object)
    if data_object.Type == 'SimilarRemarketingList':
        output_similarremarketinglist(data_object)
    output_status_message("* * * End output_audience * * *")

def output_array_of_audience(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Audience']:
        output_audience(data_object)

def output_audiencecriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_audiencecriterion * * *")
    output_status_message("AudienceId: {0}".format(data_object.AudienceId))
    output_status_message("AudienceType: {0}".format(data_object.AudienceType))
    output_status_message("* * * End output_audiencecriterion * * *")

def output_array_of_audiencecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AudienceCriterion']:
        output_audiencecriterion(data_object)

def output_batcherror(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_batcherror * * *")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("FieldPath: {0}".format(data_object.FieldPath))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Message: {0}".format(data_object.Message))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'EditorialError':
        output_editorialerror(data_object)
    output_status_message("* * * End output_batcherror * * *")

def output_array_of_batcherror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BatchError']:
        output_batcherror(data_object)

def output_batcherrorcollection(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_batcherrorcollection * * *")
    output_status_message("BatchErrors:")
    output_array_of_batcherror(data_object.BatchErrors)
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("ErrorCode: {0}".format(data_object.ErrorCode))
    output_status_message("FieldPath: {0}".format(data_object.FieldPath))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Message: {0}".format(data_object.Message))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'EditorialErrorCollection':
        output_editorialerrorcollection(data_object)
    output_status_message("* * * End output_batcherrorcollection * * *")

def output_array_of_batcherrorcollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BatchErrorCollection']:
        output_batcherrorcollection(data_object)

def output_bid(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_bid * * *")
    output_status_message("Amount: {0}".format(data_object.Amount))
    output_status_message("* * * End output_bid * * *")

def output_array_of_bid(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Bid']:
        output_bid(data_object)

def output_biddableadgroupcriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_biddableadgroupcriterion * * *")
    output_status_message("CriterionBid:")
    output_criterionbid(data_object.CriterionBid)
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("EditorialStatus: {0}".format(data_object.EditorialStatus))
    output_status_message("FinalAppUrls:")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("CriterionCashback:")
    output_criterioncashback(data_object.CriterionCashback)
    output_status_message("* * * End output_biddableadgroupcriterion * * *")

def output_array_of_biddableadgroupcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BiddableAdGroupCriterion']:
        output_biddableadgroupcriterion(data_object)

def output_biddablecampaigncriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_biddablecampaigncriterion * * *")
    output_status_message("CriterionBid:")
    output_criterionbid(data_object.CriterionBid)
    output_status_message("CriterionCashback:")
    output_criterioncashback(data_object.CriterionCashback)
    output_status_message("* * * End output_biddablecampaigncriterion * * *")

def output_array_of_biddablecampaigncriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BiddableCampaignCriterion']:
        output_biddablecampaigncriterion(data_object)

def output_biddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_biddingscheme * * *")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'EnhancedCpcBiddingScheme':
        output_enhancedcpcbiddingscheme(data_object)
    if data_object.Type == 'InheritFromParentBiddingScheme':
        output_inheritfromparentbiddingscheme(data_object)
    if data_object.Type == 'ManualCpcBiddingScheme':
        output_manualcpcbiddingscheme(data_object)
    if data_object.Type == 'ManualCpmBiddingScheme':
        output_manualcpmbiddingscheme(data_object)
    if data_object.Type == 'ManualCpvBiddingScheme':
        output_manualcpvbiddingscheme(data_object)
    if data_object.Type == 'MaxClicksBiddingScheme':
        output_maxclicksbiddingscheme(data_object)
    if data_object.Type == 'MaxConversionsBiddingScheme':
        output_maxconversionsbiddingscheme(data_object)
    if data_object.Type == 'MaxConversionValueBiddingScheme':
        output_maxconversionvaluebiddingscheme(data_object)
    if data_object.Type == 'MaxRoasBiddingScheme':
        output_maxroasbiddingscheme(data_object)
    if data_object.Type == 'TargetCpaBiddingScheme':
        output_targetcpabiddingscheme(data_object)
    if data_object.Type == 'TargetImpressionShareBiddingScheme':
        output_targetimpressionsharebiddingscheme(data_object)
    if data_object.Type == 'TargetRoasBiddingScheme':
        output_targetroasbiddingscheme(data_object)
    output_status_message("* * * End output_biddingscheme * * *")

def output_array_of_biddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BiddingScheme']:
        output_biddingscheme(data_object)

def output_bidmultiplier(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_bidmultiplier * * *")
    output_status_message("Multiplier: {0}".format(data_object.Multiplier))
    output_status_message("* * * End output_bidmultiplier * * *")

def output_array_of_bidmultiplier(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BidMultiplier']:
        output_bidmultiplier(data_object)

def output_bidstrategy(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_bidstrategy * * *")
    output_status_message("AssociatedCampaignType: {0}".format(data_object.AssociatedCampaignType))
    output_status_message("AssociationCount: {0}".format(data_object.AssociationCount))
    output_status_message("BiddingScheme:")
    output_biddingscheme(data_object.BiddingScheme)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("* * * End output_bidstrategy * * *")

def output_array_of_bidstrategy(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BidStrategy']:
        output_bidstrategy(data_object)

def output_bmcstore(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_bmcstore * * *")
    output_status_message("HasCatalog: {0}".format(data_object.HasCatalog))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("IsActive: {0}".format(data_object.IsActive))
    output_status_message("IsProductAdsEnabled: {0}".format(data_object.IsProductAdsEnabled))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("SubType: {0}".format(data_object.SubType))
    output_status_message("* * * End output_bmcstore * * *")

def output_array_of_bmcstore(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BMCStore']:
        output_bmcstore(data_object)

def output_budget(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_budget * * *")
    output_status_message("Amount: {0}".format(data_object.Amount))
    output_status_message("AssociationCount: {0}".format(data_object.AssociationCount))
    output_status_message("BudgetType: {0}".format(data_object.BudgetType))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("* * * End output_budget * * *")

def output_array_of_budget(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Budget']:
        output_budget(data_object)

def output_calladextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_calladextension * * *")
    output_status_message("CountryCode: {0}".format(data_object.CountryCode))
    output_status_message("IsCallOnly: {0}".format(data_object.IsCallOnly))
    output_status_message("IsCallTrackingEnabled: {0}".format(data_object.IsCallTrackingEnabled))
    output_status_message("PhoneNumber: {0}".format(data_object.PhoneNumber))
    output_status_message("RequireTollFreeTrackingNumber: {0}".format(data_object.RequireTollFreeTrackingNumber))
    output_status_message("* * * End output_calladextension * * *")

def output_array_of_calladextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CallAdExtension']:
        output_calladextension(data_object)

def output_calloutadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_calloutadextension * * *")
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("* * * End output_calloutadextension * * *")

def output_array_of_calloutadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CalloutAdExtension']:
        output_calloutadextension(data_object)

def output_campaign(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_campaign * * *")
    output_status_message("AudienceAdsBidAdjustment: {0}".format(data_object.AudienceAdsBidAdjustment))
    output_status_message("BiddingScheme:")
    output_biddingscheme(data_object.BiddingScheme)
    output_status_message("BudgetType: {0}".format(data_object.BudgetType))
    output_status_message("DailyBudget: {0}".format(data_object.DailyBudget))
    output_status_message("ExperimentId: {0}".format(data_object.ExperimentId))
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MultimediaAdsBidAdjustment: {0}".format(data_object.MultimediaAdsBidAdjustment))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("SubType: {0}".format(data_object.SubType))
    output_status_message("TimeZone: {0}".format(data_object.TimeZone))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("CampaignType: {0}".format(data_object.CampaignType))
    output_status_message("Settings:")
    output_array_of_setting(data_object.Settings)
    output_status_message("BudgetId: {0}".format(data_object.BudgetId))
    output_status_message("Languages:")
    output_array_of_string(data_object.Languages)
    output_status_message("AdScheduleUseSearcherTimeZone: {0}".format(data_object.AdScheduleUseSearcherTimeZone))
    output_status_message("BidStrategyId: {0}".format(data_object.BidStrategyId))
    output_status_message("* * * End output_campaign * * *")

def output_array_of_campaign(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Campaign']:
        output_campaign(data_object)

def output_campaignadgroupids(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_campaignadgroupids * * *")
    output_status_message("ActiveAdGroupsOnly: {0}".format(data_object.ActiveAdGroupsOnly))
    output_status_message("AdGroupIds:")
    output_array_of_long(data_object.AdGroupIds)
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("* * * End output_campaignadgroupids * * *")

def output_array_of_campaignadgroupids(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CampaignAdGroupIds']:
        output_campaignadgroupids(data_object)

def output_campaigncriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_campaigncriterion * * *")
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("Criterion:")
    output_criterion(data_object.Criterion)
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'BiddableCampaignCriterion':
        output_biddablecampaigncriterion(data_object)
    if data_object.Type == 'NegativeCampaignCriterion':
        output_negativecampaigncriterion(data_object)
    output_status_message("* * * End output_campaigncriterion * * *")

def output_array_of_campaigncriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CampaignCriterion']:
        output_campaigncriterion(data_object)

def output_campaignnegativesites(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_campaignnegativesites * * *")
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("NegativeSites:")
    output_array_of_string(data_object.NegativeSites)
    output_status_message("* * * End output_campaignnegativesites * * *")

def output_array_of_campaignnegativesites(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CampaignNegativeSites']:
        output_campaignnegativesites(data_object)

def output_cashbackadjustment(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_cashbackadjustment * * *")
    output_status_message("CashbackPercent: {0}".format(data_object.CashbackPercent))
    output_status_message("* * * End output_cashbackadjustment * * *")

def output_array_of_cashbackadjustment(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CashbackAdjustment']:
        output_cashbackadjustment(data_object)

def output_combinationrule(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_combinationrule * * *")
    output_status_message("AudienceIds:")
    output_array_of_long(data_object.AudienceIds)
    output_status_message("Operator: {0}".format(data_object.Operator))
    output_status_message("* * * End output_combinationrule * * *")

def output_array_of_combinationrule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CombinationRule']:
        output_combinationrule(data_object)

def output_combinedlist(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_combinedlist * * *")
    output_status_message("CombinationRules:")
    output_array_of_combinationrule(data_object.CombinationRules)
    output_status_message("* * * End output_combinedlist * * *")

def output_array_of_combinedlist(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CombinedList']:
        output_combinedlist(data_object)

def output_company(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_company * * *")
    output_status_message("LogoUrl: {0}".format(data_object.LogoUrl))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("ProfileId: {0}".format(data_object.ProfileId))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("* * * End output_company * * *")

def output_array_of_company(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Company']:
        output_company(data_object)

def output_conversiongoal(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_conversiongoal * * *")
    output_status_message("ConversionWindowInMinutes: {0}".format(data_object.ConversionWindowInMinutes))
    output_status_message("CountType: {0}".format(data_object.CountType))
    output_status_message("ExcludeFromBidding: {0}".format(data_object.ExcludeFromBidding))
    output_status_message("GoalCategory: {0}".format(data_object.GoalCategory))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Revenue:")
    output_conversiongoalrevenue(data_object.Revenue)
    output_status_message("Scope: {0}".format(data_object.Scope))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("TagId: {0}".format(data_object.TagId))
    output_status_message("TrackingStatus: {0}".format(data_object.TrackingStatus))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("ViewThroughConversionWindowInMinutes: {0}".format(data_object.ViewThroughConversionWindowInMinutes))
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
    output_status_message("* * * End output_conversiongoal * * *")

def output_array_of_conversiongoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ConversionGoal']:
        output_conversiongoal(data_object)

def output_conversiongoalrevenue(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_conversiongoalrevenue * * *")
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("Value: {0}".format(data_object.Value))
    output_status_message("* * * End output_conversiongoalrevenue * * *")

def output_array_of_conversiongoalrevenue(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ConversionGoalRevenue']:
        output_conversiongoalrevenue(data_object)

def output_coopsetting(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_coopsetting * * *")
    output_status_message("BidBoostValue: {0}".format(data_object.BidBoostValue))
    output_status_message("BidMaxValue: {0}".format(data_object.BidMaxValue))
    output_status_message("BidOption: {0}".format(data_object.BidOption))
    output_status_message("* * * End output_coopsetting * * *")

def output_array_of_coopsetting(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CoOpSetting']:
        output_coopsetting(data_object)

def output_criterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_criterion * * *")
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
    if data_object.Type == 'ProfileCriterion':
        output_profilecriterion(data_object)
    if data_object.Type == 'RadiusCriterion':
        output_radiuscriterion(data_object)
    if data_object.Type == 'StoreCriterion':
        output_storecriterion(data_object)
    if data_object.Type == 'Webpage':
        output_webpage(data_object)
    output_status_message("* * * End output_criterion * * *")

def output_array_of_criterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Criterion']:
        output_criterion(data_object)

def output_criterionbid(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_criterionbid * * *")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'BidMultiplier':
        output_bidmultiplier(data_object)
    if data_object.Type == 'FixedBid':
        output_fixedbid(data_object)
    output_status_message("* * * End output_criterionbid * * *")

def output_array_of_criterionbid(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CriterionBid']:
        output_criterionbid(data_object)

def output_criterioncashback(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_criterioncashback * * *")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'CashbackAdjustment':
        output_cashbackadjustment(data_object)
    output_status_message("* * * End output_criterioncashback * * *")

def output_array_of_criterioncashback(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CriterionCashback']:
        output_criterioncashback(data_object)

def output_customaudience(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customaudience * * *")
    output_status_message("* * * End output_customaudience * * *")

def output_array_of_customaudience(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CustomAudience']:
        output_customaudience(data_object)

def output_customeraccountshare(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customeraccountshare * * *")
    output_status_message("AccountId: {0}".format(data_object.AccountId))
    output_status_message("Associations:")
    output_array_of_customeraccountshareassociation(data_object.Associations)
    output_status_message("CustomerId: {0}".format(data_object.CustomerId))
    output_status_message("* * * End output_customeraccountshare * * *")

def output_array_of_customeraccountshare(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CustomerAccountShare']:
        output_customeraccountshare(data_object)

def output_customeraccountshareassociation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customeraccountshareassociation * * *")
    output_status_message("AssociationCount: {0}".format(data_object.AssociationCount))
    output_status_message("UsageType: {0}".format(data_object.UsageType))
    output_status_message("* * * End output_customeraccountshareassociation * * *")

def output_array_of_customeraccountshareassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CustomerAccountShareAssociation']:
        output_customeraccountshareassociation(data_object)

def output_customershare(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customershare * * *")
    output_status_message("CustomerAccountShares:")
    output_array_of_customeraccountshare(data_object.CustomerAccountShares)
    output_status_message("OwnerCustomerId: {0}".format(data_object.OwnerCustomerId))
    output_status_message("* * * End output_customershare * * *")

def output_array_of_customershare(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CustomerShare']:
        output_customershare(data_object)

def output_customeventsrule(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customeventsrule * * *")
    output_status_message("Action: {0}".format(data_object.Action))
    output_status_message("ActionOperator: {0}".format(data_object.ActionOperator))
    output_status_message("Category: {0}".format(data_object.Category))
    output_status_message("CategoryOperator: {0}".format(data_object.CategoryOperator))
    output_status_message("Label: {0}".format(data_object.Label))
    output_status_message("LabelOperator: {0}".format(data_object.LabelOperator))
    output_status_message("Value: {0}".format(data_object.Value))
    output_status_message("ValueOperator: {0}".format(data_object.ValueOperator))
    output_status_message("* * * End output_customeventsrule * * *")

def output_array_of_customeventsrule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CustomEventsRule']:
        output_customeventsrule(data_object)

def output_customparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customparameter * * *")
    output_status_message("Key: {0}".format(data_object.Key))
    output_status_message("Value: {0}".format(data_object.Value))
    output_status_message("* * * End output_customparameter * * *")

def output_array_of_customparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CustomParameter']:
        output_customparameter(data_object)

def output_customparameters(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customparameters * * *")
    output_status_message("Parameters:")
    output_array_of_customparameter(data_object.Parameters)
    output_status_message("* * * End output_customparameters * * *")

def output_array_of_customparameters(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CustomParameters']:
        output_customparameters(data_object)

def output_date(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_date * * *")
    output_status_message("Day: {0}".format(data_object.Day))
    output_status_message("Month: {0}".format(data_object.Month))
    output_status_message("Year: {0}".format(data_object.Year))
    output_status_message("* * * End output_date * * *")

def output_array_of_date(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Date']:
        output_date(data_object)

def output_daytime(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_daytime * * *")
    output_status_message("Day: {0}".format(data_object.Day))
    output_status_message("EndHour: {0}".format(data_object.EndHour))
    output_status_message("EndMinute: {0}".format(data_object.EndMinute))
    output_status_message("StartHour: {0}".format(data_object.StartHour))
    output_status_message("StartMinute: {0}".format(data_object.StartMinute))
    output_status_message("* * * End output_daytime * * *")

def output_array_of_daytime(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DayTime']:
        output_daytime(data_object)

def output_daytimecriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_daytimecriterion * * *")
    output_status_message("Day: {0}".format(data_object.Day))
    output_status_message("FromHour: {0}".format(data_object.FromHour))
    output_status_message("FromMinute: {0}".format(data_object.FromMinute))
    output_status_message("ToHour: {0}".format(data_object.ToHour))
    output_status_message("ToMinute: {0}".format(data_object.ToMinute))
    output_status_message("* * * End output_daytimecriterion * * *")

def output_array_of_daytimecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DayTimeCriterion']:
        output_daytimecriterion(data_object)

def output_devicecriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_devicecriterion * * *")
    output_status_message("DeviceName: {0}".format(data_object.DeviceName))
    output_status_message("OSName: {0}".format(data_object.OSName))
    output_status_message("* * * End output_devicecriterion * * *")

def output_array_of_devicecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DeviceCriterion']:
        output_devicecriterion(data_object)

def output_durationgoal(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_durationgoal * * *")
    output_status_message("MinimumDurationInSeconds: {0}".format(data_object.MinimumDurationInSeconds))
    output_status_message("* * * End output_durationgoal * * *")

def output_array_of_durationgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DurationGoal']:
        output_durationgoal(data_object)

def output_dynamicfeedsetting(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_dynamicfeedsetting * * *")
    output_status_message("FeedId: {0}".format(data_object.FeedId))
    output_status_message("* * * End output_dynamicfeedsetting * * *")

def output_array_of_dynamicfeedsetting(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DynamicFeedSetting']:
        output_dynamicfeedsetting(data_object)

def output_dynamicsearchad(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_dynamicsearchad * * *")
    output_status_message("Path1: {0}".format(data_object.Path1))
    output_status_message("Path2: {0}".format(data_object.Path2))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("TextPart2: {0}".format(data_object.TextPart2))
    output_status_message("* * * End output_dynamicsearchad * * *")

def output_array_of_dynamicsearchad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DynamicSearchAd']:
        output_dynamicsearchad(data_object)

def output_dynamicsearchadssetting(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_dynamicsearchadssetting * * *")
    output_status_message("DomainName: {0}".format(data_object.DomainName))
    output_status_message("DynamicDescriptionEnabled: {0}".format(data_object.DynamicDescriptionEnabled))
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("PageFeedIds:")
    output_array_of_long(data_object.PageFeedIds)
    output_status_message("Source: {0}".format(data_object.Source))
    output_status_message("* * * End output_dynamicsearchadssetting * * *")

def output_array_of_dynamicsearchadssetting(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DynamicSearchAdsSetting']:
        output_dynamicsearchadssetting(data_object)

def output_editorialapifaultdetail(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_editorialapifaultdetail * * *")
    output_status_message("BatchErrors:")
    output_array_of_batcherror(data_object.BatchErrors)
    output_status_message("EditorialErrors:")
    output_array_of_editorialerror(data_object.EditorialErrors)
    output_status_message("OperationErrors:")
    output_array_of_operationerror(data_object.OperationErrors)
    output_status_message("* * * End output_editorialapifaultdetail * * *")

def output_array_of_editorialapifaultdetail(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EditorialApiFaultDetail']:
        output_editorialapifaultdetail(data_object)

def output_editorialerror(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_editorialerror * * *")
    output_status_message("Appealable: {0}".format(data_object.Appealable))
    output_status_message("DisapprovedText: {0}".format(data_object.DisapprovedText))
    output_status_message("Location: {0}".format(data_object.Location))
    output_status_message("PublisherCountry: {0}".format(data_object.PublisherCountry))
    output_status_message("ReasonCode: {0}".format(data_object.ReasonCode))
    output_status_message("* * * End output_editorialerror * * *")

def output_array_of_editorialerror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EditorialError']:
        output_editorialerror(data_object)

def output_editorialerrorcollection(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_editorialerrorcollection * * *")
    output_status_message("Appealable: {0}".format(data_object.Appealable))
    output_status_message("DisapprovedText: {0}".format(data_object.DisapprovedText))
    output_status_message("Location: {0}".format(data_object.Location))
    output_status_message("PublisherCountry: {0}".format(data_object.PublisherCountry))
    output_status_message("ReasonCode: {0}".format(data_object.ReasonCode))
    output_status_message("* * * End output_editorialerrorcollection * * *")

def output_array_of_editorialerrorcollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EditorialErrorCollection']:
        output_editorialerrorcollection(data_object)

def output_editorialreason(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_editorialreason * * *")
    output_status_message("Location: {0}".format(data_object.Location))
    output_status_message("PublisherCountries:")
    output_array_of_string(data_object.PublisherCountries)
    output_status_message("ReasonCode: {0}".format(data_object.ReasonCode))
    output_status_message("Term: {0}".format(data_object.Term))
    output_status_message("* * * End output_editorialreason * * *")

def output_array_of_editorialreason(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EditorialReason']:
        output_editorialreason(data_object)

def output_editorialreasoncollection(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_editorialreasoncollection * * *")
    output_status_message("AdGroupId: {0}".format(data_object.AdGroupId))
    output_status_message("AdOrKeywordId: {0}".format(data_object.AdOrKeywordId))
    output_status_message("AppealStatus: {0}".format(data_object.AppealStatus))
    output_status_message("Reasons:")
    output_array_of_editorialreason(data_object.Reasons)
    output_status_message("* * * End output_editorialreasoncollection * * *")

def output_array_of_editorialreasoncollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EditorialReasonCollection']:
        output_editorialreasoncollection(data_object)

def output_enhancedcpcbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_enhancedcpcbiddingscheme * * *")
    output_status_message("* * * End output_enhancedcpcbiddingscheme * * *")

def output_array_of_enhancedcpcbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EnhancedCpcBiddingScheme']:
        output_enhancedcpcbiddingscheme(data_object)

def output_entityidtoparentidassociation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_entityidtoparentidassociation * * *")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("ParentId: {0}".format(data_object.ParentId))
    output_status_message("* * * End output_entityidtoparentidassociation * * *")

def output_array_of_entityidtoparentidassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EntityIdToParentIdAssociation']:
        output_entityidtoparentidassociation(data_object)

def output_entitynegativekeyword(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_entitynegativekeyword * * *")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("EntityType: {0}".format(data_object.EntityType))
    output_status_message("NegativeKeywords:")
    output_array_of_negativekeyword(data_object.NegativeKeywords)
    output_status_message("* * * End output_entitynegativekeyword * * *")

def output_array_of_entitynegativekeyword(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EntityNegativeKeyword']:
        output_entitynegativekeyword(data_object)

def output_eventgoal(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_eventgoal * * *")
    output_status_message("ActionExpression: {0}".format(data_object.ActionExpression))
    output_status_message("ActionOperator: {0}".format(data_object.ActionOperator))
    output_status_message("CategoryExpression: {0}".format(data_object.CategoryExpression))
    output_status_message("CategoryOperator: {0}".format(data_object.CategoryOperator))
    output_status_message("LabelExpression: {0}".format(data_object.LabelExpression))
    output_status_message("LabelOperator: {0}".format(data_object.LabelOperator))
    output_status_message("Value: {0}".format(data_object.Value))
    output_status_message("ValueOperator: {0}".format(data_object.ValueOperator))
    output_status_message("* * * End output_eventgoal * * *")

def output_array_of_eventgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['EventGoal']:
        output_eventgoal(data_object)

def output_expandedtextad(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_expandedtextad * * *")
    output_status_message("Domain: {0}".format(data_object.Domain))
    output_status_message("Path1: {0}".format(data_object.Path1))
    output_status_message("Path2: {0}".format(data_object.Path2))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("TextPart2: {0}".format(data_object.TextPart2))
    output_status_message("TitlePart1: {0}".format(data_object.TitlePart1))
    output_status_message("TitlePart2: {0}".format(data_object.TitlePart2))
    output_status_message("TitlePart3: {0}".format(data_object.TitlePart3))
    output_status_message("* * * End output_expandedtextad * * *")

def output_array_of_expandedtextad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ExpandedTextAd']:
        output_expandedtextad(data_object)

def output_experiment(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_experiment * * *")
    output_status_message("BaseCampaignId: {0}".format(data_object.BaseCampaignId))
    output_status_message("EndDate:")
    output_date(data_object.EndDate)
    output_status_message("ExperimentCampaignId: {0}".format(data_object.ExperimentCampaignId))
    output_status_message("ExperimentStatus: {0}".format(data_object.ExperimentStatus))
    output_status_message("ExperimentType: {0}".format(data_object.ExperimentType))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("StartDate:")
    output_date(data_object.StartDate)
    output_status_message("TrafficSplitPercent: {0}".format(data_object.TrafficSplitPercent))
    output_status_message("* * * End output_experiment * * *")

def output_array_of_experiment(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Experiment']:
        output_experiment(data_object)

def output_fileimportjob(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_fileimportjob * * *")
    output_status_message("FileSource: {0}".format(data_object.FileSource))
    output_status_message("FileUrl: {0}".format(data_object.FileUrl))
    output_status_message("* * * End output_fileimportjob * * *")

def output_array_of_fileimportjob(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['FileImportJob']:
        output_fileimportjob(data_object)

def output_fileimportoption(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_fileimportoption * * *")
    output_status_message("* * * End output_fileimportoption * * *")

def output_array_of_fileimportoption(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['FileImportOption']:
        output_fileimportoption(data_object)

def output_filterlinkadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_filterlinkadextension * * *")
    output_status_message("AdExtensionHeaderType: {0}".format(data_object.AdExtensionHeaderType))
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("Texts:")
    output_array_of_string(data_object.Texts)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("* * * End output_filterlinkadextension * * *")

def output_array_of_filterlinkadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['FilterLinkAdExtension']:
        output_filterlinkadextension(data_object)

def output_fixedbid(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_fixedbid * * *")
    output_status_message("Amount: {0}".format(data_object.Amount))
    output_status_message("* * * End output_fixedbid * * *")

def output_array_of_fixedbid(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['FixedBid']:
        output_fixedbid(data_object)

def output_flyeradextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_flyeradextension * * *")
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("FinalAppUrls:")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("FlyerName: {0}".format(data_object.FlyerName))
    output_status_message("ImageMediaIds:")
    output_array_of_long(data_object.ImageMediaIds)
    output_status_message("ImageMediaUrls:")
    output_array_of_string(data_object.ImageMediaUrls)
    output_status_message("StoreId: {0}".format(data_object.StoreId))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("* * * End output_flyeradextension * * *")

def output_array_of_flyeradextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['FlyerAdExtension']:
        output_flyeradextension(data_object)

def output_frequency(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_frequency * * *")
    output_status_message("Cron: {0}".format(data_object.Cron))
    output_status_message("TimeZone: {0}".format(data_object.TimeZone))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("* * * End output_frequency * * *")

def output_array_of_frequency(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Frequency']:
        output_frequency(data_object)

def output_gendercriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_gendercriterion * * *")
    output_status_message("GenderType: {0}".format(data_object.GenderType))
    output_status_message("* * * End output_gendercriterion * * *")

def output_array_of_gendercriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['GenderCriterion']:
        output_gendercriterion(data_object)

def output_geopoint(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_geopoint * * *")
    output_status_message("LatitudeInMicroDegrees: {0}".format(data_object.LatitudeInMicroDegrees))
    output_status_message("LongitudeInMicroDegrees: {0}".format(data_object.LongitudeInMicroDegrees))
    output_status_message("* * * End output_geopoint * * *")

def output_array_of_geopoint(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['GeoPoint']:
        output_geopoint(data_object)

def output_googleimportjob(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_googleimportjob * * *")
    output_status_message("CampaignAdGroupIds:")
    output_array_of_campaignadgroupids(data_object.CampaignAdGroupIds)
    output_status_message("CredentialId: {0}".format(data_object.CredentialId))
    output_status_message("GoogleAccountId: {0}".format(data_object.GoogleAccountId))
    output_status_message("GoogleUserName: {0}".format(data_object.GoogleUserName))
    output_status_message("* * * End output_googleimportjob * * *")

def output_array_of_googleimportjob(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['GoogleImportJob']:
        output_googleimportjob(data_object)

def output_googleimportoption(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_googleimportoption * * *")
    output_status_message("AccountUrlOptions: {0}".format(data_object.AccountUrlOptions))
    output_status_message("AdjustmentForBids: {0}".format(data_object.AdjustmentForBids))
    output_status_message("AdjustmentForCampaignBudgets: {0}".format(data_object.AdjustmentForCampaignBudgets))
    output_status_message("AssociatedStoreId: {0}".format(data_object.AssociatedStoreId))
    output_status_message("AssociatedUetTagId: {0}".format(data_object.AssociatedUetTagId))
    output_status_message("AutoDeviceBidOptimization: {0}".format(data_object.AutoDeviceBidOptimization))
    output_status_message("DeleteRemovedEntities: {0}".format(data_object.DeleteRemovedEntities))
    output_status_message("EnableAutoCurrencyConversion: {0}".format(data_object.EnableAutoCurrencyConversion))
    output_status_message("EnableParentLocationMapping: {0}".format(data_object.EnableParentLocationMapping))
    output_status_message("NewActiveAdsForExistingAdGroups: {0}".format(data_object.NewActiveAdsForExistingAdGroups))
    output_status_message("NewActiveCampaignsAndChildEntities: {0}".format(data_object.NewActiveCampaignsAndChildEntities))
    output_status_message("NewAdCustomizerFeeds: {0}".format(data_object.NewAdCustomizerFeeds))
    output_status_message("NewAdGroupsAndChildEntitiesForExistingCampaigns: {0}".format(data_object.NewAdGroupsAndChildEntitiesForExistingCampaigns))
    output_status_message("NewAdSchedules: {0}".format(data_object.NewAdSchedules))
    output_status_message("NewAppAdExtensions: {0}".format(data_object.NewAppAdExtensions))
    output_status_message("NewAudienceTargets: {0}".format(data_object.NewAudienceTargets))
    output_status_message("NewCallAdExtensions: {0}".format(data_object.NewCallAdExtensions))
    output_status_message("NewCalloutAdExtensions: {0}".format(data_object.NewCalloutAdExtensions))
    output_status_message("NewDemographicTargets: {0}".format(data_object.NewDemographicTargets))
    output_status_message("NewDeviceTargets: {0}".format(data_object.NewDeviceTargets))
    output_status_message("NewEntities: {0}".format(data_object.NewEntities))
    output_status_message("NewKeywordUrls: {0}".format(data_object.NewKeywordUrls))
    output_status_message("NewKeywordsForExistingAdGroups: {0}".format(data_object.NewKeywordsForExistingAdGroups))
    output_status_message("NewLabels: {0}".format(data_object.NewLabels))
    output_status_message("NewLocationAdExtensions: {0}".format(data_object.NewLocationAdExtensions))
    output_status_message("NewLocationTargets: {0}".format(data_object.NewLocationTargets))
    output_status_message("NewNegativeKeywordLists: {0}".format(data_object.NewNegativeKeywordLists))
    output_status_message("NewNegativeKeywordsForExistingParents: {0}".format(data_object.NewNegativeKeywordsForExistingParents))
    output_status_message("NewNegativeSites: {0}".format(data_object.NewNegativeSites))
    output_status_message("NewPageFeeds: {0}".format(data_object.NewPageFeeds))
    output_status_message("NewPausedAdsForExistingAdGroups: {0}".format(data_object.NewPausedAdsForExistingAdGroups))
    output_status_message("NewPausedCampaignsAndChildEntities: {0}".format(data_object.NewPausedCampaignsAndChildEntities))
    output_status_message("NewPriceAdExtensions: {0}".format(data_object.NewPriceAdExtensions))
    output_status_message("NewProductFilters: {0}".format(data_object.NewProductFilters))
    output_status_message("NewPromotionAdExtensions: {0}".format(data_object.NewPromotionAdExtensions))
    output_status_message("NewReviewAdExtensions: {0}".format(data_object.NewReviewAdExtensions))
    output_status_message("NewSitelinkAdExtensions: {0}".format(data_object.NewSitelinkAdExtensions))
    output_status_message("NewStructuredSnippetAdExtensions: {0}".format(data_object.NewStructuredSnippetAdExtensions))
    output_status_message("NewUrlOptions: {0}".format(data_object.NewUrlOptions))
    output_status_message("PauseCampaignsWithoutSupportedLocations: {0}".format(data_object.PauseCampaignsWithoutSupportedLocations))
    output_status_message("PauseNewCampaigns: {0}".format(data_object.PauseNewCampaigns))
    output_status_message("RaiseBidsToMinimum: {0}".format(data_object.RaiseBidsToMinimum))
    output_status_message("RaiseCampaignBudgetsToMinimum: {0}".format(data_object.RaiseCampaignBudgetsToMinimum))
    output_status_message("RaiseProductGroupBidsToMinimum: {0}".format(data_object.RaiseProductGroupBidsToMinimum))
    output_status_message("SearchAndDsaMixedCampaignAsSearchCampaign: {0}".format(data_object.SearchAndDsaMixedCampaignAsSearchCampaign))
    output_status_message("SearchAndReplaceForCampaignNames:")
    output_importsearchandreplaceforstringproperty(data_object.SearchAndReplaceForCampaignNames)
    output_status_message("SearchAndReplaceForCustomParameters:")
    output_importsearchandreplaceforstringproperty(data_object.SearchAndReplaceForCustomParameters)
    output_status_message("SearchAndReplaceForTrackingTemplates:")
    output_importsearchandreplaceforstringproperty(data_object.SearchAndReplaceForTrackingTemplates)
    output_status_message("SearchAndReplaceForUrls:")
    output_importsearchandreplaceforstringproperty(data_object.SearchAndReplaceForUrls)
    output_status_message("SuffixForCampaignNames: {0}".format(data_object.SuffixForCampaignNames))
    output_status_message("SuffixForTrackingTemplates: {0}".format(data_object.SuffixForTrackingTemplates))
    output_status_message("SuffixForUrls: {0}".format(data_object.SuffixForUrls))
    output_status_message("UpdateAdCustomizerFeeds: {0}".format(data_object.UpdateAdCustomizerFeeds))
    output_status_message("UpdateAdGroupNetwork: {0}".format(data_object.UpdateAdGroupNetwork))
    output_status_message("UpdateAdSchedules: {0}".format(data_object.UpdateAdSchedules))
    output_status_message("UpdateAppAdExtensions: {0}".format(data_object.UpdateAppAdExtensions))
    output_status_message("UpdateAudienceTargets: {0}".format(data_object.UpdateAudienceTargets))
    output_status_message("UpdateBiddingStrategies: {0}".format(data_object.UpdateBiddingStrategies))
    output_status_message("UpdateBids: {0}".format(data_object.UpdateBids))
    output_status_message("UpdateCallAdExtensions: {0}".format(data_object.UpdateCallAdExtensions))
    output_status_message("UpdateCalloutAdExtensions: {0}".format(data_object.UpdateCalloutAdExtensions))
    output_status_message("UpdateCampaignAdGroupLanguages: {0}".format(data_object.UpdateCampaignAdGroupLanguages))
    output_status_message("UpdateCampaignBudgets: {0}".format(data_object.UpdateCampaignBudgets))
    output_status_message("UpdateCampaignNames: {0}".format(data_object.UpdateCampaignNames))
    output_status_message("UpdateDemographicTargets: {0}".format(data_object.UpdateDemographicTargets))
    output_status_message("UpdateDeviceTargets: {0}".format(data_object.UpdateDeviceTargets))
    output_status_message("UpdateEntities: {0}".format(data_object.UpdateEntities))
    output_status_message("UpdateKeywordUrls: {0}".format(data_object.UpdateKeywordUrls))
    output_status_message("UpdateLabels: {0}".format(data_object.UpdateLabels))
    output_status_message("UpdateLocationAdExtensions: {0}".format(data_object.UpdateLocationAdExtensions))
    output_status_message("UpdateLocationTargets: {0}".format(data_object.UpdateLocationTargets))
    output_status_message("UpdateNegativeKeywordLists: {0}".format(data_object.UpdateNegativeKeywordLists))
    output_status_message("UpdateNegativeSites: {0}".format(data_object.UpdateNegativeSites))
    output_status_message("UpdatePageFeeds: {0}".format(data_object.UpdatePageFeeds))
    output_status_message("UpdatePriceAdExtensions: {0}".format(data_object.UpdatePriceAdExtensions))
    output_status_message("UpdateProductFilters: {0}".format(data_object.UpdateProductFilters))
    output_status_message("UpdatePromotionAdExtensions: {0}".format(data_object.UpdatePromotionAdExtensions))
    output_status_message("UpdateReviewAdExtensions: {0}".format(data_object.UpdateReviewAdExtensions))
    output_status_message("UpdateSitelinkAdExtensions: {0}".format(data_object.UpdateSitelinkAdExtensions))
    output_status_message("UpdateStatusForAdGroups: {0}".format(data_object.UpdateStatusForAdGroups))
    output_status_message("UpdateStatusForAds: {0}".format(data_object.UpdateStatusForAds))
    output_status_message("UpdateStatusForCampaigns: {0}".format(data_object.UpdateStatusForCampaigns))
    output_status_message("UpdateStatusForKeywords: {0}".format(data_object.UpdateStatusForKeywords))
    output_status_message("UpdateStructuredSnippetAdExtensions: {0}".format(data_object.UpdateStructuredSnippetAdExtensions))
    output_status_message("UpdateUrlOptions: {0}".format(data_object.UpdateUrlOptions))
    output_status_message("* * * End output_googleimportoption * * *")

def output_array_of_googleimportoption(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['GoogleImportOption']:
        output_googleimportoption(data_object)

def output_idcollection(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_idcollection * * *")
    output_status_message("Ids:")
    output_array_of_long(data_object.Ids)
    output_status_message("* * * End output_idcollection * * *")

def output_array_of_idcollection(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['IdCollection']:
        output_idcollection(data_object)

def output_image(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_image * * *")
    output_status_message("Data: {0}".format(data_object.Data))
    output_status_message("* * * End output_image * * *")

def output_array_of_image(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Image']:
        output_image(data_object)

def output_imageadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_imageadextension * * *")
    output_status_message("AlternativeText: {0}".format(data_object.AlternativeText))
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("DisplayText: {0}".format(data_object.DisplayText))
    output_status_message("FinalAppUrls:")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("ImageMediaIds:")
    output_array_of_long(data_object.ImageMediaIds)
    output_status_message("Images:")
    output_array_of_assetlink(data_object.Images)
    output_status_message("Layouts:")
    output_array_of_string(data_object.Layouts)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("* * * End output_imageadextension * * *")

def output_array_of_imageadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ImageAdExtension']:
        output_imageadextension(data_object)

def output_imageasset(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_imageasset * * *")
    output_status_message("CropHeight: {0}".format(data_object.CropHeight))
    output_status_message("CropWidth: {0}".format(data_object.CropWidth))
    output_status_message("CropX: {0}".format(data_object.CropX))
    output_status_message("CropY: {0}".format(data_object.CropY))
    output_status_message("SubType: {0}".format(data_object.SubType))
    output_status_message("* * * End output_imageasset * * *")

def output_array_of_imageasset(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ImageAsset']:
        output_imageasset(data_object)

def output_imagemediarepresentation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_imagemediarepresentation * * *")
    output_status_message("Height: {0}".format(data_object.Height))
    output_status_message("Width: {0}".format(data_object.Width))
    output_status_message("* * * End output_imagemediarepresentation * * *")

def output_array_of_imagemediarepresentation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ImageMediaRepresentation']:
        output_imagemediarepresentation(data_object)

def output_importentitystatistics(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_importentitystatistics * * *")
    output_status_message("Additions: {0}".format(data_object.Additions))
    output_status_message("Changes: {0}".format(data_object.Changes))
    output_status_message("Deletions: {0}".format(data_object.Deletions))
    output_status_message("EntityType: {0}".format(data_object.EntityType))
    output_status_message("Errors: {0}".format(data_object.Errors))
    output_status_message("Total: {0}".format(data_object.Total))
    output_status_message("* * * End output_importentitystatistics * * *")

def output_array_of_importentitystatistics(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ImportEntityStatistics']:
        output_importentitystatistics(data_object)

def output_importjob(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_importjob * * *")
    output_status_message("CreatedByUserId: {0}".format(data_object.CreatedByUserId))
    output_status_message("CreatedByUserName: {0}".format(data_object.CreatedByUserName))
    output_status_message("CreatedDateTimeInUTC: {0}".format(data_object.CreatedDateTimeInUTC))
    output_status_message("Frequency:")
    output_frequency(data_object.Frequency)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("ImportOption:")
    output_importoption(data_object.ImportOption)
    output_status_message("LastRunTimeInUTC: {0}".format(data_object.LastRunTimeInUTC))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("NotificationEmail: {0}".format(data_object.NotificationEmail))
    output_status_message("NotificationType: {0}".format(data_object.NotificationType))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'FileImportJob':
        output_fileimportjob(data_object)
    if data_object.Type == 'GoogleImportJob':
        output_googleimportjob(data_object)
    output_status_message("* * * End output_importjob * * *")

def output_array_of_importjob(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ImportJob']:
        output_importjob(data_object)

def output_importoption(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_importoption * * *")
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'FileImportOption':
        output_fileimportoption(data_object)
    if data_object.Type == 'GoogleImportOption':
        output_googleimportoption(data_object)
    output_status_message("* * * End output_importoption * * *")

def output_array_of_importoption(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ImportOption']:
        output_importoption(data_object)

def output_importresult(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_importresult * * *")
    output_status_message("EntityStatistics:")
    output_array_of_importentitystatistics(data_object.EntityStatistics)
    output_status_message("ErrorLogUrl: {0}".format(data_object.ErrorLogUrl))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("ImportJob:")
    output_importjob(data_object.ImportJob)
    output_status_message("StartTimeInUTC: {0}".format(data_object.StartTimeInUTC))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("* * * End output_importresult * * *")

def output_array_of_importresult(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ImportResult']:
        output_importresult(data_object)

def output_importsearchandreplaceforstringproperty(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_importsearchandreplaceforstringproperty * * *")
    output_status_message("ReplaceString: {0}".format(data_object.ReplaceString))
    output_status_message("SearchString: {0}".format(data_object.SearchString))
    output_status_message("* * * End output_importsearchandreplaceforstringproperty * * *")

def output_array_of_importsearchandreplaceforstringproperty(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ImportSearchAndReplaceForStringProperty']:
        output_importsearchandreplaceforstringproperty(data_object)

def output_inheritfromparentbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_inheritfromparentbiddingscheme * * *")
    output_status_message("InheritedBidStrategyType: {0}".format(data_object.InheritedBidStrategyType))
    output_status_message("* * * End output_inheritfromparentbiddingscheme * * *")

def output_array_of_inheritfromparentbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['InheritFromParentBiddingScheme']:
        output_inheritfromparentbiddingscheme(data_object)

def output_inmarketaudience(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_inmarketaudience * * *")
    output_status_message("* * * End output_inmarketaudience * * *")

def output_array_of_inmarketaudience(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['InMarketAudience']:
        output_inmarketaudience(data_object)

def output_instoretransactiongoal(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_instoretransactiongoal * * *")
    output_status_message("* * * End output_instoretransactiongoal * * *")

def output_array_of_instoretransactiongoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['InStoreTransactionGoal']:
        output_instoretransactiongoal(data_object)

def output_keyvaluepairoflonglong(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keyvaluepairoflonglong * * *")
    output_status_message("key: {0}".format(data_object.key))
    output_status_message("value: {0}".format(data_object.value))
    output_status_message("* * * End output_keyvaluepairoflonglong * * *")

def output_array_of_keyvaluepairoflonglong(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeyValuePairOflonglong']:
        output_keyvaluepairoflonglong(data_object)

def output_keyvaluepairofstringstring(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keyvaluepairofstringstring * * *")
    output_status_message("key: {0}".format(data_object.key))
    output_status_message("value: {0}".format(data_object.value))
    output_status_message("* * * End output_keyvaluepairofstringstring * * *")

def output_array_of_keyvaluepairofstringstring(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeyValuePairOfstringstring']:
        output_keyvaluepairofstringstring(data_object)

def output_keyword(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keyword * * *")
    output_status_message("Bid:")
    output_bid(data_object.Bid)
    output_status_message("BiddingScheme:")
    output_biddingscheme(data_object.BiddingScheme)
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("EditorialStatus: {0}".format(data_object.EditorialStatus))
    output_status_message("FinalAppUrls:")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MatchType: {0}".format(data_object.MatchType))
    output_status_message("Param1: {0}".format(data_object.Param1))
    output_status_message("Param2: {0}".format(data_object.Param2))
    output_status_message("Param3: {0}".format(data_object.Param3))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("* * * End output_keyword * * *")

def output_array_of_keyword(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Keyword']:
        output_keyword(data_object)

def output_label(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_label * * *")
    output_status_message("ColorCode: {0}".format(data_object.ColorCode))
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("* * * End output_label * * *")

def output_array_of_label(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Label']:
        output_label(data_object)

def output_labelassociation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_labelassociation * * *")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("LabelId: {0}".format(data_object.LabelId))
    output_status_message("* * * End output_labelassociation * * *")

def output_array_of_labelassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['LabelAssociation']:
        output_labelassociation(data_object)

def output_locationadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_locationadextension * * *")
    output_status_message("Address:")
    output_address(data_object.Address)
    output_status_message("CompanyName: {0}".format(data_object.CompanyName))
    output_status_message("GeoCodeStatus: {0}".format(data_object.GeoCodeStatus))
    output_status_message("GeoPoint:")
    output_geopoint(data_object.GeoPoint)
    output_status_message("PhoneNumber: {0}".format(data_object.PhoneNumber))
    output_status_message("* * * End output_locationadextension * * *")

def output_array_of_locationadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['LocationAdExtension']:
        output_locationadextension(data_object)

def output_locationcriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_locationcriterion * * *")
    output_status_message("DisplayName: {0}".format(data_object.DisplayName))
    output_status_message("EnclosedLocationIds:")
    output_array_of_long(data_object.EnclosedLocationIds)
    output_status_message("LocationId: {0}".format(data_object.LocationId))
    output_status_message("LocationType: {0}".format(data_object.LocationType))
    output_status_message("* * * End output_locationcriterion * * *")

def output_array_of_locationcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['LocationCriterion']:
        output_locationcriterion(data_object)

def output_locationintentcriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_locationintentcriterion * * *")
    output_status_message("IntentOption: {0}".format(data_object.IntentOption))
    output_status_message("* * * End output_locationintentcriterion * * *")

def output_array_of_locationintentcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['LocationIntentCriterion']:
        output_locationintentcriterion(data_object)

def output_manualcpcbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_manualcpcbiddingscheme * * *")
    output_status_message("* * * End output_manualcpcbiddingscheme * * *")

def output_array_of_manualcpcbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ManualCpcBiddingScheme']:
        output_manualcpcbiddingscheme(data_object)

def output_manualcpmbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_manualcpmbiddingscheme * * *")
    output_status_message("* * * End output_manualcpmbiddingscheme * * *")

def output_array_of_manualcpmbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ManualCpmBiddingScheme']:
        output_manualcpmbiddingscheme(data_object)

def output_manualcpvbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_manualcpvbiddingscheme * * *")
    output_status_message("* * * End output_manualcpvbiddingscheme * * *")

def output_array_of_manualcpvbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ManualCpvBiddingScheme']:
        output_manualcpvbiddingscheme(data_object)

def output_maxclicksbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_maxclicksbiddingscheme * * *")
    output_status_message("MaxCpc:")
    output_bid(data_object.MaxCpc)
    output_status_message("* * * End output_maxclicksbiddingscheme * * *")

def output_array_of_maxclicksbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['MaxClicksBiddingScheme']:
        output_maxclicksbiddingscheme(data_object)

def output_maxconversionsbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_maxconversionsbiddingscheme * * *")
    output_status_message("MaxCpc:")
    output_bid(data_object.MaxCpc)
    output_status_message("* * * End output_maxconversionsbiddingscheme * * *")

def output_array_of_maxconversionsbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['MaxConversionsBiddingScheme']:
        output_maxconversionsbiddingscheme(data_object)

def output_maxconversionvaluebiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_maxconversionvaluebiddingscheme * * *")
    output_status_message("TargetRoas: {0}".format(data_object.TargetRoas))
    output_status_message("* * * End output_maxconversionvaluebiddingscheme * * *")

def output_array_of_maxconversionvaluebiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['MaxConversionValueBiddingScheme']:
        output_maxconversionvaluebiddingscheme(data_object)

def output_maxroasbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_maxroasbiddingscheme * * *")
    output_status_message("MaxCpc:")
    output_bid(data_object.MaxCpc)
    output_status_message("* * * End output_maxroasbiddingscheme * * *")

def output_array_of_maxroasbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['MaxRoasBiddingScheme']:
        output_maxroasbiddingscheme(data_object)

def output_media(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_media * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MediaType: {0}".format(data_object.MediaType))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'Image':
        output_image(data_object)
    output_status_message("* * * End output_media * * *")

def output_array_of_media(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Media']:
        output_media(data_object)

def output_mediaassociation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_mediaassociation * * *")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("MediaEnabledEntity: {0}".format(data_object.MediaEnabledEntity))
    output_status_message("MediaId: {0}".format(data_object.MediaId))
    output_status_message("* * * End output_mediaassociation * * *")

def output_array_of_mediaassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['MediaAssociation']:
        output_mediaassociation(data_object)

def output_mediametadata(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_mediametadata * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("MediaType: {0}".format(data_object.MediaType))
    output_status_message("Representations:")
    output_array_of_mediarepresentation(data_object.Representations)
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("* * * End output_mediametadata * * *")

def output_array_of_mediametadata(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['MediaMetaData']:
        output_mediametadata(data_object)

def output_mediarepresentation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_mediarepresentation * * *")
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("Url: {0}".format(data_object.Url))
    if data_object.Type == 'ImageMediaRepresentation':
        output_imagemediarepresentation(data_object)
    output_status_message("* * * End output_mediarepresentation * * *")

def output_array_of_mediarepresentation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['MediaRepresentation']:
        output_mediarepresentation(data_object)

def output_migrationstatusinfo(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_migrationstatusinfo * * *")
    output_status_message("MigrationType: {0}".format(data_object.MigrationType))
    output_status_message("StartTimeInUtc: {0}".format(data_object.StartTimeInUtc))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("* * * End output_migrationstatusinfo * * *")

def output_array_of_migrationstatusinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['MigrationStatusInfo']:
        output_migrationstatusinfo(data_object)

def output_negativeadgroupcriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_negativeadgroupcriterion * * *")
    output_status_message("* * * End output_negativeadgroupcriterion * * *")

def output_array_of_negativeadgroupcriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['NegativeAdGroupCriterion']:
        output_negativeadgroupcriterion(data_object)

def output_negativecampaigncriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_negativecampaigncriterion * * *")
    output_status_message("* * * End output_negativecampaigncriterion * * *")

def output_array_of_negativecampaigncriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['NegativeCampaignCriterion']:
        output_negativecampaigncriterion(data_object)

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

def output_negativekeywordlist(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_negativekeywordlist * * *")
    output_status_message("* * * End output_negativekeywordlist * * *")

def output_array_of_negativekeywordlist(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['NegativeKeywordList']:
        output_negativekeywordlist(data_object)

def output_negativesite(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_negativesite * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Url: {0}".format(data_object.Url))
    output_status_message("* * * End output_negativesite * * *")

def output_array_of_negativesite(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['NegativeSite']:
        output_negativesite(data_object)

def output_offlineconversion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_offlineconversion * * *")
    output_status_message("ConversionCurrencyCode: {0}".format(data_object.ConversionCurrencyCode))
    output_status_message("ConversionName: {0}".format(data_object.ConversionName))
    output_status_message("ConversionTime: {0}".format(data_object.ConversionTime))
    output_status_message("ConversionValue: {0}".format(data_object.ConversionValue))
    output_status_message("ExternalAttributionCredit: {0}".format(data_object.ExternalAttributionCredit))
    output_status_message("ExternalAttributionModel: {0}".format(data_object.ExternalAttributionModel))
    output_status_message("MicrosoftClickId: {0}".format(data_object.MicrosoftClickId))
    output_status_message("* * * End output_offlineconversion * * *")

def output_array_of_offlineconversion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['OfflineConversion']:
        output_offlineconversion(data_object)

def output_offlineconversionadjustment(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_offlineconversionadjustment * * *")
    output_status_message("AdjustmentCurrencyCode: {0}".format(data_object.AdjustmentCurrencyCode))
    output_status_message("AdjustmentTime: {0}".format(data_object.AdjustmentTime))
    output_status_message("AdjustmentType: {0}".format(data_object.AdjustmentType))
    output_status_message("AdjustmentValue: {0}".format(data_object.AdjustmentValue))
    output_status_message("ConversionName: {0}".format(data_object.ConversionName))
    output_status_message("ConversionTime: {0}".format(data_object.ConversionTime))
    output_status_message("MicrosoftClickId: {0}".format(data_object.MicrosoftClickId))
    output_status_message("* * * End output_offlineconversionadjustment * * *")

def output_array_of_offlineconversionadjustment(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['OfflineConversionAdjustment']:
        output_offlineconversionadjustment(data_object)

def output_offlineconversiongoal(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_offlineconversiongoal * * *")
    output_status_message("IsExternallyAttributed: {0}".format(data_object.IsExternallyAttributed))
    output_status_message("* * * End output_offlineconversiongoal * * *")

def output_array_of_offlineconversiongoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['OfflineConversionGoal']:
        output_offlineconversiongoal(data_object)

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

def output_pagesviewedpervisitgoal(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_pagesviewedpervisitgoal * * *")
    output_status_message("MinimumPagesViewed: {0}".format(data_object.MinimumPagesViewed))
    output_status_message("* * * End output_pagesviewedpervisitgoal * * *")

def output_array_of_pagesviewedpervisitgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['PagesViewedPerVisitGoal']:
        output_pagesviewedpervisitgoal(data_object)

def output_pagevisitorsrule(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_pagevisitorsrule * * *")
    output_status_message("NormalForm: {0}".format(data_object.NormalForm))
    output_status_message("RuleItemGroups:")
    output_array_of_ruleitemgroup(data_object.RuleItemGroups)
    output_status_message("* * * End output_pagevisitorsrule * * *")

def output_array_of_pagevisitorsrule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['PageVisitorsRule']:
        output_pagevisitorsrule(data_object)

def output_pagevisitorswhodidnotvisitanotherpagerule(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_pagevisitorswhodidnotvisitanotherpagerule * * *")
    output_status_message("ExcludeRuleItemGroups:")
    output_array_of_ruleitemgroup(data_object.ExcludeRuleItemGroups)
    output_status_message("IncludeRuleItemGroups:")
    output_array_of_ruleitemgroup(data_object.IncludeRuleItemGroups)
    output_status_message("* * * End output_pagevisitorswhodidnotvisitanotherpagerule * * *")

def output_array_of_pagevisitorswhodidnotvisitanotherpagerule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['PageVisitorsWhoDidNotVisitAnotherPageRule']:
        output_pagevisitorswhodidnotvisitanotherpagerule(data_object)

def output_pagevisitorswhovisitedanotherpagerule(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_pagevisitorswhovisitedanotherpagerule * * *")
    output_status_message("AnotherRuleItemGroups:")
    output_array_of_ruleitemgroup(data_object.AnotherRuleItemGroups)
    output_status_message("RuleItemGroups:")
    output_array_of_ruleitemgroup(data_object.RuleItemGroups)
    output_status_message("* * * End output_pagevisitorswhovisitedanotherpagerule * * *")

def output_array_of_pagevisitorswhovisitedanotherpagerule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['PageVisitorsWhoVisitedAnotherPageRule']:
        output_pagevisitorswhovisitedanotherpagerule(data_object)

def output_paging(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_paging * * *")
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Size: {0}".format(data_object.Size))
    output_status_message("* * * End output_paging * * *")

def output_array_of_paging(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Paging']:
        output_paging(data_object)

def output_placementexclusionlist(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_placementexclusionlist * * *")
    output_status_message("* * * End output_placementexclusionlist * * *")

def output_array_of_placementexclusionlist(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['PlacementExclusionList']:
        output_placementexclusionlist(data_object)

def output_priceadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_priceadextension * * *")
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("PriceExtensionType: {0}".format(data_object.PriceExtensionType))
    output_status_message("TableRows:")
    output_array_of_pricetablerow(data_object.TableRows)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("* * * End output_priceadextension * * *")

def output_array_of_priceadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['PriceAdExtension']:
        output_priceadextension(data_object)

def output_pricetablerow(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_pricetablerow * * *")
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("Header: {0}".format(data_object.Header))
    output_status_message("Price: {0}".format(data_object.Price))
    output_status_message("PriceQualifier: {0}".format(data_object.PriceQualifier))
    output_status_message("PriceUnit: {0}".format(data_object.PriceUnit))
    output_status_message("TermsAndConditions: {0}".format(data_object.TermsAndConditions))
    output_status_message("TermsAndConditionsUrl: {0}".format(data_object.TermsAndConditionsUrl))
    output_status_message("* * * End output_pricetablerow * * *")

def output_array_of_pricetablerow(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['PriceTableRow']:
        output_pricetablerow(data_object)

def output_productad(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_productad * * *")
    output_status_message("PromotionalText: {0}".format(data_object.PromotionalText))
    output_status_message("* * * End output_productad * * *")

def output_array_of_productad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ProductAd']:
        output_productad(data_object)

def output_productaudience(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_productaudience * * *")
    output_status_message("ProductAudienceType: {0}".format(data_object.ProductAudienceType))
    output_status_message("TagId: {0}".format(data_object.TagId))
    output_status_message("* * * End output_productaudience * * *")

def output_array_of_productaudience(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ProductAudience']:
        output_productaudience(data_object)

def output_productcondition(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_productcondition * * *")
    output_status_message("Attribute: {0}".format(data_object.Attribute))
    output_status_message("Operand: {0}".format(data_object.Operand))
    output_status_message("* * * End output_productcondition * * *")

def output_array_of_productcondition(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ProductCondition']:
        output_productcondition(data_object)

def output_productpartition(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_productpartition * * *")
    output_status_message("Condition:")
    output_productcondition(data_object.Condition)
    output_status_message("ParentCriterionId: {0}".format(data_object.ParentCriterionId))
    output_status_message("PartitionType: {0}".format(data_object.PartitionType))
    output_status_message("* * * End output_productpartition * * *")

def output_array_of_productpartition(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ProductPartition']:
        output_productpartition(data_object)

def output_productscope(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_productscope * * *")
    output_status_message("Conditions:")
    output_array_of_productcondition(data_object.Conditions)
    output_status_message("* * * End output_productscope * * *")

def output_array_of_productscope(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ProductScope']:
        output_productscope(data_object)

def output_profilecriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_profilecriterion * * *")
    output_status_message("ProfileId: {0}".format(data_object.ProfileId))
    output_status_message("ProfileType: {0}".format(data_object.ProfileType))
    output_status_message("* * * End output_profilecriterion * * *")

def output_array_of_profilecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ProfileCriterion']:
        output_profilecriterion(data_object)

def output_promotionadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_promotionadextension * * *")
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("DiscountModifier: {0}".format(data_object.DiscountModifier))
    output_status_message("FinalAppUrls:")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("MoneyAmountOff: {0}".format(data_object.MoneyAmountOff))
    output_status_message("OrdersOverAmount: {0}".format(data_object.OrdersOverAmount))
    output_status_message("PercentOff: {0}".format(data_object.PercentOff))
    output_status_message("PromotionCode: {0}".format(data_object.PromotionCode))
    output_status_message("PromotionEndDate:")
    output_date(data_object.PromotionEndDate)
    output_status_message("PromotionItem: {0}".format(data_object.PromotionItem))
    output_status_message("PromotionOccasion: {0}".format(data_object.PromotionOccasion))
    output_status_message("PromotionStartDate:")
    output_date(data_object.PromotionStartDate)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("* * * End output_promotionadextension * * *")

def output_array_of_promotionadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['PromotionAdExtension']:
        output_promotionadextension(data_object)

def output_radiuscriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_radiuscriterion * * *")
    output_status_message("LatitudeDegrees: {0}".format(data_object.LatitudeDegrees))
    output_status_message("LongitudeDegrees: {0}".format(data_object.LongitudeDegrees))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Radius: {0}".format(data_object.Radius))
    output_status_message("RadiusUnit: {0}".format(data_object.RadiusUnit))
    output_status_message("* * * End output_radiuscriterion * * *")

def output_array_of_radiuscriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['RadiusCriterion']:
        output_radiuscriterion(data_object)

def output_remarketinglist(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_remarketinglist * * *")
    output_status_message("Rule:")
    output_remarketingrule(data_object.Rule)
    output_status_message("TagId: {0}".format(data_object.TagId))
    output_status_message("* * * End output_remarketinglist * * *")

def output_array_of_remarketinglist(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['RemarketingList']:
        output_remarketinglist(data_object)

def output_remarketingrule(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_remarketingrule * * *")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'CustomEventsRule':
        output_customeventsrule(data_object)
    if data_object.Type == 'PageVisitorsRule':
        output_pagevisitorsrule(data_object)
    if data_object.Type == 'PageVisitorsWhoDidNotVisitAnotherPageRule':
        output_pagevisitorswhodidnotvisitanotherpagerule(data_object)
    if data_object.Type == 'PageVisitorsWhoVisitedAnotherPageRule':
        output_pagevisitorswhovisitedanotherpagerule(data_object)
    output_status_message("* * * End output_remarketingrule * * *")

def output_array_of_remarketingrule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['RemarketingRule']:
        output_remarketingrule(data_object)

def output_responsivead(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_responsivead * * *")
    output_status_message("BusinessName: {0}".format(data_object.BusinessName))
    output_status_message("CallToAction: {0}".format(data_object.CallToAction))
    output_status_message("CallToActionLanguage: {0}".format(data_object.CallToActionLanguage))
    output_status_message("Descriptions:")
    output_array_of_assetlink(data_object.Descriptions)
    output_status_message("Headline: {0}".format(data_object.Headline))
    output_status_message("Headlines:")
    output_array_of_assetlink(data_object.Headlines)
    output_status_message("Images:")
    output_array_of_assetlink(data_object.Images)
    output_status_message("ImpressionTrackingUrls:")
    output_array_of_string(data_object.ImpressionTrackingUrls)
    output_status_message("LongHeadline:")
    output_assetlink(data_object.LongHeadline)
    output_status_message("LongHeadlineString: {0}".format(data_object.LongHeadlineString))
    output_status_message("LongHeadlines:")
    output_array_of_assetlink(data_object.LongHeadlines)
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("Videos:")
    output_array_of_assetlink(data_object.Videos)
    output_status_message("* * * End output_responsivead * * *")

def output_array_of_responsivead(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ResponsiveAd']:
        output_responsivead(data_object)

def output_responsivesearchad(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_responsivesearchad * * *")
    output_status_message("Descriptions:")
    output_array_of_assetlink(data_object.Descriptions)
    output_status_message("Domain: {0}".format(data_object.Domain))
    output_status_message("Headlines:")
    output_array_of_assetlink(data_object.Headlines)
    output_status_message("Path1: {0}".format(data_object.Path1))
    output_status_message("Path2: {0}".format(data_object.Path2))
    output_status_message("* * * End output_responsivesearchad * * *")

def output_array_of_responsivesearchad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ResponsiveSearchAd']:
        output_responsivesearchad(data_object)

def output_reviewadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_reviewadextension * * *")
    output_status_message("IsExact: {0}".format(data_object.IsExact))
    output_status_message("Source: {0}".format(data_object.Source))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("Url: {0}".format(data_object.Url))
    output_status_message("* * * End output_reviewadextension * * *")

def output_array_of_reviewadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ReviewAdExtension']:
        output_reviewadextension(data_object)

def output_ruleitem(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_ruleitem * * *")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'StringRuleItem':
        output_stringruleitem(data_object)
    output_status_message("* * * End output_ruleitem * * *")

def output_array_of_ruleitem(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['RuleItem']:
        output_ruleitem(data_object)

def output_ruleitemgroup(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_ruleitemgroup * * *")
    output_status_message("Items:")
    output_array_of_ruleitem(data_object.Items)
    output_status_message("* * * End output_ruleitemgroup * * *")

def output_array_of_ruleitemgroup(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['RuleItemGroup']:
        output_ruleitemgroup(data_object)

def output_schedule(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_schedule * * *")
    output_status_message("DayTimeRanges:")
    output_array_of_daytime(data_object.DayTimeRanges)
    output_status_message("EndDate:")
    output_date(data_object.EndDate)
    output_status_message("StartDate:")
    output_date(data_object.StartDate)
    output_status_message("UseSearcherTimeZone: {0}".format(data_object.UseSearcherTimeZone))
    output_status_message("* * * End output_schedule * * *")

def output_array_of_schedule(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Schedule']:
        output_schedule(data_object)

def output_setting(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_setting * * *")
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'CoOpSetting':
        output_coopsetting(data_object)
    if data_object.Type == 'DynamicFeedSetting':
        output_dynamicfeedsetting(data_object)
    if data_object.Type == 'DynamicSearchAdsSetting':
        output_dynamicsearchadssetting(data_object)
    if data_object.Type == 'ShoppingSetting':
        output_shoppingsetting(data_object)
    if data_object.Type == 'TargetSetting':
        output_targetsetting(data_object)
    output_status_message("* * * End output_setting * * *")

def output_array_of_setting(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Setting']:
        output_setting(data_object)

def output_sharedentity(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_sharedentity * * *")
    output_status_message("AssociationCount: {0}".format(data_object.AssociationCount))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'SharedList':
        output_sharedlist(data_object)
    output_status_message("* * * End output_sharedentity * * *")

def output_array_of_sharedentity(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SharedEntity']:
        output_sharedentity(data_object)

def output_sharedentityassociation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_sharedentityassociation * * *")
    output_status_message("EntityId: {0}".format(data_object.EntityId))
    output_status_message("EntityType: {0}".format(data_object.EntityType))
    output_status_message("SharedEntityCustomerId: {0}".format(data_object.SharedEntityCustomerId))
    output_status_message("SharedEntityId: {0}".format(data_object.SharedEntityId))
    output_status_message("SharedEntityType: {0}".format(data_object.SharedEntityType))
    output_status_message("* * * End output_sharedentityassociation * * *")

def output_array_of_sharedentityassociation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SharedEntityAssociation']:
        output_sharedentityassociation(data_object)

def output_sharedlist(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_sharedlist * * *")
    output_status_message("ItemCount: {0}".format(data_object.ItemCount))
    if data_object.Type == 'NegativeKeywordList':
        output_negativekeywordlist(data_object)
    if data_object.Type == 'PlacementExclusionList':
        output_placementexclusionlist(data_object)
    output_status_message("* * * End output_sharedlist * * *")

def output_array_of_sharedlist(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SharedList']:
        output_sharedlist(data_object)

def output_sharedlistitem(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_sharedlistitem * * *")
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("Type: {0}".format(data_object.Type))
    if data_object.Type == 'NegativeKeyword':
        output_negativekeyword(data_object)
    if data_object.Type == 'NegativeSite':
        output_negativesite(data_object)
    output_status_message("* * * End output_sharedlistitem * * *")

def output_array_of_sharedlistitem(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SharedListItem']:
        output_sharedlistitem(data_object)

def output_shoppingsetting(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_shoppingsetting * * *")
    output_status_message("LocalInventoryAdsEnabled: {0}".format(data_object.LocalInventoryAdsEnabled))
    output_status_message("Priority: {0}".format(data_object.Priority))
    output_status_message("SalesCountryCode: {0}".format(data_object.SalesCountryCode))
    output_status_message("StoreId: {0}".format(data_object.StoreId))
    output_status_message("* * * End output_shoppingsetting * * *")

def output_array_of_shoppingsetting(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ShoppingSetting']:
        output_shoppingsetting(data_object)

def output_similarremarketinglist(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_similarremarketinglist * * *")
    output_status_message("SourceId: {0}".format(data_object.SourceId))
    output_status_message("* * * End output_similarremarketinglist * * *")

def output_array_of_similarremarketinglist(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SimilarRemarketingList']:
        output_similarremarketinglist(data_object)

def output_sitelinkadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_sitelinkadextension * * *")
    output_status_message("Description1: {0}".format(data_object.Description1))
    output_status_message("Description2: {0}".format(data_object.Description2))
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("DisplayText: {0}".format(data_object.DisplayText))
    output_status_message("FinalAppUrls:")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("* * * End output_sitelinkadextension * * *")

def output_array_of_sitelinkadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['SitelinkAdExtension']:
        output_sitelinkadextension(data_object)

def output_storecriterion(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_storecriterion * * *")
    output_status_message("StoreId: {0}".format(data_object.StoreId))
    output_status_message("* * * End output_storecriterion * * *")

def output_array_of_storecriterion(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['StoreCriterion']:
        output_storecriterion(data_object)

def output_stringruleitem(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_stringruleitem * * *")
    output_status_message("Operand: {0}".format(data_object.Operand))
    output_status_message("Operator: {0}".format(data_object.Operator))
    output_status_message("Value: {0}".format(data_object.Value))
    output_status_message("* * * End output_stringruleitem * * *")

def output_array_of_stringruleitem(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['StringRuleItem']:
        output_stringruleitem(data_object)

def output_structuredsnippetadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_structuredsnippetadextension * * *")
    output_status_message("Header: {0}".format(data_object.Header))
    output_status_message("Values:")
    output_array_of_string(data_object.Values)
    output_status_message("* * * End output_structuredsnippetadextension * * *")

def output_array_of_structuredsnippetadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['StructuredSnippetAdExtension']:
        output_structuredsnippetadextension(data_object)

def output_targetcpabiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_targetcpabiddingscheme * * *")
    output_status_message("MaxCpc:")
    output_bid(data_object.MaxCpc)
    output_status_message("TargetCpa: {0}".format(data_object.TargetCpa))
    output_status_message("* * * End output_targetcpabiddingscheme * * *")

def output_array_of_targetcpabiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['TargetCpaBiddingScheme']:
        output_targetcpabiddingscheme(data_object)

def output_targetimpressionsharebiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_targetimpressionsharebiddingscheme * * *")
    output_status_message("MaxCpc:")
    output_bid(data_object.MaxCpc)
    output_status_message("TargetAdPosition: {0}".format(data_object.TargetAdPosition))
    output_status_message("TargetImpressionShare: {0}".format(data_object.TargetImpressionShare))
    output_status_message("* * * End output_targetimpressionsharebiddingscheme * * *")

def output_array_of_targetimpressionsharebiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['TargetImpressionShareBiddingScheme']:
        output_targetimpressionsharebiddingscheme(data_object)

def output_targetroasbiddingscheme(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_targetroasbiddingscheme * * *")
    output_status_message("MaxCpc:")
    output_bid(data_object.MaxCpc)
    output_status_message("TargetRoas: {0}".format(data_object.TargetRoas))
    output_status_message("* * * End output_targetroasbiddingscheme * * *")

def output_array_of_targetroasbiddingscheme(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['TargetRoasBiddingScheme']:
        output_targetroasbiddingscheme(data_object)

def output_targetsetting(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_targetsetting * * *")
    output_status_message("Details:")
    output_array_of_targetsettingdetail(data_object.Details)
    output_status_message("* * * End output_targetsetting * * *")

def output_array_of_targetsetting(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['TargetSetting']:
        output_targetsetting(data_object)

def output_targetsettingdetail(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_targetsettingdetail * * *")
    output_status_message("CriterionTypeGroup: {0}".format(data_object.CriterionTypeGroup))
    output_status_message("TargetAndBid: {0}".format(data_object.TargetAndBid))
    output_status_message("* * * End output_targetsettingdetail * * *")

def output_array_of_targetsettingdetail(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['TargetSettingDetail']:
        output_targetsettingdetail(data_object)

def output_textad(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_textad * * *")
    output_status_message("DestinationUrl: {0}".format(data_object.DestinationUrl))
    output_status_message("DisplayUrl: {0}".format(data_object.DisplayUrl))
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("Title: {0}".format(data_object.Title))
    output_status_message("* * * End output_textad * * *")

def output_array_of_textad(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['TextAd']:
        output_textad(data_object)

def output_textasset(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_textasset * * *")
    output_status_message("Text: {0}".format(data_object.Text))
    output_status_message("* * * End output_textasset * * *")

def output_array_of_textasset(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['TextAsset']:
        output_textasset(data_object)

def output_uettag(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_uettag * * *")
    output_status_message("CustomerShare:")
    output_customershare(data_object.CustomerShare)
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("TrackingNoScript: {0}".format(data_object.TrackingNoScript))
    output_status_message("TrackingScript: {0}".format(data_object.TrackingScript))
    output_status_message("TrackingStatus: {0}".format(data_object.TrackingStatus))
    output_status_message("* * * End output_uettag * * *")

def output_array_of_uettag(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['UetTag']:
        output_uettag(data_object)

def output_urlgoal(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_urlgoal * * *")
    output_status_message("UrlExpression: {0}".format(data_object.UrlExpression))
    output_status_message("UrlOperator: {0}".format(data_object.UrlOperator))
    output_status_message("* * * End output_urlgoal * * *")

def output_array_of_urlgoal(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['UrlGoal']:
        output_urlgoal(data_object)

def output_video(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_video * * *")
    output_status_message("AspectRatio: {0}".format(data_object.AspectRatio))
    output_status_message("CreatedDateTimeInUTC: {0}".format(data_object.CreatedDateTimeInUTC))
    output_status_message("Description: {0}".format(data_object.Description))
    output_status_message("DurationInMilliseconds: {0}".format(data_object.DurationInMilliseconds))
    output_status_message("FailureCode: {0}".format(data_object.FailureCode))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("ModifiedDateTimeInUTC: {0}".format(data_object.ModifiedDateTimeInUTC))
    output_status_message("SourceUrl: {0}".format(data_object.SourceUrl))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("ThumbnailUrl: {0}".format(data_object.ThumbnailUrl))
    output_status_message("Url: {0}".format(data_object.Url))
    output_status_message("* * * End output_video * * *")

def output_array_of_video(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Video']:
        output_video(data_object)

def output_videoadextension(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_videoadextension * * *")
    output_status_message("ActionText: {0}".format(data_object.ActionText))
    output_status_message("AlternativeText: {0}".format(data_object.AlternativeText))
    output_status_message("DisplayText: {0}".format(data_object.DisplayText))
    output_status_message("FinalAppUrls:")
    output_array_of_appurl(data_object.FinalAppUrls)
    output_status_message("FinalMobileUrls:")
    output_array_of_string(data_object.FinalMobileUrls)
    output_status_message("FinalUrlSuffix: {0}".format(data_object.FinalUrlSuffix))
    output_status_message("FinalUrls:")
    output_array_of_string(data_object.FinalUrls)
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("ThumbnailId: {0}".format(data_object.ThumbnailId))
    output_status_message("ThumbnailUrl: {0}".format(data_object.ThumbnailUrl))
    output_status_message("TrackingUrlTemplate: {0}".format(data_object.TrackingUrlTemplate))
    output_status_message("UrlCustomParameters:")
    output_customparameters(data_object.UrlCustomParameters)
    output_status_message("VideoId: {0}".format(data_object.VideoId))
    output_status_message("* * * End output_videoadextension * * *")

def output_array_of_videoadextension(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['VideoAdExtension']:
        output_videoadextension(data_object)

def output_videoasset(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_videoasset * * *")
    output_status_message("SubType: {0}".format(data_object.SubType))
    output_status_message("ThumbnailImage:")
    output_imageasset(data_object.ThumbnailImage)
    output_status_message("* * * End output_videoasset * * *")

def output_array_of_videoasset(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['VideoAsset']:
        output_videoasset(data_object)

def output_webpage(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_webpage * * *")
    output_status_message("Parameter:")
    output_webpageparameter(data_object.Parameter)
    output_status_message("* * * End output_webpage * * *")

def output_array_of_webpage(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Webpage']:
        output_webpage(data_object)

def output_webpagecondition(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_webpagecondition * * *")
    output_status_message("Argument: {0}".format(data_object.Argument))
    output_status_message("Operand: {0}".format(data_object.Operand))
    output_status_message("* * * End output_webpagecondition * * *")

def output_array_of_webpagecondition(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['WebpageCondition']:
        output_webpagecondition(data_object)

def output_webpageparameter(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_webpageparameter * * *")
    output_status_message("Conditions:")
    output_array_of_webpagecondition(data_object.Conditions)
    output_status_message("CriterionName: {0}".format(data_object.CriterionName))
    output_status_message("* * * End output_webpageparameter * * *")

def output_array_of_webpageparameter(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['WebpageParameter']:
        output_webpageparameter(data_object)

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

def output_calltoaction(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_calltoaction(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CallToAction:\n")
    for value_set in value_sets['CallToAction']:
        output_calltoaction(value_set)

def output_languagename(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_languagename(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of LanguageName:\n")
    for value_set in value_sets['LanguageName']:
        output_languagename(value_set)

def output_assetlinkeditorialstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_assetlinkeditorialstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AssetLinkEditorialStatus:\n")
    for value_set in value_sets['AssetLinkEditorialStatus']:
        output_assetlinkeditorialstatus(value_set)

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

def output_dynamicsearchadssource(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_dynamicsearchadssource(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DynamicSearchAdsSource:\n")
    for value_set in value_sets['DynamicSearchAdsSource']:
        output_dynamicsearchadssource(value_set)

def output_criteriontypegroup(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_criteriontypegroup(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CriterionTypeGroup:\n")
    for value_set in value_sets['CriterionTypeGroup']:
        output_criteriontypegroup(value_set)

def output_bidoption(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_bidoption(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BidOption:\n")
    for value_set in value_sets['BidOption']:
        output_bidoption(value_set)

def output_campaignadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_campaignadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CampaignAdditionalField:\n")
    for value_set in value_sets['CampaignAdditionalField']:
        output_campaignadditionalfield(value_set)

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

def output_adgroupprivacystatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adgroupprivacystatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdGroupPrivacyStatus:\n")
    for value_set in value_sets['AdGroupPrivacyStatus']:
        output_adgroupprivacystatus(value_set)

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

def output_adadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdAdditionalField:\n")
    for value_set in value_sets['AdAdditionalField']:
        output_adadditionalfield(value_set)

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

def output_actionadextensionactiontype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_actionadextensionactiontype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ActionAdExtensionActionType:\n")
    for value_set in value_sets['ActionAdExtensionActionType']:
        output_actionadextensionactiontype(value_set)

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

def output_promotiondiscountmodifier(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_promotiondiscountmodifier(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of PromotionDiscountModifier:\n")
    for value_set in value_sets['PromotionDiscountModifier']:
        output_promotiondiscountmodifier(value_set)

def output_promotionoccasion(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_promotionoccasion(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of PromotionOccasion:\n")
    for value_set in value_sets['PromotionOccasion']:
        output_promotionoccasion(value_set)

def output_adextensionheadertype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adextensionheadertype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdExtensionHeaderType:\n")
    for value_set in value_sets['AdExtensionHeaderType']:
        output_adextensionheadertype(value_set)

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

def output_adextensionadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_adextensionadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AdExtensionAdditionalField:\n")
    for value_set in value_sets['AdExtensionAdditionalField']:
        output_adextensionadditionalfield(value_set)

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

def output_criterionadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_criterionadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CriterionAdditionalField:\n")
    for value_set in value_sets['CriterionAdditionalField']:
        output_criterionadditionalfield(value_set)

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

def output_profiletype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_profiletype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ProfileType:\n")
    for value_set in value_sets['ProfileType']:
        output_profiletype(value_set)

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

def output_bmcstoreadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_bmcstoreadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BMCStoreAdditionalField:\n")
    for value_set in value_sets['BMCStoreAdditionalField']:
        output_bmcstoreadditionalfield(value_set)

def output_bmcstoresubtype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_bmcstoresubtype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of BMCStoreSubType:\n")
    for value_set in value_sets['BMCStoreSubType']:
        output_bmcstoresubtype(value_set)

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

def output_normalform(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_normalform(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of NormalForm:\n")
    for value_set in value_sets['NormalForm']:
        output_normalform(value_set)

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

def output_productaudiencetype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_productaudiencetype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ProductAudienceType:\n")
    for value_set in value_sets['ProductAudienceType']:
        output_productaudiencetype(value_set)

def output_logicaloperator(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_logicaloperator(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of LogicalOperator:\n")
    for value_set in value_sets['LogicalOperator']:
        output_logicaloperator(value_set)

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

def output_conversiongoaladditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_conversiongoaladditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ConversionGoalAdditionalField:\n")
    for value_set in value_sets['ConversionGoalAdditionalField']:
        output_conversiongoaladditionalfield(value_set)

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

def output_conversiongoalcategory(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_conversiongoalcategory(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ConversionGoalCategory:\n")
    for value_set in value_sets['ConversionGoalCategory']:
        output_conversiongoalcategory(value_set)

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

def output_importadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_importadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ImportAdditionalField:\n")
    for value_set in value_sets['ImportAdditionalField']:
        output_importadditionalfield(value_set)

def output_importentitytype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_importentitytype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ImportEntityType:\n")
    for value_set in value_sets['ImportEntityType']:
        output_importentitytype(value_set)

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
