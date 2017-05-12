class _ServiceInfo:

    @property
    def name(self):
        return self._name

    @property
    def env(self):
        return self._env

    @property
    def url(self):
        return self._url

    def __init__(self, name, env, url):
        self._name = name
        self._env = env
        self._url = url


_SERVICE_INFO_LIST = [
    # customer billing
    _ServiceInfo(
        "customerbilling",
        "production",
        "https://clientcenter.api.bingads.microsoft.com/Api/Billing/v9/CustomerBillingService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "customerbilling",
        "sandbox",
        "https://clientcenter.api.sandbox.bingads.microsoft.com/Api/Billing/v9/CustomerBillingService.svc?singleWsdl"
    ),

    # customer management
    _ServiceInfo(
        "customermanagement",
        "production",
        "https://clientcenter.api.bingads.microsoft.com/Api/CustomerManagement/v9/CustomerManagementService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "customermanagement",
        "sandbox",
        "https://clientcenter.api.sandbox.bingads.microsoft.com/Api/CustomerManagement/v9/CustomerManagementService.svc?singleWsdl"
    ),

    # reporting
    _ServiceInfo(
        "reporting",
        "production",
        "https://api.bingads.microsoft.com/Api/Advertiser/Reporting/v9/ReportingService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "reporting",
        "sandbox",
        "https://api.sandbox.bingads.microsoft.com/Api/Advertiser/Reporting/v9/ReportingService.svc?singleWsdl"
    ),
]


SERVICE_INFO_DICT = {}

for service_info in _SERVICE_INFO_LIST:
    SERVICE_INFO_DICT[(service_info.name, service_info.env)] = service_info

_SERVICE_INFO_LIST_V10 = [
    # ad insight service
    _ServiceInfo(
        "adinsight",
        "production",
        "https://adinsight.api.bingads.microsoft.com/Api/Advertiser/AdInsight/V10/AdInsightService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "adinsight",
        "sandbox",
        "https://adinsight.api.sandbox.bingads.microsoft.com/Api/Advertiser/AdInsight/V10/AdInsightService.svc?singleWsdl"
    ),

    # bulk service
    _ServiceInfo(
        "bulk",
        "production",
        "https://bulk.api.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v10/BulkService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "bulk",
        "sandbox",
        "https://bulk.api.sandbox.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v10/BulkService.svc?singleWsdl"
    ),

    # campaign management
    _ServiceInfo(
        "campaignmanagement",
        "production",
        "https://campaign.api.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v10/CampaignManagementService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "campaignmanagement",
        "sandbox",
        "https://campaign.api.sandbox.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v10/CampaignManagementService.svc?singleWsdl"
    ),
]

SERVICE_INFO_DICT_V10 = {}

for service_info in _SERVICE_INFO_LIST_V10:
    SERVICE_INFO_DICT_V10[(service_info.name, service_info.env)] = service_info

_SERVICE_INFO_LIST_V11 = [
    # ad insight service
    _ServiceInfo(
        "adinsight",
        "production",
        "https://adinsight.api.bingads.microsoft.com/Api/Advertiser/AdInsight/V11/AdInsightService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "adinsight",
        "sandbox",
        "https://adinsight.api.sandbox.bingads.microsoft.com/Api/Advertiser/AdInsight/V11/AdInsightService.svc?singleWsdl"
    ),

    # bulk service
    _ServiceInfo(
        "bulk",
        "production",
        "https://bulk.api.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v11/BulkService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "bulk",
        "sandbox",
        "https://bulk.api.sandbox.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v11/BulkService.svc?singleWsdl"
    ),

    # campaign management
    _ServiceInfo(
        "campaignmanagement",
        "production",
        "https://campaign.api.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v11/CampaignManagementService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "campaignmanagement",
        "sandbox",
        "https://campaign.api.sandbox.bingads.microsoft.com/Api/Advertiser/CampaignManagement/v11/CampaignManagementService.svc?singleWsdl"
    ),

    # customer billing
    _ServiceInfo(
        "customerbilling",
        "production",
        "https://clientcenter.api.bingads.microsoft.com/Api/Billing/v11/CustomerBillingService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "customerbilling",
        "sandbox",
        "https://clientcenter.api.sandbox.bingads.microsoft.com/Api/Billing/v11/CustomerBillingService.svc?singleWsdl"
    ),

    # customer management
    _ServiceInfo(
        "customermanagement",
        "production",
        "https://clientcenter.api.bingads.microsoft.com/Api/CustomerManagement/v11/CustomerManagementService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "customermanagement",
        "sandbox",
        "https://clientcenter.api.sandbox.bingads.microsoft.com/Api/CustomerManagement/v11/CustomerManagementService.svc?singleWsdl"
    ),

    # reporting
    _ServiceInfo(
        "reporting",
        "production",
        "https://reporting.api.bingads.microsoft.com/Api/Advertiser/Reporting/v11/ReportingService.svc?singleWsdl"
    ),
    _ServiceInfo(
        "reporting",
        "sandbox",
        "https://reporting.api.sandbox.bingads.microsoft.com/Api/Advertiser/Reporting/v11/ReportingService.svc?singleWsdl"
    ),
]

SERVICE_INFO_DICT_V11 = {}

for service_info in _SERVICE_INFO_LIST_V11:
    SERVICE_INFO_DICT_V11[(service_info.name, service_info.env)] = service_info
