import pkg_resources

_SERVICE_LIST = ['adinsight', 'bulk', 'campaignmanagement', 'customerbilling', 'customermanagement', 'reporting']

SERVICE_INFO_DICT_V13 = {}

for service in _SERVICE_LIST:
    SERVICE_INFO_DICT_V13[(service, 'production')] = 'file:///' + pkg_resources.resource_filename('bingads', 'v13/proxies/production/%s_service.xml' % (service))
    SERVICE_INFO_DICT_V13[(service, 'sandbox')] = 'file:///' + pkg_resources.resource_filename('bingads', 'v13/proxies/sandbox/%s_service.xml' % (service))

SERVICE_INFO_DICT = {13: SERVICE_INFO_DICT_V13}
