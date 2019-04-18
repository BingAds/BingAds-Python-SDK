from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.


def main(authorization_data):

    errors=[]

    try:
        # Download all campaigns, ad groups, and ads in the account.
        entities=['Campaigns', 'AdGroups', 'Ads']

        # DownloadParameters is used for Option A below.
        download_parameters = DownloadParameters(
            campaign_ids=None,
            data_scope=['EntityData', 'QualityScoreData'],
            download_entities=entities,
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
            data_scope=['EntityData', 'QualityScoreData'],
            download_entities=entities,
            file_type=FILE_TYPE,
            last_sync_time_in_utc=None
        )

        #Option A - Background Completion with BulkServiceManager
        #You can submit a download request and the BulkServiceManager will automatically 
        #return results. The BulkServiceManager abstracts the details of checking for result file 
        #completion, and you don't have to write any code for results polling.

        output_status_message("-----\nAwaiting Background Completion...")
        background_completion(download_parameters)

        #Option B - Submit and Download with BulkServiceManager
        #Submit the download request and then use the BulkDownloadOperation result to 
        #track status yourself using BulkServiceManager.get_status().

        output_status_message("-----\nAwaiting Submit and Download...")
        submit_and_download(submit_download_parameters)

        #Option C - Download Results with BulkServiceManager
        #If for any reason you have to resume from a previous application state, 
        #you can use an existing download request identifier and use it 
        #to download the result file. Use track() to indicate that the application 
        #should wait to ensure that the download status is completed.

        #For example you might have previously retrieved a request ID using submit_download.
        bulk_download_operation=bulk_service_manager.submit_download(submit_download_parameters)
        request_id=bulk_download_operation.request_id

        #Given the request ID above, you can resume the workflow and download the bulk file.
        #The download request identifier is valid for two days. 
        #If you do not download the bulk file within two days, you must request it again.
        output_status_message("-----\nAwaiting Download Results...")
        download_results(request_id, authorization_data)

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

def background_completion(download_parameters):
    '''
    You can submit a download or upload request and the BulkServiceManager will automatically 
    return results. The BulkServiceManager abstracts the details of checking for result file 
    completion, and you don't have to write any code for results polling.
    '''
    global bulk_service_manager
    result_file_path = bulk_service_manager.download_file(download_parameters)
    output_status_message("Download result file: {0}".format(result_file_path))

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
    
    output_status_message("Download result file: {0}".format(result_file_path))

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
    output_status_message("Status: {0}".format(bulk_operation_status.status))

# Main execution
if __name__ == '__main__':

    print("Loading the web service client proxies...")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    bulk_service_manager=BulkServiceManager(
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=5000, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
