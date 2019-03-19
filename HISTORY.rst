.. :changelog:

Release History
-----------
12.0.4(2019-03-15)
+++++++++++++++++++
* Updated service proxies to reflect recent interface changes. For details please see the Bing Ads API Release Notes: https://docs.microsoft.com/en-us/bingads/guides/release-notes.
* Added a new Bulk property for Action Text i.e., added ActionText to the existing BulkActionAdExtension.
* Removed the is_expired property from BulkAdGroup. Use the Status property of the BulkAdGroup instead. 
* For optional fields, the Bulk file schema mapping is updated such that "delete_value" will only be written to the file for update operations. Update intent is assumed when the Bulk entity ID is greater than zero. 
* Updated the Status mapping for BulkExperiment i.e., map the string value directly instead of via bulk_optional_str. 


12.0.3.1(2019-02-01)
+++++++++++++++++++
* Fix import issue introduced by version 12.0.3, in which version python 3 users will see error "ImportError: No module named 'bulk_ad_group_negative_audience_association". See issue: https://github.com/BingAds/BingAds-Python-SDK/issues/110.

12.0.3(2019-01-10)
+++++++++++++++++++
* BREAKING CHANGE for BulkAdGroupCustomAudienceAssociation, BulkAdGroupInMarketAudienceAssociation, BulkAdGroupNegativeCustomAudienceAssociation, BulkAdGroupNegativeInMarketAudienceAssociation, BulkAdGroupNegativeProductAudienceAssociation, BulkAdGroupNegativeRemarketingListAssociation, BulkAdGroupNegativeSimilarRemarketingListAssociation, BulkAdGroupProductAudienceAssociation, BulkAdGroupRemarketingListAssociation, and BulkAdGroupSimilarRemarketingListAssociation: Replaced custom_audience_name, in_market_audience_name, product_audience_name, remarketing_list_name, and similar_remarketing_list_name with audience_name. The audience_name property is now used to map from the 'Audience Name' field of a Bulk file via all audience association SDK objects. 
* Updated service proxies to reflect recent interface changes. For details please see the release notes: https://docs.microsoft.com/en-us/bingads/guides/release-notes.
* Added Bulk mapping for responsive ad images i.e., added Images to the existing BulkResponsiveAd.
* Added Bulk mapping for campaign target setting i.e., added TargetSetting to the existing BulkCampaign.
* Added Bulk mapping for campaign level audience associations i.e.,BulkCampaignCustomAudienceAssociation, BulkCampaignInMarketAudienceAssociation, BulkCampaignNegativeCustomAudienceAssociation, BulkCampaignNegativeInMarketAudienceAssociation, BulkCampaignNegativeProductAudienceAssociation, BulkCampaignNegativeRemarketingListAssociation, BulkCampaignNegativeSimilarRemarketingListAssociation, BulkCampaignProductAudienceAssociation, BulkCampaignRemarketingListAssociation, and BulkCampaignSimilarRemarketingListAssociation. 
* Added the get_response_header method in class ServiceClient, to access the service TrackingId, etc per GitHub issue https://github.com/BingAds/BingAds-Python-SDK/issues/106. 

12.0.2(2018-12-10)
+++++++++++++++++++
*Updated service proxies to reflect recent interface changes. For details please see the Bing Ads API Release Notes: https://docs.microsoft.com/en-us/bingads/guides/release-notes.
*Added Bulk mapping for campaign experiments i.e., BulkExperiment and BulkCampaign.
*Added Bulk mapping for action ad extensions i.e., BulkActionAdExtension, BulkAccountActionAdExtension, BulkAdGroupActionAdExtension, and BulkCampaignActionAdExtension. 

-----------
12.0.1(2018-11-10)
+++++++++++++++++++
*Removed support for Bing Ads API Version 11, per the October 31, 2018 sunset. 
*Added Bulk mapping for responsive search ads i.e., BulkResponsiveSearchAd and BulkResponsiveSearchAdLabel.
*Added all fragments returned via the tokens request as a new property in the OAuthTokens SDK class.

-----------
11.12.7(2018-10-10)
+++++++++++++++++++
*Update service proxies to reflect recent interface changes.
*Map TitlePart3 and TextPart2 to BulkExpandedTextAd.

-----------
11.12.6(2018-09-10)
+++++++++++++++++++
*Updated service proxies to reflect recent Bulk, Campaign Management, Customer Management, and Reporting API changes. 
*Added Bulk mapping for similar remarketing lists i.e., BulkSimilarRemarketingList, BulkAdGroupSimilarRemarketingListAssociation, and BulkAdGroupNegativeSimilarRemarketingListAssociation.

-----------
11.12.5(2018-08-10)
+++++++++++++++++++
*Updated service proxies to support customer address, campaign level profile criteria, similar audiences for remarketing lists, and new change history report columns. For details see the service release notes: https://docs.microsoft.com/en-us/bingads/guides/release-notes?view=bingads-12#august2018. 
*Added BulkEntity mappings for campaign level profile criteria i.e., added BulkCampaignCompanyNameCriterion, BulkCampaignJobFunctionCriterion, and BulkCampaignIndustryCriterion. 

-----------
11.12.4(2018-07-10)
+++++++++++++++++++
* Added a mapping for the Domain column in the Bulk file to the BulkExpandedTextAd object.
* Limited the scope to bingads.manage for access token requests. Previously the default scope was used, which can vary if a user granted your app permissions to multiple scopes. The Bing Ads SDKs only support the bingads.manage scope. 
* Updated the Customer Management proxies to support LinkedAccountIds for agencies. For agency users the customer role can contain a list of linked accounts that the user can access as an agency on behalf of another customer. 

-----------
11.12.3(2018-06-10)
+++++++++++++++++++
* Added support for Cooperative bidding e.g., added mappings for "Bid Boost Value", "Bid Option" and "Maximum Bid" fields via the BulkAdGroup. 
* Added mappings for the 'MSCLKID Auto Tagging Enabled" and "Tracking Tempalte" fields via the BulkAccount.

-----------
11.12.2(2018-05-15)
+++++++++++++++++++
*To extend support for Microsoft Audience Ads, new bulk objects are added to the SDK for reading and writing Bulk file records e.g., BulkResponsiveAd and BulkResponsiveAdLabel. 
*Added retries for the 117 throttling error if encountered while polling for the status of a bulk or reporting operation. 

---------------
11.12.1(2018-04-12)
+++++++++++++++++++
*Added support for Bing Ads API Version 12. For more information, see Migrating to Bing Ads API Version 12.
*The version parameter is now required when creating each ServiceClient. Previously the version was optional and defaulted to version 11. The version parameter is moved to the second position between the service client name and the authorization data. 
*The file_type parameter now defaults to 'Csv' as an *str* datatype instead of the DownloadFileType for BulkFileReader, BulkServiceManager, DownloadParameters and SubmitDownloadParameters. You can set 'Tsv' if you prefer the tab separated file format type.  

---------------
11.5.9(2018-03-12)
+++++++++++++++++++
*Updated to support Microsoft Account authentication in sandbox. 

---------------
11.5.8(2018-01-12)
+++++++++++++++++++
*The Bulk and Campaign Management proxies are updated to support audience search size. In addition the SDK supports audience search size via the BulkCustomAudience, BulkInMarketAudience, and BulkRemarketingList classes.
	
*Allow the Parent Id to be empty when deleting Bulk entities. Previously the Parent Id was required by the SDK although the Bulk service does not always require it.

---------------
11.5.7(2017-12-12)
+++++++++++++++++++

*The Version 11 Reporting service proxies are updated to support new columns for Estimated Bids. 

11.5.6(2017-11-01)
+++++++++++++++++++

* Support for version 9 and 10 ended on October 31st, 2017. The following version 9 and 10 proxies are now removed from the SDK. You must upgrade to version 11.
  - Removed the Version 9 proxies for Customer Billing, Customer Management, and Reporting services. Also removed the Version 9 ReportingServiceManager.
  - Removed the Version 10 proxies for Ad Insight, Bulk, and Campaign Management services. Also removed the Version 10 BulkServiceManager and Version 10 Bulk entities.
* The Version 11 Reporting service proxies are updated to support new columns for Exact Match Impression Share Percent and Labels.
* Improved memory usage for decompressing the bulk and report files.
* Set the default encoding to utf-8-sig and removed the chardet requirement. Bulk file download and upload should always be UTF-8 encoding with BOM.

11.5.5.1(2017-09-19)
+++++++++++++++++++

* Fix user-agent including '\n' character issue introduced by 11.5.5. Only (Major, Minor, Micro) tuple will be added into user-agent.

11.5.5(2017-09-13)
+++++++++++++++++++

* The Reporting service proxies are updated to support new columns for location targeting.


11.5.4(2017-08-08)
+++++++++++++++++++

* The Campaign Management service proxies are updated to support inherited bid strategy type.
* The Reporting service proxies are updated to support new columns for Bing Shopping campaigns.
* New version 11 bulk labels objects are added i.e., *BulkLabel*, *BulkCampaignLabel*, *BulkAdGroupLabel*, *BulkKeywordLabel*, *BulkAppInstallAdLabel*, *BulkDynamicSearchAdLabel*, *BulkExpandedTextAdLabel*, *BulkProductAdLabel*, and *BulkTextAdLabel* objects are added to the SDK for reading and writing the corresponding Bulk file records.
* A new version 11 bulk offline conversion object is added i.e., the *BulkOfflineConversion* object is added to the SDK for writing and uploading the corresponding Bulk file record.


10.4.12(2017-02-28)
+++++++++++++++++++

* Support Remarketing list bulk upload
* Add Remarketing Rule in bulk schema

10.4.11(2016-12-30)
+++++++++++++++++++

* Add bulk support for Dynamic Search Ads feature
* Update wsdl proxy to latest version
* Bug fixes

10.4.10(2016-10-28)
+++++++++++++++++++

* Update wsdl proxy for Dynamic Search Ads Bulk
* Update wsdl proxy for Remarketing Add/Update/Delete APIs

10.4.9(2016-09-29)
++++++++++++++++++

* Update wsdl proxy for Dynamic Search Ads APIs
* Update wsdl proxy for Remarketing

10.4.8(2016-08-29)
++++++++++++++++++

* Add Sitelink2 Ad Extension
* Add Budget
* Add Budget Id in Campaign for Shared Budget
* Add Scheduling in Ad Extensions
* Update wsdl proxy to latest version

10.4.7(2016-07-28)
++++++++++++++++++

* Add Remarketing List and Ad Group Remarketing List Association
* Add Expanded Text Ad
* Add Structured Snippet Ad Extension
* Update wsdl proxy to latest version

10.4.6(2016-07-18)
++++++++++++++++++

* Fix Reporting Service default version bug

10.4.5(2016-06-30)
++++++++++++++++++

* Sunset campaign management, bulk, ad intelligence, optimizer services in v9
* Add Ad Format Preference in Text Ad
* Add Bid Strategy Type in Campaign, AdGroup and Keyword
* Updated wsdl proxy to latest version
* Bug fixes

10.4.4(2016-05-30)
++++++++++++++++++

* Add App Install Ad support
* Add state property in OAuthAuthorization classes
* Support oauth_tokens initialization in Authentication classes
* Updated wsdl proxy to latest version

10.4.3(2016-04-30)
++++++++++++++++++

* Changed condition to write delete value for Keyword Bid in bulk
* Support suds option in BulkServiceManager and ReportingServiceManager
* Updated wsdl proxy to latest version
* Bug fixes

10.4.2(2016-03-30)
++++++++++++++++++

* Add suds option parameter to support timeout and location settings in soap service
* Add timeout logic for bulk upload, bulk download and report download methods
* Add retry logic for upload and download status tracking
* New exception types to handle bulk and reporting errors
* Remove location_target_version parameter from DownloadParameters and SubmitDownloadParameters
* Updated wsdl proxy file to latest version

10.4.1(2015-10-23)
++++++++++++++++++

* Support Bing Ads API V10 and upgrade bulk format version to 4.0
* Compatible with Bing Ads API V9
* Add Reporting Service support to SDK 9.3
* Bug Fixes

9.3.4 (2015-08-20)
++++++++++++++++++

* Replace SSLv3 with SSLv23 for TLS support


9.3.3 (2015-07-31)
++++++++++++++++++

* Add Bing Shopping Campaign Support
* Add Native Ads Support


9.3.2 (2015-04-24)
++++++++++++++++++

* Add App AdExtension support.
* Bug Fixes.

9.3.1 (2015-03-31)
++++++++++++++++++

* First release on PyPI.
