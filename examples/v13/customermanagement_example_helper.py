def output_accountinfo(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_accountinfo * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Number: {0}".format(data_object.Number))
    output_status_message("AccountLifeCycleStatus: {0}".format(data_object.AccountLifeCycleStatus))
    output_status_message("PauseReason: {0}".format(data_object.PauseReason))
    output_status_message("* * * End output_accountinfo * * *")

def output_array_of_accountinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AccountInfo']:
        output_accountinfo(data_object)

def output_accountinfowithcustomerdata(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_accountinfowithcustomerdata * * *")
    output_status_message("CustomerId: {0}".format(data_object.CustomerId))
    output_status_message("CustomerName: {0}".format(data_object.CustomerName))
    output_status_message("AccountId: {0}".format(data_object.AccountId))
    output_status_message("AccountName: {0}".format(data_object.AccountName))
    output_status_message("AccountNumber: {0}".format(data_object.AccountNumber))
    output_status_message("AccountLifeCycleStatus: {0}".format(data_object.AccountLifeCycleStatus))
    output_status_message("PauseReason: {0}".format(data_object.PauseReason))
    output_status_message("AccountMode: {0}".format(data_object.AccountMode))
    output_status_message("* * * End output_accountinfowithcustomerdata * * *")

def output_array_of_accountinfowithcustomerdata(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AccountInfoWithCustomerData']:
        output_accountinfowithcustomerdata(data_object)

def output_accounttaxcertificate(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_accounttaxcertificate * * *")
    output_status_message("TaxCertificateBlobContainerName: {0}".format(data_object.TaxCertificateBlobContainerName))
    output_status_message("TaxCertificates:")
    output_array_of_keyvaluepairofstringbase64binary(data_object.TaxCertificates)
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("* * * End output_accounttaxcertificate * * *")

def output_array_of_accounttaxcertificate(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AccountTaxCertificate']:
        output_accounttaxcertificate(data_object)

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

def output_address(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_address * * *")
    output_status_message("City: {0}".format(data_object.City))
    output_status_message("CountryCode: {0}".format(data_object.CountryCode))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Line1: {0}".format(data_object.Line1))
    output_status_message("Line2: {0}".format(data_object.Line2))
    output_status_message("Line3: {0}".format(data_object.Line3))
    output_status_message("Line4: {0}".format(data_object.Line4))
    output_status_message("PostalCode: {0}".format(data_object.PostalCode))
    output_status_message("StateOrProvince: {0}".format(data_object.StateOrProvince))
    output_status_message("TimeStamp: {0}".format(data_object.TimeStamp))
    output_status_message("BusinessName: {0}".format(data_object.BusinessName))
    output_status_message("* * * End output_address * * *")

def output_array_of_address(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Address']:
        output_address(data_object)

def output_advertiseraccount(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_advertiseraccount * * *")
    output_status_message("BillToCustomerId: {0}".format(data_object.BillToCustomerId))
    output_status_message("CurrencyCode: {0}".format(data_object.CurrencyCode))
    output_status_message("AccountFinancialStatus: {0}".format(data_object.AccountFinancialStatus))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Language: {0}".format(data_object.Language))
    output_status_message("LastModifiedByUserId: {0}".format(data_object.LastModifiedByUserId))
    output_status_message("LastModifiedTime: {0}".format(data_object.LastModifiedTime))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("Number: {0}".format(data_object.Number))
    output_status_message("ParentCustomerId: {0}".format(data_object.ParentCustomerId))
    output_status_message("PaymentMethodId: {0}".format(data_object.PaymentMethodId))
    output_status_message("PaymentMethodType: {0}".format(data_object.PaymentMethodType))
    output_status_message("PrimaryUserId: {0}".format(data_object.PrimaryUserId))
    output_status_message("AccountLifeCycleStatus: {0}".format(data_object.AccountLifeCycleStatus))
    output_status_message("TimeStamp: {0}".format(data_object.TimeStamp))
    output_status_message("TimeZone: {0}".format(data_object.TimeZone))
    output_status_message("PauseReason: {0}".format(data_object.PauseReason))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("LinkedAgencies:")
    output_array_of_customerinfo(data_object.LinkedAgencies)
    output_status_message("SalesHouseCustomerId: {0}".format(data_object.SalesHouseCustomerId))
    output_status_message("TaxInformation:")
    output_array_of_keyvaluepairofstringstring(data_object.TaxInformation)
    output_status_message("BackUpPaymentInstrumentId: {0}".format(data_object.BackUpPaymentInstrumentId))
    output_status_message("BillingThresholdAmount: {0}".format(data_object.BillingThresholdAmount))
    output_status_message("BusinessAddress:")
    output_address(data_object.BusinessAddress)
    output_status_message("AutoTagType: {0}".format(data_object.AutoTagType))
    output_status_message("SoldToPaymentInstrumentId: {0}".format(data_object.SoldToPaymentInstrumentId))
    output_status_message("TaxCertificate:")
    output_accounttaxcertificate(data_object.TaxCertificate)
    output_status_message("AccountMode: {0}".format(data_object.AccountMode))
    output_status_message("* * * End output_advertiseraccount * * *")

def output_array_of_advertiseraccount(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['AdvertiserAccount']:
        output_advertiseraccount(data_object)

def output_apifault(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_apifault * * *")
    output_status_message("OperationErrors:")
    output_array_of_operationerror(data_object.OperationErrors)
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

def output_clientlink(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_clientlink * * *")
    output_status_message("Type: {0}".format(data_object.Type))
    output_status_message("ClientEntityId: {0}".format(data_object.ClientEntityId))
    output_status_message("ClientEntityNumber: {0}".format(data_object.ClientEntityNumber))
    output_status_message("ClientEntityName: {0}".format(data_object.ClientEntityName))
    output_status_message("ManagingCustomerId: {0}".format(data_object.ManagingCustomerId))
    output_status_message("ManagingCustomerNumber: {0}".format(data_object.ManagingCustomerNumber))
    output_status_message("ManagingCustomerName: {0}".format(data_object.ManagingCustomerName))
    output_status_message("Note: {0}".format(data_object.Note))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("InviterEmail: {0}".format(data_object.InviterEmail))
    output_status_message("InviterName: {0}".format(data_object.InviterName))
    output_status_message("InviterPhone: {0}".format(data_object.InviterPhone))
    output_status_message("IsBillToClient: {0}".format(data_object.IsBillToClient))
    output_status_message("StartDate: {0}".format(data_object.StartDate))
    output_status_message("Status: {0}".format(data_object.Status))
    output_status_message("SuppressNotification: {0}".format(data_object.SuppressNotification))
    output_status_message("LastModifiedDateTime: {0}".format(data_object.LastModifiedDateTime))
    output_status_message("LastModifiedByUserId: {0}".format(data_object.LastModifiedByUserId))
    output_status_message("Timestamp: {0}".format(data_object.Timestamp))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("CustomerLinkPermission: {0}".format(data_object.CustomerLinkPermission))
    output_status_message("* * * End output_clientlink * * *")

def output_array_of_clientlink(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ClientLink']:
        output_clientlink(data_object)

def output_contactinfo(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_contactinfo * * *")
    output_status_message("Address:")
    output_address(data_object.Address)
    output_status_message("ContactByPhone: {0}".format(data_object.ContactByPhone))
    output_status_message("ContactByPostalMail: {0}".format(data_object.ContactByPostalMail))
    output_status_message("Email: {0}".format(data_object.Email))
    output_status_message("EmailFormat: {0}".format(data_object.EmailFormat))
    output_status_message("Fax: {0}".format(data_object.Fax))
    output_status_message("HomePhone: {0}".format(data_object.HomePhone))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Mobile: {0}".format(data_object.Mobile))
    output_status_message("Phone1: {0}".format(data_object.Phone1))
    output_status_message("Phone2: {0}".format(data_object.Phone2))
    output_status_message("* * * End output_contactinfo * * *")

def output_array_of_contactinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['ContactInfo']:
        output_contactinfo(data_object)

def output_customer(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customer * * *")
    output_status_message("CustomerFinancialStatus: {0}".format(data_object.CustomerFinancialStatus))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Industry: {0}".format(data_object.Industry))
    output_status_message("LastModifiedByUserId: {0}".format(data_object.LastModifiedByUserId))
    output_status_message("LastModifiedTime: {0}".format(data_object.LastModifiedTime))
    output_status_message("MarketCountry: {0}".format(data_object.MarketCountry))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("MarketLanguage: {0}".format(data_object.MarketLanguage))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("ServiceLevel: {0}".format(data_object.ServiceLevel))
    output_status_message("CustomerLifeCycleStatus: {0}".format(data_object.CustomerLifeCycleStatus))
    output_status_message("TimeStamp: {0}".format(data_object.TimeStamp))
    output_status_message("Number: {0}".format(data_object.Number))
    output_status_message("CustomerAddress:")
    output_address(data_object.CustomerAddress)
    output_status_message("* * * End output_customer * * *")

def output_array_of_customer(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['Customer']:
        output_customer(data_object)

def output_customerinfo(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customerinfo * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("Name: {0}".format(data_object.Name))
    output_status_message("* * * End output_customerinfo * * *")

def output_array_of_customerinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CustomerInfo']:
        output_customerinfo(data_object)

def output_customerrole(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_customerrole * * *")
    output_status_message("RoleId: {0}".format(data_object.RoleId))
    output_status_message("CustomerId: {0}".format(data_object.CustomerId))
    output_status_message("AccountIds:")
    output_array_of_long(data_object.AccountIds)
    output_status_message("LinkedAccountIds:")
    output_array_of_long(data_object.LinkedAccountIds)
    output_status_message("CustomerLinkPermission: {0}".format(data_object.CustomerLinkPermission))
    output_status_message("* * * End output_customerrole * * *")

def output_array_of_customerrole(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['CustomerRole']:
        output_customerrole(data_object)

def output_daterange(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_daterange * * *")
    output_status_message("MinDate: {0}".format(data_object.MinDate))
    output_status_message("MaxDate: {0}".format(data_object.MaxDate))
    output_status_message("* * * End output_daterange * * *")

def output_array_of_daterange(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['DateRange']:
        output_daterange(data_object)

def output_keyvaluepairofstringbase64binary(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_keyvaluepairofstringbase64binary * * *")
    output_status_message("key: {0}".format(data_object.key))
    output_status_message("value: {0}".format(data_object.value))
    output_status_message("* * * End output_keyvaluepairofstringbase64binary * * *")

def output_array_of_keyvaluepairofstringbase64binary(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['KeyValuePairOfstringbase64Binary']:
        output_keyvaluepairofstringbase64binary(data_object)

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

def output_personname(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_personname * * *")
    output_status_message("FirstName: {0}".format(data_object.FirstName))
    output_status_message("LastName: {0}".format(data_object.LastName))
    output_status_message("MiddleInitial: {0}".format(data_object.MiddleInitial))
    output_status_message("* * * End output_personname * * *")

def output_array_of_personname(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['PersonName']:
        output_personname(data_object)

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

def output_user(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_user * * *")
    output_status_message("ContactInfo:")
    output_contactinfo(data_object.ContactInfo)
    output_status_message("CustomerId: {0}".format(data_object.CustomerId))
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("JobTitle: {0}".format(data_object.JobTitle))
    output_status_message("LastModifiedByUserId: {0}".format(data_object.LastModifiedByUserId))
    output_status_message("LastModifiedTime: {0}".format(data_object.LastModifiedTime))
    output_status_message("Lcid: {0}".format(data_object.Lcid))
    output_status_message("Name:")
    output_personname(data_object.Name)
    output_status_message("Password: {0}".format(data_object.Password))
    output_status_message("SecretAnswer: {0}".format(data_object.SecretAnswer))
    output_status_message("SecretQuestion: {0}".format(data_object.SecretQuestion))
    output_status_message("UserLifeCycleStatus: {0}".format(data_object.UserLifeCycleStatus))
    output_status_message("TimeStamp: {0}".format(data_object.TimeStamp))
    output_status_message("UserName: {0}".format(data_object.UserName))
    output_status_message("ForwardCompatibilityMap:")
    output_array_of_keyvaluepairofstringstring(data_object.ForwardCompatibilityMap)
    output_status_message("* * * End output_user * * *")

def output_array_of_user(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['User']:
        output_user(data_object)

def output_userinfo(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_userinfo * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("UserName: {0}".format(data_object.UserName))
    output_status_message("* * * End output_userinfo * * *")

def output_array_of_userinfo(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['UserInfo']:
        output_userinfo(data_object)

def output_userinvitation(data_object):
    if data_object is None:
        return
    output_status_message("* * * Begin output_userinvitation * * *")
    output_status_message("Id: {0}".format(data_object.Id))
    output_status_message("FirstName: {0}".format(data_object.FirstName))
    output_status_message("LastName: {0}".format(data_object.LastName))
    output_status_message("Email: {0}".format(data_object.Email))
    output_status_message("CustomerId: {0}".format(data_object.CustomerId))
    output_status_message("RoleId: {0}".format(data_object.RoleId))
    output_status_message("AccountIds:")
    output_array_of_long(data_object.AccountIds)
    output_status_message("ExpirationDate: {0}".format(data_object.ExpirationDate))
    output_status_message("Lcid: {0}".format(data_object.Lcid))
    output_status_message("* * * End output_userinvitation * * *")

def output_array_of_userinvitation(data_objects):
    if data_objects is None or len(data_objects) == 0:
        return
    for data_object in data_objects['UserInvitation']:
        output_userinvitation(data_object)

def output_accountlifecyclestatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_accountlifecyclestatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AccountLifeCycleStatus:\n")
    for value_set in value_sets['AccountLifeCycleStatus']:
        output_accountlifecyclestatus(value_set)

def output_currencycode(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_currencycode(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CurrencyCode:\n")
    for value_set in value_sets['CurrencyCode']:
        output_currencycode(value_set)

def output_accountfinancialstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_accountfinancialstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AccountFinancialStatus:\n")
    for value_set in value_sets['AccountFinancialStatus']:
        output_accountfinancialstatus(value_set)

def output_languagetype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_languagetype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of LanguageType:\n")
    for value_set in value_sets['LanguageType']:
        output_languagetype(value_set)

def output_paymentmethodtype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_paymentmethodtype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of PaymentMethodType:\n")
    for value_set in value_sets['PaymentMethodType']:
        output_paymentmethodtype(value_set)

def output_timezonetype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_timezonetype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of TimeZoneType:\n")
    for value_set in value_sets['TimeZoneType']:
        output_timezonetype(value_set)

def output_autotagtype(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_autotagtype(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AutoTagType:\n")
    for value_set in value_sets['AutoTagType']:
        output_autotagtype(value_set)

def output_taxcertificatestatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_taxcertificatestatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of TaxCertificateStatus:\n")
    for value_set in value_sets['TaxCertificateStatus']:
        output_taxcertificatestatus(value_set)

def output_customerfinancialstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_customerfinancialstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CustomerFinancialStatus:\n")
    for value_set in value_sets['CustomerFinancialStatus']:
        output_customerfinancialstatus(value_set)

def output_industry(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_industry(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of Industry:\n")
    for value_set in value_sets['Industry']:
        output_industry(value_set)

def output_servicelevel(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_servicelevel(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ServiceLevel:\n")
    for value_set in value_sets['ServiceLevel']:
        output_servicelevel(value_set)

def output_customerlifecyclestatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_customerlifecyclestatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of CustomerLifeCycleStatus:\n")
    for value_set in value_sets['CustomerLifeCycleStatus']:
        output_customerlifecyclestatus(value_set)

def output_lcid(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_lcid(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of LCID:\n")
    for value_set in value_sets['LCID']:
        output_lcid(value_set)

def output_accountadditionalfield(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_accountadditionalfield(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of AccountAdditionalField:\n")
    for value_set in value_sets['AccountAdditionalField']:
        output_accountadditionalfield(value_set)

def output_emailformat(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_emailformat(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of EmailFormat:\n")
    for value_set in value_sets['EmailFormat']:
        output_emailformat(value_set)

def output_secretquestion(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_secretquestion(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of SecretQuestion:\n")
    for value_set in value_sets['SecretQuestion']:
        output_secretquestion(value_set)

def output_userlifecyclestatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_userlifecyclestatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of UserLifeCycleStatus:\n")
    for value_set in value_sets['UserLifeCycleStatus']:
        output_userlifecyclestatus(value_set)

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

def output_clientlinkstatus(value_set):
    output_status_message("Values in {0}".format(value_set.Type))
    for value in value_set['string']:
        output_status_message(value)

def output_array_of_clientlinkstatus(value_sets):
    if value_sets is None or len(value_sets) == 0:
        return
    output_status_message("Array Of ClientLinkStatus:\n")
    for value_set in value_sets['ClientLinkStatus']:
        output_clientlinkstatus(value_set)

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
