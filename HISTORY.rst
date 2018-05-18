.. :changelog:

Release History
-----------
11.12.2(2018-05-15)
+++++++++++++++++++
*To extend support for [Microsoft Audience Ads](https://docs.microsoft.com/en-us/bingads/guides/audience-ads), new bulk objects are added to the SDK for reading and writing Bulk file records e.g., BulkResponsiveAd and BulkResponsiveAdLabel. 
*Added retries for the 117 throttling error if encountered while polling for the status of a bulk or reporting operation. 

---------------
11.12.1(2018-04-12)
+++++++++++++++++++
*Added support for Bing Ads API Version 12. For more information, see [Migrating to Bing Ads API Version 12](https://docs.microsoft.com/en-us/bingads/guides/migration-guide).
*The version parameter is now required when creating each ServiceClient. Previously the version was optional and defaulted to version 11. The version parameter is moved to the second position between the service client name and the authorization data. 
*The file_type parameter now defaults to 'Csv' as an *str* datatype instead of the DownloadFileType for BulkFileReader, BulkServiceManager, DownloadParameters and SubmitDownloadParameters. You can set 'Tsv' if you prefer the tab separated file format type.  

---------------
11.5.9(2018-03-12)
+++++++++++++++++++
*Updated to support [Microsoft Account authentication in sandbox](https://docs.microsoft.com/en-us/bingads/guides/sandbox.md#access). 

---------------
11.5.8(2018-01-12)
+++++++++++++++++++
*The Bulk and Campaign Management proxies are updated to support [audience search size](https://docs.microsoft.com/en-us/bingads/guides/release-notes#audiencesearchsize-january2018). In addition the SDK supports audience search size via the BulkCustomAudience, BulkInMarketAudience, and BulkRemarketingList classes.
	
*Allow the Parent Id to be empty when deleting Bulk entities. Previously the Parent Id was required by the SDK although the Bulk service does not always require it.

---------------
11.5.7(2017-12-12)
+++++++++++++++++++

*The Version 11 Reporting service proxies are updated to support new columns for [Estimated Bids](https://docs.microsoft.com/en-us/bingads/guides/release-notes#reporting-estimatedbids-november2017). 

11.5.6(2017-11-01)
+++++++++++++++++++

* Support for version 9 and 10 ended on October 31st, 2017. The following version 9 and 10 proxies are now removed from the SDK. You must upgrade to version 11.
  - Removed the Version 9 proxies for Customer Billing, Customer Management, and Reporting services. Also removed the Version 9 ReportingServiceManager.
  - Removed the Version 10 proxies for Ad Insight, Bulk, and Campaign Management services. Also removed the Version 10 BulkServiceManager and Version 10 Bulk entities.
* The Version 11 Reporting service proxies are updated to support new columns for [Exact Match Impression Share Percent](https://docs.microsoft.com/en-us/bingads/guides/release-notes#reporting-exactmatchimpressionshare-october2017) and [Labels](https://docs.microsoft.com/en-us/bingads/guides/release-notes#reporting-labels-october2017).
* Improved memory usage for decompressing the bulk and report files.
* Set the default encoding to utf-8-sig and removed the chardet requirement. Bulk file download and upload should always be UTF-8 encoding with BOM.

11.5.5.1(2017-09-19)
+++++++++++++++++++

* Fix user-agent including '\n' character issue introduced by 11.5.5. Only (Major, Minor, Micro) tuple will be added into user-agent.

11.5.5(2017-09-13)
+++++++++++++++++++

* The [Reporting]( https://msdn.microsoft.com/library/bing-ads-overview-release-notes.aspx#reporting_locations_august2017) service proxies are updated to support new columns for location targeting.


11.5.4(2017-08-08)
+++++++++++++++++++

* The [Campaign Management]( https://msdn.microsoft.com/library/bing-ads-overview-release-notes.aspx#inheritedbidstrategytype_july2017) service proxies are updated to support inherited bid strategy type.
* The [Reporting]( https://msdn.microsoft.com/library/bing-ads-overview-release-notes.aspx#reporting_bsc_july2017) service proxies are updated to support new columns for Bing Shopping campaigns.
* New version 11 bulk labels objects are added i.e., *BulkLabel*, *BulkCampaignLabel*, *BulkAdGroupLabel*, *BulkKeywordLabel*, *BulkAppInstallAdLabel*, *BulkDynamicSearchAdLabel*, *BulkExpandedTextAdLabel*, *BulkProductAdLabel*, and *BulkTextAdLabel* objects are added to the SDK for reading and writing the corresponding [Bulk file records]( https://msdn.microsoft.com/library/bing-ads-overview-release-notes.aspx#bulk_v11_labels_july2017).
* A new version 11 bulk offline conversion object is added i.e., the *BulkOfflineConversion* object is added to the SDK for writing and uploading the corresponding [Bulk file record]( https://msdn.microsoft.com/library/bing-ads-overview-release-notes.aspx#bulk_v11_offline_conversions_july2017).


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
