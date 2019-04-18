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

def output_applicationfault(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_applicationfault * * *")
    output_status_message("TrackingId: {0}".format(data_object.TrackingId))
    if data_object.Type == 'AdApiFaultDetail':
        output_adapifaultdetail(data_object)
    if data_object.Type == 'ApiFaultDetail':
        output_apifaultdetail(data_object)
    output_status_message("* * * End output_applicationfault * * *")

def output_array_of_applicationfault(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ApplicationFault']:
        output_applicationfault(data_object)

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

def output_campaignscope(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_campaignscope * * *")
    output_status_message("CampaignId: {0}".format(data_object.CampaignId))
    output_status_message("ParentAccountId: {0}".format(data_object.ParentAccountId))
    output_status_message("* * * End output_campaignscope * * *")

def output_array_of_campaignscope(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CampaignScope']:
        output_campaignscope(data_object)

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
        output_status_message("{0}".format(item))
def output_array_of_string(items):
    if items is None or items['string'] is None:
        return
    output_status_message("Array Of string:")
    for item in items['string']:
        output_status_message("{0}".format(item))
def output_status_message(message):
    print(message)
