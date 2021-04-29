REM Campaign Mangement Service
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://campaign.api.sandbox.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v13/CampaignManagementService.svc?singleWsdl" -path "bingads\v13\proxies\sandbox\campaignmanagement_service.xml"
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://campaign.api.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v13/CampaignManagementService.svc?singleWsdl" -path "bingads\v13\proxies\production\campaignmanagement_service.xml"

REM Bulk Service 
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://bulk.api.sandbox.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v13/BulkService.svc?singleWsdl" -path "bingads\v13\proxies\sandbox\bulk_service.xml"
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://bulk.api.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v13/BulkService.svc?singleWsdl" -path "bingads\v13\proxies\production\bulk_service.xml"

REM customerbilling Service
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://clientcenter.api.sandbox.bingads.microsoft.com/Api/Billing/v13/CustomerBillingService.svc?singleWsdl" -path "bingads\v13\proxies\sandbox\customerbilling_service.xml"
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://clientcenter.api.bingads.microsoft.com/Api/Billing/v13/CustomerBillingService.svc?singleWsdl" -path "bingads\v13\proxies\production\customerbilling_service.xml"

REM customermanagement Service
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://clientcenter.api.sandbox.bingads.microsoft.com/Api/CustomerManagement/v13/CustomerManagementService.svc?singleWsdl" -path "bingads\v13\proxies\sandbox\customermanagement_service.xml"
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://clientcenter.api.bingads.microsoft.com/Api/CustomerManagement/v13/CustomerManagementService.svc?singleWsdl" -path "bingads\v13\proxies\production\customermanagement_service.xml"

REM reporting Service
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://reporting.api.sandbox.bingads.microsoft.com/Api/Advertiser/Reporting/v13/ReportingService.svc?singleWsdl" -path "bingads\v13\proxies\sandbox\reporting_service.xml"
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://reporting.api.bingads.microsoft.com/Api/Advertiser/Reporting/v13/ReportingService.svc?singleWsdl" -path "bingads\v13\proxies\production\reporting_service.xml"

REM adinsight Service
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://adinsight.api.sandbox.bingads.microsoft.com/Api/Advertiser/AdInsight/v13/AdInsightService.svc?singleWsdl" -path "bingads\v13\proxies\sandbox\adinsight_service.xml"
Powershell.exe -executionpolicy remotesigned -File .\generate_proxies.ps1 -svcWsdl "https://adinsight.api.bingads.microsoft.com/Api/Advertiser/AdInsight/v13/AdInsightService.svc?singleWsdl" -path "bingads\v13\proxies\production\adinsight_service.xml"


pause