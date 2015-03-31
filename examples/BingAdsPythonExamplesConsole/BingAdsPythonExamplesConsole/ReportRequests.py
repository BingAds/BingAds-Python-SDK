from bingads import *

import time
import contextlib
import ssl
import requests
import zipfile
import os
import six

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

import webbrowser
from time import gmtime, strftime

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

    FILE_DIRECTORY='c:/reports/'

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
    )

    reporting_service=ServiceClient(
        'ReportingService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
    
class Ssl3HttpAdapter(HTTPAdapter):
    """" Transport adapter" that allows us to use SSLv3. """

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager=PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_SSLv3,
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
    #authorization_data.authentication.token_refreshed_callback=save_refresh_token
    
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

def download_result_file(url, result_file_directory, result_file_name, decompress, overwrite):
    """ Download file with specified URL and download parameters.

    :param result_file_directory: The download result local directory name.
    :type result_file_directory: str
    :param result_file_name: The download result local file name.
    :type result_file_name: str
    :param decompress: Determines whether to decompress the ZIP file.
                        If set to true, the file will be decompressed after download.
                        The default value is false, in which case the downloaded file is not decompressed.
    :type decompress: bool
    :param overwrite: Indicates whether the result file should overwrite the existing file if any.
    :type overwrite: bool
    :return: The download file path.
    :rtype: str
    """

    if result_file_directory is None:
        raise ValueError('result_file_directory cannot be None.')

    if result_file_name is None:
        result_file_name="default_file_name"

    if decompress:
        name, ext=os.path.splitext(result_file_name)
        if ext == '.zip':
            raise ValueError("Result file can't be decompressed into a file with extension 'zip'."
                                " Please change the extension of the result_file_name or pass decompress=false")
        zip_file_path=os.path.join(result_file_directory, name + '.zip')
        result_file_path=os.path.join(result_file_directory, result_file_name)
    else:
        result_file_path=os.path.join(result_file_directory, result_file_name)
        zip_file_path=result_file_path

    if os.path.exists(result_file_path) and overwrite is False:
        if six.PY3:
            raise FileExistsError('Result file: {0} exists'.format(result_file_path))
        else:
            raise OSError('Result file: {0} exists'.format(result_file_path))
    
    pool_manager=PoolManager(
        ssl_version=ssl.PROTOCOL_SSLv3,
    )
    http_adapter=HTTPAdapter()
    http_adapter.poolmanager=pool_manager
    
    s=requests.Session()
    s.mount('https://', http_adapter)
    r=s.get(url, stream=True, verify=True)
    r.raise_for_status()
    try:
        with open(zip_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
                    f.flush()
        if decompress:
            with contextlib.closing(zipfile.ZipFile(zip_file_path)) as compressed:
                first=compressed.namelist()[0]
                with open(result_file_path, 'wb') as f:
                    f.write(compressed.read(first))
    except Exception as ex:
        raise ex
    finally:
        if decompress and os.path.exists(zip_file_path):
            os.remove(zip_file_path)
    return result_file_path

def get_budget_report_request():
    '''
    Build a budget summary report request, including Format, ReportName,
    Time, and Columns.
    '''
    report_request=reporting_service.factory.create('BudgetSummaryReportRequest')
    report_request.Format='Csv'
    report_request.ReportName='My Budget Summary Report'
    report_request.ReturnOnlyCompleteData=False
    report_request.Language='English'

    scope=reporting_service.factory.create('AccountThroughCampaignReportScope')
    scope.AccountIds={'long': [authorization_data.account_id] }
    scope.Campaigns=None
    report_request.Scope=scope

    report_time=reporting_service.factory.create('ReportTime')
    # You may either use a custom date range or predefined time.
    '''
    custom_date_range_start=reporting_service.factory.create('Date')
    custom_date_range_start.Day=1
    custom_date_range_start.Month=1
    custom_date_range_start.Year=2015
    report_time.CustomDateRangeStart=custom_date_range_start
    custom_date_range_end=reporting_service.factory.create('Date')
    custom_date_range_end.Day=28
    custom_date_range_end.Month=2
    custom_date_range_end.Year=2015
    report_time.CustomDateRangeEnd=custom_date_range_end
    report_time.PredefinedTime=None
    '''
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
    report_request.Format='Csv'
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
    '''
    custom_date_range_start=reporting_service.factory.create('Date')
    custom_date_range_start.Day=1
    custom_date_range_start.Month=1
    custom_date_range_start.Year=2015
    report_time.CustomDateRangeStart=custom_date_range_start
    custom_date_range_end=reporting_service.factory.create('Date')
    custom_date_range_end.Day=28
    custom_date_range_end.Month=2
    custom_date_range_end.Year=2015
    report_time.CustomDateRangeEnd=custom_date_range_end
    report_time.PredefinedTime=None
    '''
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
        
        # Choose a helper method to build the report request, including Format, ReportName, Aggregation,
        # Scope, Time, Filter, and Columns.

        #report_request=get_budget_report_request()
        report_request=get_keyword_report_request()
        
        # SubmitGenerateReport returns the report identifier. The identifier is used to check report generation status
        # before downloading the report. 

        report_request_id=reporting_service.SubmitGenerateReport(
            ReportRequest=report_request,
        )
        result_file_name="{0}.csv".format(report_request_id)
        report_request_status=None

        # This example polls every 5 seconds up to 2 minutes.
        # In production you may poll the status every 1 to 2 minutes for up to one hour.
        # If the call succeeds, stop polling. If the call or 
        # download fails, the call throws a fault.

        for _ in range(24):
            time.sleep(5)
            report_request_status=reporting_service.PollGenerateReport(
                ReportRequestId=report_request_id
            )
            if report_request_status.Status == 'Success':
                output_status_message("Downloading from {0}.".format(report_request_status.ReportDownloadUrl))
                download_result_file(
                    url=report_request_status.ReportDownloadUrl,
                    result_file_directory=FILE_DIRECTORY,
                    result_file_name=result_file_name,
                    decompress=True,
                    overwrite=True,
                )
                output_status_message("The report was written to {0}{1}.".format(FILE_DIRECTORY, result_file_name))
                break
            elif report_request_status.Status == 'Error':
                output_status_message(
                    "The request failed. Try requesting the report. \n" \
                    "later.\nIf the request continues to fail, contact support."
                )
                break
        if report_request_status is not None:
            if report_request_status.Status != 'Success' and report_request_status.Status != 'Error':
                output_status_message(
                    "The request is taking longer than expected. \n" \
                    "Save the report ID ({0}) and try again later.".format(report_request_id)
                )

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

