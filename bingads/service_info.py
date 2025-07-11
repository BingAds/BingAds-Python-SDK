import sys

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

_SERVICE_LIST = ['adinsight', 'bulk', 'campaignmanagement', 'customerbilling', 'customermanagement', 'reporting']

SERVICE_INFO_DICT_V13 = {}

for service in _SERVICE_LIST:
    SERVICE_INFO_DICT_V13[(service, 'production')] = 'file:///' + importlib_resources.files('bingads', 'v13/proxies/production/%s_service.xml' % (service))
    SERVICE_INFO_DICT_V13[(service, 'sandbox')] = 'file:///' + importlib_resources.files('bingads', 'v13/proxies/sandbox/%s_service.xml' % (service))

SERVICE_INFO_DICT = {13: SERVICE_INFO_DICT_V13}
