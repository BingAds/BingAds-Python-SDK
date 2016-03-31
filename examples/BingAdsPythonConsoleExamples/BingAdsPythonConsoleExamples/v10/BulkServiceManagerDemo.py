from bingads.service_client import ServiceClient
from bingads.authorization import *
from bingads.v10 import *
from bingads.v10.bulk import *

import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    ENVIRONMENT='production'
    DEVELOPER_TOKEN='YourDeveloperTokenGoesHere'
    CLIENT_ID='YourClientIdGoesHere'

    # The directory for the bulk files.
    FILE_DIRECTORY='c:/bulk/'

    # The name of the bulk download file.
    DOWNLOAD_FILE_NAME='download.csv'

    #The name of the bulk upload file.
    UPLOAD_FILE_NAME='upload.csv'

    # The name of the bulk upload result file.
    RESULT_FILE_NAME='result.csv'

    # The bulk file extension type.
    FILE_FORMAT = DownloadFileType.csv

    # The bulk file extension type as a string.
    FILE_TYPE = 'Csv'

    # The maximum amount of time (in milliseconds) that you want to wait for the bulk download or upload.
    TIMEOUT_IN_MILLISECONDS=3600000

    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    # Take advantage of the BulkServiceManager class to efficiently manage ads and keywords for all campaigns in an account. 
    # The client library provides classes to accelerate productivity for downloading and uploading entities. 
    # For example the upload_entities method of the BulkServiceManager class submits your upload request to the bulk service, 
    # polls the service until the upload completed, downloads the result file to a temporary directory, and exposes BulkEntity-derived objects  
    # that contain close representations of the corresponding Campaign Management data objects and value sets.

    # Poll for downloads at reasonable intervals. You know your data better than anyone. 
    # If you download an account that is well less than one million keywords, consider polling 
    # at 15 to 20 second intervals. If the account contains about one million keywords, consider polling 
    # at one minute intervals after waiting five minutes. For accounts with about four million keywords, 
    # consider polling at one minute intervals after waiting 10 minutes. 
      
    bulk_service_manager=BulkServiceManager(
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=5000, 
        environment=ENVIRONMENT,
    )

    # In addition to BulkServiceManager, if you want to get performance data in the bulk download, 
    # then you need a Bulk ServiceClient to build the PerformanceStatsDateRange object.

    bulk_service=ServiceClient(
        service='BulkService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=10,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=10,
    )

    customer_service=ServiceClient(
        'CustomerManagementService', 
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

def print_percent_complete(progress):
    output_status_message("Percent Complete: {0}\n".format(progress.percent_complete))

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
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v10:Entities.
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

def background_completion(download_parameters):
    '''
    You can submit a download or upload request and the BulkServiceManager will automatically 
    return results. The BulkServiceManager abstracts the details of checking for result file 
    completion, and you don't have to write any code for results polling.
    '''
    global bulk_service_manager
    result_file_path = bulk_service_manager.download_file(download_parameters)
    output_status_message("Download result file: {0}\n".format(result_file_path))

def submit_and_download(submit_download_parameters):
    '''
    Submit the download request and then use the BulkDownloadOperation result to 
    track status until the download is complete e.g. either using
    BulkDownloadOperation.track() or BulkDownloadOperation.get_status().
    '''
    global bulk_service_manager
    bulk_download_operation = bulk_service_manager.submit_download(submit_download_parameters)

    # You may optionally cancel the track() operation after a specified time interval.
    download_status = bulk_download_operation.track(timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS)

    # You can use BulkDownloadOperation.track() to poll until complete as shown above, 
    # or use custom polling logic with getStatus() as shown below.
    #for i in range(10):
    #    time.sleep(bulk_service_manager.poll_interval_in_milliseconds / 1000.0)

    #    download_status = bulk_download_operation.get_status()
        
    #    if download_status.status == 'Completed':
    #        break
    
    result_file_path = bulk_download_operation.download_result_file(
        result_file_directory = FILE_DIRECTORY, 
        result_file_name = DOWNLOAD_FILE_NAME, 
        decompress = True, 
        overwrite = True, # Set this value true if you want to overwrite the same file.
        timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS # You may optionally cancel the download after a specified time interval.
    )
    
    output_status_message("Download result file: {0}\n".format(result_file_path))

def download_results(request_id, authorization_data):
    '''
    If for any reason you have to resume from a previous application state, 
    you can use an existing download request identifier and use it 
    to download the result file. Use BulkDownloadOperation.track() to indicate that the application 
    should wait to ensure that the download status is completed.
    '''
    bulk_download_operation = BulkDownloadOperation(
        request_id = request_id, 
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=1000, 
        environment=ENVIRONMENT,
    )

    # Use track() to indicate that the application should wait to ensure that 
    # the download status is completed.
    # You may optionally cancel the track() operation after a specified time interval.
    bulk_operation_status = bulk_download_operation.track(timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS)
    
    result_file_path = bulk_download_operation.download_result_file(
        result_file_directory = FILE_DIRECTORY, 
        result_file_name = DOWNLOAD_FILE_NAME, 
        decompress = True, 
        overwrite = True, # Set this value true if you want to overwrite the same file.
        timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS # You may optionally cancel the download after a specified time interval.
    ) 

    output_status_message("Download result file: {0}".format(result_file_path))
    output_status_message("Status: {0}\n".format(bulk_operation_status.status))

# Main execution
if __name__ == '__main__':

    errors=[]

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
        user_id=None
        user=customer_service.GetUser(None).User
        accounts=search_accounts_by_user_id(user.Id)
        
        # For this example we'll use the first account.
        authorization_data.account_id=accounts['Account'][0].Id
        authorization_data.customer_id=accounts['Account'][0].ParentCustomerId

        # In this example we will download all ads and keywords in the account.
        entities=['Ads','Keywords']

        # Optionally you can request performance data for the downloaded entities.
        performance_stats_date_range=bulk_service.factory.create('PerformanceStatsDateRange')
        performance_stats_date_range.PredefinedTime='LastFourWeeks'

        # DownloadParameters is used for Option A below.
        download_parameters = DownloadParameters(
            campaign_ids=None,
            data_scope=['EntityPerformanceData'],
            performance_stats_date_range=performance_stats_date_range,
            entities=entities,
            file_type=FILE_TYPE,
            last_sync_time_in_utc=None,
            result_file_directory = FILE_DIRECTORY, 
            result_file_name = DOWNLOAD_FILE_NAME, 
            overwrite_result_file = True, # Set this value true if you want to overwrite the same file.
            timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS # You may optionally cancel the download after a specified time interval.
        )
        
        # SubmitDownloadParameters is used for Option B and Option C below.
        submit_download_parameters = SubmitDownloadParameters(
            campaign_ids=None,
            data_scope=['EntityPerformanceData'],
            performance_stats_date_range=performance_stats_date_range,
            entities=entities,
            file_type=FILE_TYPE,
            last_sync_time_in_utc=None
        )

        #Option A - Background Completion with BulkServiceManager
        #You can submit a download request and the BulkServiceManager will automatically 
        #return results. The BulkServiceManager abstracts the details of checking for result file 
        #completion, and you don't have to write any code for results polling.

        output_status_message("Awaiting Background Completion . . .");
        background_completion(download_parameters)

        #Option B - Submit and Download with BulkServiceManager
        #Submit the download request and then use the BulkDownloadOperation result to 
        #track status yourself using BulkServiceManager.get_status().

        output_status_message("Awaiting Submit and Download . . .");
        submit_and_download(submit_download_parameters)

        #Option C - Download Results with BulkServiceManager
        #If for any reason you have to resume from a previous application state, 
        #you can use an existing download request identifier and use it 
        #to download the result file. Use track() to indicate that the application 
        #should wait to ensure that the download status is completed.

        #For example you might have previously retrieved a request ID using submit_download.
        bulk_download_operation=bulk_service_manager.submit_download(submit_download_parameters);
        request_id=bulk_download_operation.request_id;

        #Given the request ID above, you can resume the workflow and download the bulk file.
        #The download request identifier is valid for two days. 
        #If you do not download the bulk file within two days, you must request it again.
        output_status_message("Awaiting Download Results . . .");
        download_results(request_id, authorization_data)

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

