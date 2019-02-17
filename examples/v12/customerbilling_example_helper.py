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

def output_apibatchfault(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_apibatchfault * * *")
    output_status_message("BatchErrors:")
    output_array_of_batcherror(data_object.BatchErrors)
    output_status_message("* * * End output_apibatchfault * * *")

def output_array_of_apibatchfault(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ApiBatchFault']:
        output_apibatchfault(data_object)

def output_apifault(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_apifault * * *")
    output_status_message("OperationErrors:")
    output_array_of_operationerror(data_object.OperationErrors)
    if data_object.Type == 'ApiBatchFault':
        output_apibatchfault(data_object)
    output_status_message("* * * End output_apifault * * *")

def output_array_of_apifault(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ApiFault']:
        output_apifault(data_object)

def output_applicationfault(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_applicationfault * * *")
    output_status_message("TrackingId: {0}".format(data_object.TrackingId))
    if data_object.Type == 'AdApiFaultDetail':
        output_adapifaultdetail(data_object)
    if data_object.Type == 'ApiFault':
        output_apifault(data_object)
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
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Message: {0}".format(data_object.Message))
    output_status_message("* * * End output_batcherror * * *")

def output_array_of_batcherror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BatchError']:
        output_batcherror(data_object)

def output_billingdocument(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_billingdocument * * *")
    output_status_message("Data: {0}".format(data_object.Data))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("* * * End output_billingdocument * * *")

def output_array_of_billingdocument(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BillingDocument']:
        output_billingdocument(data_object)

def output_billingdocumentinfo(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_billingdocumentinfo * * *")
    output_status_message("AccountId: {0}".format(data_object.AccountId))
    output_status_message("AccountName: {0}".format(data_object.AccountName))
    output_status_message("AccountNumber: {0}".format(data_object.AccountNumber))
    output_status_message("Amount: {0}".format(data_object.Amount))
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("DocumentDate: {0}".format(data_object.DocumentDate))
    output_status_message("DocumentId: {0}".format(data_object.DocumentId))
    output_status_message("CustomerId: {0}".format(data_object.CustomerId))
    output_status_message("* * * End output_billingdocumentinfo * * *")

def output_array_of_billingdocumentinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['BillingDocumentInfo']:
        output_billingdocumentinfo(data_object)

def output_insertionorder(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_insertionorder * * *")
    output_status_message("AccountId: {0}".format(data_object.AccountId))
    output_status_message("BalanceAmount: {0}".format(data_object.BalanceAmount))
    output_status_message("BookingCountryCode: {0}".format(data_object.BookingCountryCode))
    output_status_message("Comment: {0}".format(data_object.Comment))
    output_status_message("EndDate: {0}".format(data_object.EndDate))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("LastModifiedByUserId: {0}".format(data_object.LastModifiedByUserId))
    output_status_message("LastModifiedTime: {0}".format(data_object.LastModifiedTime))
    output_status_message("NotificationThreshold: {0}".format(data_object.NotificationThreshold))
    output_status_message("ReferenceId: {0}".format(data_object.ReferenceId))
    output_status_message("SpendCapAmount: {0}".format(data_object.SpendCapAmount))
    output_status_message("StartDate: {0}".format(data_object.StartDate))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("PurchaseOrder: {0}".format(data_object.PurchaseOrder))
    output_status_message("PendingChanges:")
    output_insertionorderpendingchanges(data_object.PendingChanges)
    output_status_message("* * * End output_insertionorder * * *")

def output_array_of_insertionorder(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['InsertionOrder']:
        output_insertionorder(data_object)

def output_insertionorderpendingchanges(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_insertionorderpendingchanges * * *")
    output_status_message("Comment: {0}".format(data_object.Comment))
    output_status_message("EndDate: {0}".format(data_object.EndDate))
    output_status_message("RequestedByUserId: {0}".format(data_object.RequestedByUserId))
    output_status_message("ModifiedDateTime: {0}".format(data_object.ModifiedDateTime))
    output_status_message("NotificationThreshold: {0}".format(data_object.NotificationThreshold))
    output_status_message("ReferenceId: {0}".format(data_object.ReferenceId))
    output_status_message("SpendCapAmount: {0}".format(data_object.SpendCapAmount))
    output_status_message("StartDate: {0}".format(data_object.StartDate))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("PurchaseOrder: {0}".format(data_object.PurchaseOrder))
    output_status_message("ChangeStatus: {0}".format(data_object.ChangeStatus))
    output_status_message("* * * End output_insertionorderpendingchanges * * *")

def output_array_of_insertionorderpendingchanges(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['InsertionOrderPendingChanges']:
        output_insertionorderpendingchanges(data_object)

def output_operationerror(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_operationerror * * *")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("Message: {0}".format(data_object.Message))
    output_status_message("* * * End output_operationerror * * *")

def output_array_of_operationerror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['OperationError']:
        output_operationerror(data_object)

def output_orderby(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_orderby * * *")
    output_status_message("Field: {0}".format(data_object.Field))
    output_status_message("Order: {0}".format(data_object.Order))
    output_status_message("* * * End output_orderby * * *")

def output_array_of_orderby(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['OrderBy']:
        output_orderby(data_object)

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

def output_predicate(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_predicate * * *")
    output_status_message("Field: {0}".format(data_object.Field))
    output_status_message("Operator: {0}".format(data_object.Operator))
    output_status_message("Value: {0}".format(data_object.Value))
    output_status_message("* * * End output_predicate * * *")

def output_array_of_predicate(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Predicate']:
        output_predicate(data_object)

def output_datatype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_datatype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of DataType:\n")
    for value_set in value_sets['DataType']:
        output_datatype(value_set)

def output_insertionorderstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_insertionorderstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of InsertionOrderStatus:\n")
    for value_set in value_sets['InsertionOrderStatus']:
        output_insertionorderstatus(value_set)

def output_insertionorderpendingchangesstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_insertionorderpendingchangesstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of InsertionOrderPendingChangesStatus:\n")
    for value_set in value_sets['InsertionOrderPendingChangesStatus']:
        output_insertionorderpendingchangesstatus(value_set)

def output_predicateoperator(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_predicateoperator(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of PredicateOperator:\n")
    for value_set in value_sets['PredicateOperator']:
        output_predicateoperator(value_set)

def output_orderbyfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_orderbyfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of OrderByField:\n")
    for value_set in value_sets['OrderByField']:
        output_orderbyfield(value_set)

def output_sortorder(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_sortorder(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of SortOrder:\n")
    for value_set in value_sets['SortOrder']:
        output_sortorder(value_set)

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
