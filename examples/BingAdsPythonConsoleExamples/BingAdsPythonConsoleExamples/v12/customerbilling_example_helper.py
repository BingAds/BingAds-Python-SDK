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

def output_apibatchfault(data_object):
    if data_object is None:
        return
    output_status_message("ApiBatchFault (Data Object):")
    output_status_message("BatchErrors (Element Name):")
    output_array_of_batcherror(data_object.BatchErrors)

def output_array_of_apibatchfault(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ApiBatchFault:\n")
    for data_object in data_objects['ApiBatchFault']:
        output_apibatchfault(data_object)
        output_status_message("\n")

def output_apifault(data_object):
    if data_object is None:
        return
    output_status_message("ApiFault (Data Object):")
    output_status_message("OperationErrors (Element Name):")
    output_array_of_operationerror(data_object.OperationErrors)
    if data_object.Type == 'ApiBatchFault':
        output_apibatchfault(data_object)

def output_array_of_apifault(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of ApiFault:\n")
    for data_object in data_objects['ApiFault']:
        output_apifault(data_object)
        output_status_message("\n")

def output_applicationfault(data_object):
    if data_object is None:
        return
    output_status_message("ApplicationFault (Data Object):")
    output_status_message("TrackingId: {0}".format(data_object.TrackingId))
    if data_object.Type == 'AdApiFaultDetail':
        output_adapifaultdetail(data_object)
    if data_object.Type == 'ApiFault':
        output_apifault(data_object)

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
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Message: {0}".format(data_object.Message))

def output_array_of_batcherror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BatchError:\n")
    for data_object in data_objects['BatchError']:
        output_batcherror(data_object)
        output_status_message("\n")

def output_billingdocument(data_object):
    if data_object is None:
        return
    output_status_message("BillingDocument (Data Object):")
    output_status_message("Data: {0}".format(data_object.Data))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Type: {0}".format(data_object.Type))

def output_array_of_billingdocument(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BillingDocument:\n")
    for data_object in data_objects['BillingDocument']:
        output_billingdocument(data_object)
        output_status_message("\n")

def output_billingdocumentinfo(data_object):
    if data_object is None:
        return
    output_status_message("BillingDocumentInfo (Data Object):")
    output_status_message("AccountId: {0}".format(data_object.AccountId))
    output_status_message("AccountName: {0}".format(data_object.AccountName))
    output_status_message("AccountNumber: {0}".format(data_object.AccountNumber))
    output_status_message("Amount: {0}".format(data_object.Amount))
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("DocumentDate: {0}".format(data_object.DocumentDate))
    output_status_message("DocumentId: {0}".format(data_object.DocumentId))
    output_status_message("CustomerId: {0}".format(data_object.CustomerId))

def output_array_of_billingdocumentinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of BillingDocumentInfo:\n")
    for data_object in data_objects['BillingDocumentInfo']:
        output_billingdocumentinfo(data_object)
        output_status_message("\n")

def output_insertionorder(data_object):
    if data_object is None:
        return
    output_status_message("InsertionOrder (Data Object):")
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
    output_status_message("PendingChanges (Element Name):")
    output_insertionorderpendingchanges(data_object.PendingChanges)

def output_array_of_insertionorder(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of InsertionOrder:\n")
    for data_object in data_objects['InsertionOrder']:
        output_insertionorder(data_object)
        output_status_message("\n")

def output_insertionorderpendingchanges(data_object):
    if data_object is None:
        return
    output_status_message("InsertionOrderPendingChanges (Data Object):")
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

def output_array_of_insertionorderpendingchanges(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of InsertionOrderPendingChanges:\n")
    for data_object in data_objects['InsertionOrderPendingChanges']:
        output_insertionorderpendingchanges(data_object)
        output_status_message("\n")

def output_operationerror(data_object):
    if data_object is None:
        return
    output_status_message("OperationError (Data Object):")
    output_status_message("Code: {0}".format(data_object.Code))
    output_status_message("Details: {0}".format(data_object.Details))
    output_status_message("Message: {0}".format(data_object.Message))

def output_array_of_operationerror(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of OperationError:\n")
    for data_object in data_objects['OperationError']:
        output_operationerror(data_object)
        output_status_message("\n")

def output_orderby(data_object):
    if data_object is None:
        return
    output_status_message("OrderBy (Data Object):")
    output_status_message("Field: {0}".format(data_object.Field))
    output_status_message("Order: {0}".format(data_object.Order))

def output_array_of_orderby(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of OrderBy:\n")
    for data_object in data_objects['OrderBy']:
        output_orderby(data_object)
        output_status_message("\n")

def output_paging(data_object):
    if data_object is None:
        return
    output_status_message("Paging (Data Object):")
    output_status_message("Index: {0}".format(data_object.Index))
    output_status_message("Size: {0}".format(data_object.Size))

def output_array_of_paging(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Paging:\n")
    for data_object in data_objects['Paging']:
        output_paging(data_object)
        output_status_message("\n")

def output_predicate(data_object):
    if data_object is None:
        return
    output_status_message("Predicate (Data Object):")
    output_status_message("Field: {0}".format(data_object.Field))
    output_status_message("Operator: {0}".format(data_object.Operator))
    output_status_message("Value: {0}".format(data_object.Value))

def output_array_of_predicate(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    output_status_message("Array Of Predicate:\n")
    for data_object in data_objects['Predicate']:
        output_predicate(data_object)
        output_status_message("\n")

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
        output_status_message("Value of the long: {0}".format(item))
def output_array_of_string(items):
    if items is None or items['string'] is None:
        return
    output_status_message("Array Of string:")
    for item in items['string']:
        output_status_message("Value of the string: {0}".format(item))
def output_status_message(message):
    print(message)
