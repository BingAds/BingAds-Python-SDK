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

def output_campaignscope(data_object):
    if data_object is None:
        return
    output_status_message("CampaignScope (Data Object):")
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("ParentAccountId: {0}".format(data_object.ParentAccountId))

def output_array_of_campaignscope(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of CampaignScope:\n")
    for data_object in data_objects['CampaignScope']:
        output_campaignscope(data_object)
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

def output_performancestatsdaterange(data_object):
    if data_object is None:
        return
    output_status_message("PerformanceStatsDateRange (Data Object):")
    output_status_message("CustomDateRangeEnd (Element Name):")
    output_date(data_object.CustomDateRangeEnd)
    output_status_message("CustomDateRangeStart (Element Name):")
    output_date(data_object.CustomDateRangeStart)
    output_status_message("PredefinedTime: {0}".format(data_object.PredefinedTime))

def output_array_of_performancestatsdaterange(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of PerformanceStatsDateRange:\n")
    for data_object in data_objects['PerformanceStatsDateRange']:
        output_performancestatsdaterange(data_object)
        output_status_message("\n")

def output_compressiontype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_compressiontype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CompressionType:\n")
    for value_set in value_sets['CompressionType']:
        output_compressiontype(value_set)

def output_datascope(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_datascope(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DataScope:\n")
    for value_set in value_sets['DataScope']:
        output_datascope(value_set)

def output_downloadentity(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_downloadentity(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DownloadEntity:\n")
    for value_set in value_sets['DownloadEntity']:
        output_downloadentity(value_set)

def output_downloadfiletype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_downloadfiletype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DownloadFileType:\n")
    for value_set in value_sets['DownloadFileType']:
        output_downloadfiletype(value_set)

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

def output_responsemode(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_responsemode(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ResponseMode:\n")
    for value_set in value_sets['ResponseMode']:
        output_responsemode(value_set)

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
