from bingads.service_client import ServiceClient
from bingads.authorization import *
from bingads import *
from bingads.reporting import *

import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    ENVIRONMENT='production'
    DEVELOPER_TOKEN='YourDeveloperTokenGoesHere'
    CLIENT_ID='YourClientIdGoesHere'   


    # The directory for the report file.
    FILE_DIRECTORY='c:/reports/'

    # The name of the report file.
    RESULT_FILE_NAME='result.csv'

    # The report file extension type.
    REPORT_FILE_FORMAT = 'Csv'

    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    customer_service=ServiceClient(
        'CustomerManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=9,
    )

    

    reporting_service_manager=ReportingServiceManager(
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=1000, 
        environment=ENVIRONMENT,
    )

    # In addition to ReportingServiceManager, you will need a reporting ServiceClient 
    # to build the ReportRequest.

    reporting_service=ServiceClient(
        'ReportingService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=9,
    )
    
def authenticate_with_username():
    ''' 
    Sets the authentication property of the global AuthorizationData instance with PasswordAuthentication.
    '''
    global authorization_data
    authentication=PasswordAuthentication(
        user_name='UserNameGoesHere',
        password='PasswordGoesHere'
    )

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication

def authenticate_with_oauth():
    ''' 
    Sets the authentication property of the global AuthorizationData instance with OAuthDesktopMobileAuthCodeGrant.
    '''
    global authorization_data
    authentication=OAuthDesktopMobileAuthCodeGrant(
        client_id=CLIENT_ID
    )

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication   

    # Register the callback function to automatically save the refresh token anytime it is refreshed.
    # Uncomment this line if you want to store your refresh token. Be sure to save your refresh token securely.
    authorization_data.authentication.token_refreshed_callback=save_refresh_token
    
    refresh_token=get_refresh_token()
    
    # If we have a refresh token let's refresh it
    if refresh_token is not None:
        authentication.request_oauth_tokens_by_refresh_token(refresh_token)
    else:
        webbrowser.open(authentication.get_authorization_endpoint(), new=1)
        # For Python 3.x use 'input' instead of 'raw_input'
        if(sys.version_info.major >= 3):
            response_uri=input(
                "You need to provide consent for the application to access your Bing Ads accounts. " \
                "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
                "please enter the response URI that includes the authorization 'code' parameter: \n"
            )
        else:
            response_uri=raw_input(
                "You need to provide consent for the application to access your Bing Ads accounts. " \
                "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
                "please enter the response URI that includes the authorization 'code' parameter: \n"
            )

        # Request access and refresh tokens using the URI that you provided manually during program execution.
        authentication.request_oauth_tokens_by_response_uri(response_uri=response_uri) 

def get_refresh_token():
    ''' 
    Returns a refresh token if stored locally.
    '''
    file=None
    try:
        file=open("refresh.txt")
        line=file.readline()
        file.close()
        return line if line else None
    except IOError:
        if file:
            file.close()
        return None

def save_refresh_token(oauth_tokens):
    ''' 
    Stores a refresh token locally. Be sure to save your refresh token securely.
    '''
    with open("refresh.txt","w+") as file:
        file.write(oauth_tokens.refresh_token)
        file.close()
    return None

def search_accounts_by_user_id(user_id):
    ''' 
    Search for account details by UserId.
    
    :param user_id: The Bing Ads user identifier.
    :type user_id: long
    :return: List of accounts that the user can manage.
    :rtype: ArrayOfAccount
    '''
    global customer_service
   
    paging={
        'Index': 0,
        'Size': 10
    }

    predicates={
        'Predicate': [
            {
                'Field': 'UserId',
                'Operator': 'Equals',
                'Value': user_id,
            },
        ]
    }

    search_accounts_request={
        'PageInfo': paging,
        'Predicates': predicates
    }
        
    return customer_service.SearchAccounts(
        PageInfo = paging,
        Predicates = predicates
    )

def output_status_message(message):
    print(message)

def output_bing_ads_webfault_error(error):
    if hasattr(error, 'ErrorCode'):
        output_status_message("ErrorCode: {0}".format(error.ErrorCode))
    if hasattr(error, 'Code'):
        output_status_message("Code: {0}".format(error.Code))
    if hasattr(error, 'Message'):
        output_status_message("Message: {0}".format(error.Message))
    output_status_message('')

def output_webfault_errors(ex):
    if hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFault') \
        and hasattr(ex.fault.detail.ApiFault, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFault.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.ApiFault.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'AdApiFaultDetail') \
        and hasattr(ex.fault.detail.AdApiFaultDetail, 'Errors') \
        and hasattr(ex.fault.detail.AdApiFaultDetail.Errors, 'AdApiError'):
        api_errors=ex.fault.detail.AdApiFaultDetail.Errors.AdApiError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors=ex.fault.detail.ApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.ApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'EditorialErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.EditorialErrors, 'EditorialError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.EditorialErrors.EditorialError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    # Handle serialization errors e.g. The formatter threw an exception while trying to deserialize the message: 
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v9:Entities.
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ExceptionDetail'):
        api_errors=ex.fault.detail.ExceptionDetail
        if type(api_errors) == list:
            for api_error in api_errors:
                output_status_message(api_error.Message)
        else:
            output_status_message(api_errors.Message)
    else:
        raise Exception('Unknown WebFault')

def get_budget_report_request():
    '''
    Build a budget summary report request, including Format, ReportName,
    Time, and Columns.
    '''
    report_request=reporting_service.factory.create('BudgetSummaryReportRequest')
    report_request.Format=REPORT_FILE_FORMAT
    report_request.ReportName='My Budget Summary Report'
    report_request.ReturnOnlyCompleteData=False
    report_request.Language='English'

    scope=reporting_service.factory.create('AccountThroughCampaignReportScope')
    scope.AccountIds={'long': [authorization_data.account_id] }
    scope.Campaigns=None
    report_request.Scope=scope

    report_time=reporting_service.factory.create('ReportTime')
    # You may either use a custom date range or predefined time.
    
    #custom_date_range_start=reporting_service.factory.create('Date')
    #custom_date_range_start.Day=1
    #custom_date_range_start.Month=1
    #custom_date_range_start.Year=2015
    #report_time.CustomDateRangeStart=custom_date_range_start
    #custom_date_range_end=reporting_service.factory.create('Date')
    #custom_date_range_end.Day=28
    #custom_date_range_end.Month=2
    #custom_date_range_end.Year=2017
    #report_time.CustomDateRangeEnd=custom_date_range_end
    #report_time.PredefinedTime=None
    
    report_time.PredefinedTime='Yesterday'
    report_request.Time=report_time

    # Specify the attribute and data report columns.

    report_columns=reporting_service.factory.create('ArrayOfBudgetSummaryReportColumn')
    report_columns.BudgetSummaryReportColumn.append([
        'AccountName',
        'AccountNumber',
        'CampaignName',
        'CurrencyCode',
        'Date',
        'DailySpend',
    ])
    report_request.Columns=report_columns

    return report_request

def get_keyword_report_request():
    '''
    Build a keyword performance report request, including Format, ReportName, Aggregation,
    Scope, Time, Filter, and Columns.
    '''
    report_request=reporting_service.factory.create('KeywordPerformanceReportRequest')
    report_request.Format=REPORT_FILE_FORMAT
    report_request.ReportName='My Keyword Performance Report'
    report_request.ReturnOnlyCompleteData=False
    report_request.Aggregation='Daily'
    report_request.Language='English'

    scope=reporting_service.factory.create('AccountThroughAdGroupReportScope')
    scope.AccountIds={'long': [authorization_data.account_id] }
    scope.Campaigns=None
    scope.AdGroups=None
    report_request.Scope=scope

    report_time=reporting_service.factory.create('ReportTime')
    # You may either use a custom date range or predefined time.
    
    #custom_date_range_start=reporting_service.factory.create('Date')
    #custom_date_range_start.Day=1
    #custom_date_range_start.Month=1
    #custom_date_range_start.Year=2015
    #report_time.CustomDateRangeStart=custom_date_range_start
    #custom_date_range_end=reporting_service.factory.create('Date')
    #custom_date_range_end.Day=28
    #custom_date_range_end.Month=2
    #custom_date_range_end.Year=2017
    #report_time.CustomDateRangeEnd=custom_date_range_end
    #report_time.PredefinedTime=None
    
    report_time.PredefinedTime='Yesterday'
    report_request.Time=report_time

    # If you specify a filter, results may differ from data you see in the Bing Ads web application

    report_filter=reporting_service.factory.create('KeywordPerformanceReportFilter')
    report_filter.DeviceType=[
        'Computer',
        'SmartPhone'
    ]
    report_request.Filter=report_filter

    # Specify the attribute and data report columns.

    report_columns=reporting_service.factory.create('ArrayOfKeywordPerformanceReportColumn')
    report_columns.KeywordPerformanceReportColumn.append([
        'TimePeriod',
        'AccountId',
        'CampaignId',
        'Keyword',
        'KeywordId',
        'DeviceType',
        'BidMatchType',
        'Clicks',
        'Impressions',
        'Ctr',
        'AverageCpc',
        'Spend',
        'QualityScore',
    ])
    report_request.Columns=report_columns

    # You may optionally sort by any KeywordPerformanceReportColumn, and optionally
    # specify the maximum number of rows to return in the sorted report. 

    report_sorts=reporting_service.factory.create('ArrayOfKeywordPerformanceReportSort')
    report_sort=reporting_service.factory.create('KeywordPerformanceReportSort')
    report_sort.SortColumn='Clicks'
    report_sort.SortOrder='Ascending'
    report_sorts.KeywordPerformanceReportSort.append(report_sort)
    report_request.Sort=report_sorts

    report_request.MaxRows=10

    return report_request

def background_completion(reporting_download_parameters):
    '''
    You can submit a download or upload request and the ReportingServiceManager will automatically 
    return results. The ReportingServiceManager abstracts the details of checking for result file 
    completion, and you don't have to write any code for results polling.
    '''
    global reporting_service_manager
    result_file_path = reporting_service_manager.download_file(reporting_download_parameters)
    output_status_message("Download result file: {0}\n".format(result_file_path))

def submit_and_download(report_request):
    '''
    Submit the download request and then use the ReportingDownloadOperation result to 
    track status yourself using ReportingDownloadOperation.get_status().
    '''
    global reporting_service_manager
    reporting_operation = reporting_service_manager.submit_download(report_request)

    for i in range(10):
        time.sleep(reporting_service_manager.poll_interval_in_milliseconds / 1000.0)

        download_status = reporting_operation.get_status()
        
        if download_status.status == 'Completed':
            break
    
    result_file_path = reporting_operation.download_result_file(
        result_file_directory = FILE_DIRECTORY, 
        result_file_name = RESULT_FILE_NAME, 
        decompress = True, 
        overwrite = True
    )
    
    output_status_message("Download result file: {0}\n".format(result_file_path))

def download_results(request_id, authorization_data):
    '''
    If for any reason you have to resume from a previous application state, 
    you can use an existing download request identifier and use it 
    to download the result file. Use ReportingDownloadOperation.track() to indicate that the application 
    should wait to ensure that the download status is completed.
    '''
    reporting_download_operation = ReportingDownloadOperation(
        request_id = request_id, 
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=1000, 
        environment=ENVIRONMENT,
    )

    # Use track() to indicate that the application should wait to ensure that 
    # the download status is completed.
    reporting_operation_status = reporting_download_operation.track()
    
    result_file_path = reporting_download_operation.download_result_file(
        result_file_directory = FILE_DIRECTORY, 
        result_file_name = RESULT_FILE_NAME, 
        decompress = True, 
        overwrite = True) # Set this value true if you want to overwrite the same file.

    output_status_message("Download result file: {0}".format(result_file_path))
    output_status_message("Status: {0}".format(reporting_operation_status.status))

# Main execution
if __name__ == '__main__':

    try:
        # You should authenticate for Bing Ads production services with a Microsoft Account, 
        # instead of providing the Bing Ads username and password set. 
        # Authentication with a Microsoft Account is currently not supported in Sandbox.
        authenticate_with_oauth()

        # Uncomment to run with Bing Ads legacy UserName and Password credentials.
        # For example you would use this method to authenticate in sandbox.
        #authenticate_with_username()
        
        # Set to an empty user identifier to get the current authenticated Bing Ads user,
        # and then search for all accounts the user may access.
        user=customer_service.GetUser(None).User
        accounts=search_accounts_by_user_id(user.Id)

        # For this example we'll use the first account.
        authorization_data.account_id=accounts['Account'][0].Id
        authorization_data.customer_id=accounts['Account'][0].ParentCustomerId
        
        # You can submit one of the example reports, or build your own.

        report_request=get_keyword_report_request()
        #report_request=get_budget_report_request()
        
        reporting_download_parameters = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory = FILE_DIRECTORY, 
            result_file_name = RESULT_FILE_NAME, 
            overwrite_result_file = True, # Set this value true if you want to overwrite the same file.
        )

        #Option A - Background Completion with ReportingServiceManager
        #You can submit a download or upload request and the ReportingServiceManager will automatically 
        #return results. The ReportingServiceManager abstracts the details of checking for result file 
        #completion, and you don't have to write any code for results polling.

        output_status_message("Awaiting Background Completion . . .");
        background_completion(reporting_download_parameters)

        #Option B - Submit and Download with ReportingServiceManager
        #Submit the download request and then use the ReportingDownloadOperation result to 
        #track status yourself using ReportingServiceManager.get_status().

        output_status_message("Awaiting Submit and Download . . .");
        submit_and_download(report_request)

        #Option C - Download Results with ReportingServiceManager
        #If for any reason you have to resume from a previous application state, 
        #you can use an existing download request identifier and use it 
        #to download the result file. Use track() to indicate that the application 
        #should wait to ensure that the download status is completed.

        #For example you might have previously retrieved a request ID using submit_download.
        reporting_operation=reporting_service_manager.submit_download(report_request);
        request_id=reporting_operation.request_id;

        #Given the request ID above, you can resume the workflow and download the report.
        #The report request identifier is valid for two days. 
        #If you do not download the report within two days, you must request the report again.
        output_status_message("Awaiting Download Results . . .");
        download_results(request_id, authorization_data)

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

