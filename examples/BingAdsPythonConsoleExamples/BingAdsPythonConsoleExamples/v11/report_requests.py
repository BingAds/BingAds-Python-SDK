import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

from auth_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

# The directory for the report files.
FILE_DIRECTORY='c:/reports/'

# The name of the report download file.
DOWNLOAD_FILE_NAME='download.csv'

# The report file extension type.
REPORT_FILE_FORMAT='Csv'

# The maximum amount of time (in milliseconds) that you want to wait for the report download.
TIMEOUT_IN_MILLISECONDS=3600000

def main(authorization_data):

    try:
        # You can submit one of the example reports, or build your own.

        #report_request=get_budget_summary_report_request()
        #report_request=get_user_location_performance_report_request()
        report_request=get_keyword_performance_report_request()
        
        reporting_download_parameters = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory = FILE_DIRECTORY, 
            result_file_name = DOWNLOAD_FILE_NAME, 
            overwrite_result_file = True, # Set this value true if you want to overwrite the same file.
            timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS # You may optionally cancel the download after a specified time interval.
        )

        #Option A - Background Completion with ReportingServiceManager
        #You can submit a download request and the ReportingServiceManager will automatically 
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
        #to download the result file. 

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

def get_budget_summary_report_request():
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
    #custom_date_range_start.Year=int(strftime("%Y", gmtime()))-1
    #report_time.CustomDateRangeStart=custom_date_range_start
    #custom_date_range_end=reporting_service.factory.create('Date')
    #custom_date_range_end.Day=31
    #custom_date_range_end.Month=12
    #custom_date_range_end.Year=int(strftime("%Y", gmtime()))-1
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

def get_keyword_performance_report_request():
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
    #custom_date_range_start.Year=int(strftime("%Y", gmtime()))-1
    #report_time.CustomDateRangeStart=custom_date_range_start
    #custom_date_range_end=reporting_service.factory.create('Date')
    #custom_date_range_end.Day=31
    #custom_date_range_end.Month=12
    #custom_date_range_end.Year=int(strftime("%Y", gmtime()))-1
    #report_time.CustomDateRangeEnd=custom_date_range_end
    #report_time.PredefinedTime=None
    
    report_time.PredefinedTime='Yesterday'
    report_request.Time=report_time

    # If you specify a filter, results may differ from data you see in the Bing Ads web application

    #report_filter=reporting_service.factory.create('KeywordPerformanceReportFilter')
    #report_filter.DeviceType=[
    #    'Computer',
    #    'SmartPhone'
    #]
    #report_request.Filter=report_filter

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

def get_user_location_performance_report_request():
    '''
    Build a geo location performance report request, including Format, ReportName, Aggregation,
    Scope, Time, Filter, and Columns.
    '''
    report_request=reporting_service.factory.create('UserLocationPerformanceReportRequest')
    report_request.Format=REPORT_FILE_FORMAT
    report_request.ReportName='My Geographic Performance Report'
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
    #custom_date_range_start.Year=int(strftime("%Y", gmtime()))-1
    #report_time.CustomDateRangeStart=custom_date_range_start
    #custom_date_range_end=reporting_service.factory.create('Date')
    #custom_date_range_end.Day=31
    #custom_date_range_end.Month=12
    #custom_date_range_end.Year=int(strftime("%Y", gmtime()))-1
    #report_time.CustomDateRangeEnd=custom_date_range_end
    #report_time.PredefinedTime=None
    
    report_time.PredefinedTime='Yesterday'
    report_request.Time=report_time

    # If you specify a filter, results may differ from data you see in the Bing Ads web application

    report_filter=reporting_service.factory.create('UserLocationPerformanceReportFilter')
    country_codes=reporting_service.factory.create('ns1:ArrayOfstring')
    country_codes.string.append('US')
    report_filter.CountryCode=country_codes
    report_request.Filter=report_filter

    # Specify the attribute and data report columns.

    report_columns=reporting_service.factory.create('ArrayOfUserLocationPerformanceReportColumn')
    report_columns.UserLocationPerformanceReportColumn.append([
        'TimePeriod',
        'AccountId',
        'AccountName',
        'CampaignId',
        'AdGroupId',
        'LocationType',
        'Country',
        'Clicks',
        'Impressions',
        'Ctr',
        'AverageCpc',
        'Spend',
    ])
    report_request.Columns=report_columns

    return report_request

def background_completion(reporting_download_parameters):
    '''
    You can submit a download request and the ReportingServiceManager will automatically 
    return results. The ReportingServiceManager abstracts the details of checking for result file 
    completion, and you don't have to write any code for results polling.
    '''
    global reporting_service_manager
    result_file_path = reporting_service_manager.download_file(reporting_download_parameters)
    output_status_message("Download result file: {0}\n".format(result_file_path))

def submit_and_download(report_request):
    '''
    Submit the download request and then use the ReportingDownloadOperation result to 
    track status until the report is complete e.g. either using
    ReportingDownloadOperation.track() or ReportingDownloadOperation.get_status().
    '''
    global reporting_service_manager
    reporting_download_operation = reporting_service_manager.submit_download(report_request)

    # You may optionally cancel the track() operation after a specified time interval.
    reporting_operation_status = reporting_download_operation.track(timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS)

    # You can use ReportingDownloadOperation.track() to poll until complete as shown above, 
    # or use custom polling logic with get_status() as shown below.
    #for i in range(10):
    #    time.sleep(reporting_service_manager.poll_interval_in_milliseconds / 1000.0)

    #    download_status = reporting_download_operation.get_status()
        
    #    if download_status.status == 'Success':
    #        break
    
    result_file_path = reporting_download_operation.download_result_file(
        result_file_directory = FILE_DIRECTORY, 
        result_file_name = DOWNLOAD_FILE_NAME, 
        decompress = True, 
        overwrite = True,  # Set this value true if you want to overwrite the same file.
        timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS # You may optionally cancel the download after a specified time interval.
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
    # You may optionally cancel the track() operation after a specified time interval.
    reporting_operation_status = reporting_download_operation.track(timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS)
    
    result_file_path = reporting_download_operation.download_result_file(
        result_file_directory = FILE_DIRECTORY, 
        result_file_name = DOWNLOAD_FILE_NAME, 
        decompress = True, 
        overwrite = True,  # Set this value true if you want to overwrite the same file.
        timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS # You may optionally cancel the download after a specified time interval.
    ) 

    output_status_message("Download result file: {0}".format(result_file_path))
    output_status_message("Status: {0}\n".format(reporting_operation_status.status))

# Main execution
if __name__ == '__main__':

    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    reporting_service_manager=ReportingServiceManager(
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=5000, 
        environment=ENVIRONMENT,
    )

    # In addition to ReportingServiceManager, you will need a reporting ServiceClient 
    # to build the ReportRequest.

    reporting_service=ServiceClient(
        'ReportingService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
    # Authentication with a Microsoft Account is currently not supported in Sandbox.
        
    authenticate(authorization_data)
        
    main(authorization_data)